#include <windows.h>
#include <d3d11.h>
#include <dxgi1_2.h>

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define LEN(e) (sizeof(e)/sizeof(e[0]))

uint8_t test_image_rgba[] = {
    255,0,0,255, 0,255,0,255, 0,0,255,255,
    0,255,255,255, 255,0,255,255, 255,255,0,255
};

struct WindowBuf {
    HWND windows[100];
    int num_windows;
};

BOOL CALLBACK
enumWindowsProc(HWND hwnd, LPARAM lParam) {
    WindowBuf *buf = (WindowBuf*)lParam;

    if (IsWindowVisible(hwnd)) {
        buf->windows[buf->num_windows++] = hwnd;
    }

    return true;
}

void
listProcesses() {
    WindowBuf buf;
    buf.num_windows = 0;
    EnumWindows(enumWindowsProc, (LPARAM)&buf);

    char s[128];
    for (int p=0; p<buf.num_windows; p++) {
        HWND w = buf.windows[p];
        GetWindowText(w, (LPSTR)s, 128);
        if (strcmp(s, "") != 0) {
            printf("%s\n", s);
        }
    }
}

struct CaptureState {
    ID3D11Device *device;
    ID3D11DeviceContext *device_context;

    HWND capture_window;
    IDXGIOutputDuplication *output_duplication;

    int captured_display_left;
    int captured_display_top;
    int captured_display_right;
    int captured_display_bottom;

    int capture_window_left;
    int capture_window_top;
    int capture_window_right;
    int capture_window_bottom;

    ID3D11Texture2D *capture_texture;
    ID3D11Texture2D *region_copy_texture;
    IDXGISurface *region_copy_surface;

    int width;
    int height;
    int components;
};

int
captureStateInit(CaptureState* state, const char* window_name) {
    // Windows COM api stuff, sorta odd if you've never seen it before.
    IDXGIFactory1 *dxgi_factory = NULL;
    HRESULT hr = CreateDXGIFactory1(__uuidof(IDXGIFactory1), (void**)&dxgi_factory);
    if (FAILED(hr)) {
        return -1;
    }

    D3D_FEATURE_LEVEL supported_feature_levels[] = {
        D3D_FEATURE_LEVEL_11_1,
        D3D_FEATURE_LEVEL_11_0,
        D3D_FEATURE_LEVEL_10_1,
        D3D_FEATURE_LEVEL_10_0,
        D3D_FEATURE_LEVEL_9_3,
        D3D_FEATURE_LEVEL_9_2,
        D3D_FEATURE_LEVEL_9_1,
    };

    D3D_FEATURE_LEVEL fl;

    hr = D3D11CreateDevice(NULL, D3D_DRIVER_TYPE_HARDWARE, NULL, D3D11_CREATE_DEVICE_DEBUG,
                           supported_feature_levels, LEN(supported_feature_levels),
                           D3D11_SDK_VERSION, &state->device, &fl, &state->device_context);

    if (FAILED(hr)) {
        return -1;
    }

    state->output_duplication = NULL;

    state->captured_display_left = 0;
    state->captured_display_top = 0;
    state->captured_display_right = 0;
    state->captured_display_bottom = 0;

    state->capture_texture = NULL;
    state->region_copy_texture = NULL;
    state->region_copy_surface;

    state->capture_window = NULL;

    // find the window we want
    WindowBuf buf;
    buf.num_windows = 0;
    EnumWindows(enumWindowsProc, (LPARAM)&buf);

    char s[128];
    for (int p=0; p<buf.num_windows; p++) {
        HWND w = buf.windows[p];
        GetWindowText(w, (LPSTR)s, 128);
        if (strcmp(s, window_name) == 0) {
            state->capture_window = w;
            printf("Found the window! %s\n", s);
            break;
        }
    }

    if (!state->capture_window) {
        printf("Couldn't find window\n");
        return -1;
    }

    WINDOWINFO info;
    GetWindowInfo(state->capture_window, &info);

    state->capture_window_left = info.rcClient.left;
    state->capture_window_top = info.rcClient.top;
    state->capture_window_right = info.rcClient.right;
    state->capture_window_bottom = info.rcClient.bottom;

    // find the display that has the window on it.
    IDXGIAdapter1 *adapter;
    for (int adapter_index = 0;
         dxgi_factory->EnumAdapters1(adapter_index, &adapter) != DXGI_ERROR_NOT_FOUND;
         adapter_index++) {
        // enumerate outputs
        IDXGIOutput *output;
        for (int output_index = 0;
             adapter->EnumOutputs(output_index, &output) != DXGI_ERROR_NOT_FOUND;
             output_index++) {
            DXGI_OUTPUT_DESC output_desc;
            output->GetDesc(&output_desc);
            if (output_desc.AttachedToDesktop) {
                // printf("this display dimensions (%i,%i,%i,%i)\n",
                //        output_desc.DesktopCoordinates.top,
                //        output_desc.DesktopCoordinates.left,
                //        output_desc.DesktopCoordinates.bottom,
                //        output_desc.DesktopCoordinates.right);
                if (output_desc.DesktopCoordinates.left <= state->capture_window_left &&
                    output_desc.DesktopCoordinates.right >= state->capture_window_right &&
                    output_desc.DesktopCoordinates.top <= state->capture_window_top &&
                    output_desc.DesktopCoordinates.bottom >= state->capture_window_bottom) {

                    // printf("Display output found. DeviceName=%ls  AttachedToDesktop=%d Rotation=%d DesktopCoordinates={(%d,%d),(%d,%d)}\n",
                    //         output_desc.DeviceName,
                    //         output_desc.AttachedToDesktop,
                    //         output_desc.Rotation,
                    //         output_desc.DesktopCoordinates.left,
                    //         output_desc.DesktopCoordinates.top,
                    //         output_desc.DesktopCoordinates.right,
                    //         output_desc.DesktopCoordinates.bottom);

                    state->captured_display_left = output_desc.DesktopCoordinates.left;
                    state->captured_display_right = output_desc.DesktopCoordinates.right;
                    state->captured_display_bottom = output_desc.DesktopCoordinates.bottom;
                    state->captured_display_top = output_desc.DesktopCoordinates.top;

                    IDXGIOutput1 *output1 = (IDXGIOutput1*)output;
                    hr = output1->DuplicateOutput(state->device, &state->output_duplication);
                    if (FAILED(hr)) {
                        printf("Output Duplication Failed\n");
                        printf("%#x\n", hr);
                        return -1;
                    }
                    // printf("Output Duplicated\n");
                }
            }
            output->Release();
        }
        adapter->Release();
    }

    state->width = state->capture_window_right - state->capture_window_left;
    state->height = state->capture_window_bottom - state->capture_window_top;
    state->components = 4;

    // Return the size of the buffer needed to copy captures to.
    return state->width * state->height * state->components;
}

