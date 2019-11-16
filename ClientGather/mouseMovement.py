from ctypes import *

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def get_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}


# if __name__ == '__main__':
#     while(True):
#         print(get_mouse_position())
