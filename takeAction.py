import win32api
import win32con



def convert_keys(keys):

    for key in keys:
        if key == '1':
            key = 0x31
        elif key == '2':
            key = 0x32
        elif key == '3':
            key = 0x33
        elif key == '4':
            key = 0x34
        elif key == '5':
            key = 0x35
        elif key == 'Q':
            key = 0x51
        elif key == 'R':
            key = 0x52
        elif key == ' ':
            key = 0x20
        elif key == 'ctrl':
            key = 0xA2
        elif key == 'shift':
            key = 0xA0
        elif key == 'l_c':
            key = 0x01
        elif key == 'r_c':
            key = 0x02
        elif key == 'W':
            key = 0x57
        elif key == 'S':
            key = 0x53
        elif key == 'A':
            key = 0x41
        elif key == 'D':
            key = 0x44

    return keys

def press_keys(keys):
    for key in keys:
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)

def release_keys(keys):
    for key in keys:
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP , 0)