int
captureStateCaptureFrame(CaptureState* state, uint8_t* copy_to_buffer) {
    DXGI_OUTDUPL_FRAME_INFO capture_frame_info;
    IDXGIResource *resource;

    HRESULT hr = state->output_duplication->AcquireNextFrame(0,
                                                             &capture_frame_info,
                                                             &resource);
    if (FAILED(hr)) {
        // no new frame
        return 0;
    }

    resource->QueryInterface(__uuidof(ID3D11Texture2D), (void**)&state->capture_texture);
    resource->Release();

    if (!state->region_copy_texture) {
        D3D11_TEXTURE2D_DESC capture_texture_desc;
        state->capture_texture->GetDesc(&capture_texture_desc);

        D3D11_TEXTURE2D_DESC region_texture_desc;
        ZeroMemory(&region_texture_desc, sizeof(region_texture_desc));

        region_texture_desc.Width = state->width;
        region_texture_desc.Height = state->height;
        region_texture_desc.MipLevels = 1;
        region_texture_desc.ArraySize = 1;
        region_texture_desc.SampleDesc.Count = 1;
        region_texture_desc.SampleDesc.Quality = 0;
        region_texture_desc.Usage = D3D11_USAGE_STAGING;
        region_texture_desc.Format = capture_texture_desc.Format;
        region_texture_desc.BindFlags = 0;
        region_texture_desc.CPUAccessFlags = D3D11_CPU_ACCESS_READ;
        region_texture_desc.MiscFlags = 0;

        hr = state->device->CreateTexture2D(&region_texture_desc, NULL, &state->region_copy_texture);
        if (FAILED(hr)) {
            return -1;
        }
    }

    // copy region of screen to texture
    D3D11_BOX source_region;
    source_region.left = state->capture_window_left;
    source_region.right = state->capture_window_right;
    source_region.top = state->capture_window_top;
    source_region.bottom = state->capture_window_bottom;
    source_region.front = 0;
    source_region.back = 1;

    state->device_context->CopySubresourceRegion(state->region_copy_texture, 0, 0, 0, 0, state->capture_texture, 0, &source_region);
    state->region_copy_texture->QueryInterface(__uuidof(IDXGISurface), (void**)&state->region_copy_surface);

    DXGI_MAPPED_RECT rect;
    hr = state->region_copy_surface->Map(&rect, DXGI_MAP_READ);
    if (FAILED(hr)) {
        return -1;
    }

    uint8_t *dest = copy_to_buffer;
    uint8_t *src = rect.pBits;
    for (int row = 0; row < state->height; row++) {
        memcpy(dest, src, state->width * 4);
        dest += state->width * 4;
        src += rect.Pitch;
    }

    state->region_copy_surface->Unmap();
    state->region_copy_surface->Release();
    state->output_duplication->ReleaseFrame();

    return 1;
}

// We make the state static and global to make it easier to interact with python.
static CaptureState capture_state;

extern "C" {
    int
    get_image(uint8_t* copy_to) {
        memcpy((void*)copy_to, (void*)test_image_rgba, sizeof(test_image_rgba));
        return 1;
    }

    void
    list_processes() {
        listProcesses();
    }

    int
    init(const char* window_name) {
        return captureStateInit(&capture_state, window_name);
    }

    int
    get_capture_height() {
        return capture_state.height;
    }

    int
    get_capture_width() {
        return capture_state.width;
    }

    int
    get_capture_num_components() {
        return capture_state.components;
    }

    int
    capture_frame(uint8_t* copy_to_buffer) {
        return captureStateCaptureFrame(&capture_state, copy_to_buffer);
    }

}
