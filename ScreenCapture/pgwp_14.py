import numpy as np

from cffi import FFI
ffi = FFI()
lib = ffi.dlopen("D:\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\directx_installer\\dsetup.dll")
ffi.cdef('''
    void list_processes();
    int DirectXLoadString();
    int get_capture_height();
    int get_capture_width();
    int get_capture_num_components();
    int capture_frame(uint8_t* copy_to_buffer);
    int get_image(uint8_t* copy_to);
''')


print(lib.DirectXLoadString())

# c_window_name = ffi.new("char[]", b"Counter Strike: Global Offenive")
# buffer_size = lib.init(c_window_name)
#
# capture_height = lib.get_capture_height()
# capture_width = lib.get_capture_width()
# capture_components = lib.get_capture_num_components()
#
# raw_buffer = np.empty((buffer_size), np.uint8)
#
# while True:
#     cap = lib.capture_frame(ffi.cast("uint8_t *", self.raw_buffer.ctypes.data))
#     # reshape to get it as a hxwxc numpy tensor instead of just one array.
#     capture = raw_buffer.reshape((capture_height,
#                                   capture_width,
#                                   capture_components))
#     # do something
