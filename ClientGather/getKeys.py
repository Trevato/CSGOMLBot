import win32api as wapi


def key_check():
    keys = []
    if wapi.GetAsyncKeyState(0x31):
        keys.append('1')
    if wapi.GetAsyncKeyState(0x32):
        keys.append('2')
    if wapi.GetAsyncKeyState(0x33):
        keys.append('3')
    if wapi.GetAsyncKeyState(0x34):
        keys.append('4')
    if wapi.GetAsyncKeyState(0x35):
        keys.append('5')
    if wapi.GetAsyncKeyState(0x57):
        keys.append('W')
    if wapi.GetAsyncKeyState(0x53):
        keys.append('S')
    if wapi.GetAsyncKeyState(0x41):
        keys.append('A')
    if wapi.GetAsyncKeyState(0x44):
        keys.append('D')
    if wapi.GetAsyncKeyState(0x51):
        keys.append('Q')
    if wapi.GetAsyncKeyState(0x52):
        keys.append('R')
    if wapi.GetAsyncKeyState(0x54):
        keys.append('T')
    if wapi.GetAsyncKeyState(0x20):
        keys.append(' ')
    if wapi.GetAsyncKeyState(0xA2):
        keys.append("ctrl")
    if wapi.GetAsyncKeyState(0xA0):
        keys.append("shift")
    if wapi.GetAsyncKeyState(0x01):
        keys.append("l_c")
    if wapi.GetAsyncKeyState(0x02):
        keys.append("r_c")
    return keys

# if __name__ == '__main__':
#     while(True):
#         print(key_check())
