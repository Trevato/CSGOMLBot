import numpy as np
import cv2
import mss
import time
from PIL import Image


def fast_method():
    with mss.mss(display=":1") as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 640, "height": 480}

        array_of_images = []

        count = 0

        while count < 10:
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(monitor))

            array_of_images.append(img)

            print("fps: {}".format(1 / (time.time() - last_time)))
            count+=1

        np.save('test', array_of_images)


def test():
    with mss.mss(display=":1") as sct:
        for filename in sct.save():
            print(filename)

if __name__ == '__main__':
    # resp = input('Enter mode:')
    # if resp == 'fast':
    #     fast_method()
    # elif resp == 'test':
    #     test()   

    fast_method()
