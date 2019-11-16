import numpy as np
import time
import socket
import os
import threading
import mss

from getKeys import key_check
from getScreen import grab_screen
from mouseMovement import get_mouse_position
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE
from startServer import MyServer, MyRequestHandler


CSserver = MyServer(('localhost', 3000), MyRequestHandler)

output = {'w': 0, 's' : 0, 'a': 0, 'd' : 0, 'space': 0, '1': 0, '2' : 0, '3': 0, '4' : 0, '5': 0,
    'ctrl' : 0, 'shift' : 0, 'r_c' : 0, 'l_c' : 0, 'x' : 0, 'y' : 0}

def get_key_output(keys):
    if 'W' in keys:
        output['w'] = 1
    if 'S' in keys:
        output['s'] = 1
    if 'A' in keys:
        output['a'] = 1
    if 'D' in keys:
        output['d'] = 1
    if ' ' in keys:
        output['space'] = 1
    if '1' in keys:
        output['1'] = 1
    if '2' in keys:
        output['2'] = 1
    if '3' in keys:
        output['3'] = 1
    if '4' in keys:
        output['4'] = 1
    if '5' in keys:
        output['5'] = 1
    if 'ctrl' in keys:
        output['ctrl'] = 1
    if 'shift' in keys:
        output['shift'] = 1
    if 'l_c' in keys:
        output['l_c'] = 1
    if 'r_c' in keys:
        output['r_c'] = 1

def get_mouse_output():
    pos = get_mouse_position()
    output['x'] = pos['x']
    output['y'] = pos['y']

def reset_output():
    output['w'] = 0
    output['s'] = 0
    output['a'] = 0
    output['d'] = 0
    output['space'] = 0
    output['1'] = 0
    output['2'] = 0
    output['3'] = 0
    output['4'] = 0
    output['5'] = 0
    output['ctrl'] = 0
    output['shift'] = 0
    output['r_c'] = 0
    output['l_c'] = 0

def check_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 3000))
    return result

def screen_record():
    paused = True
    starting_value = 0
    training_data = []

    while True:
        file_name = 'training_data/training_data-{}.npy'.format(starting_value)

        if os.path.isfile(file_name):
            print('File exists.',starting_value)
            starting_value += 1
        else:
            print('File does not exist.',starting_value)

            break

    while(True):
        if not paused:

            # start = time.time()

            with mss.mss() as sct:

                mon = sct.monitors[1]

                monitor = {
                    "top": mon["top"] + 405,
                    "left": mon["left"] + 720,
                    "width": 480,
                    "height": 270,
                    "mon": 1,
                }

                screen = np.array(sct.grab(monitor))

            keys = key_check()

            get_key_output(keys)
            get_mouse_output()

            print(output)

            training_data.append([screen, str(output), getattr(CSserver, 'get_reward')()])

            reset_output()
            CSserver.reset_reward()

            # print(time.time() - start)

            if len(training_data) % 500 == 0:
                np.save(file_name,training_data)
                print('SAVED', starting_value)
                training_data = []
                starting_value += 1
                file_name = 'training_data/training_data-{}.npy'.format(starting_value)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)

def start_server(server):

        print(time.asctime(), '-', 'CS:GO gamestate server starting')

        try:
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
        except (KeyboardInterrupt, SystemExit):
            print('Server unable to start!')
            pass

if __name__ == '__main__':

    start_server(CSserver)

    # Popen([executable, 'startServer.py'], creationflags=CREATE_NEW_CONSOLE)
    if check_server() == 0:
       print("Server is up.")
    else:
       print("Server is not up. Waiting.")
       time.sleep(4)
    print('Waiting for input to start. Press \'T\' to start receiving data.')
    screen_record()
