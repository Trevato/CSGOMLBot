import cv2
import mss

import numpy as np

from time import time
from PIL import ImageGrab


def use_PIL(x1, y1, x2, y2):

    count = 0
    start = time()

    while count <= 120:

        # region=(560,240,1360,840)

        screen =  np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))

        #Convert to grayscale, effectively cutting off 2/3rds of data.
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        #Remove a lot of pixels for quicker training data. SHOULD use but not required.
        # screen = cv2.resize(screen, (480,270))

        count += 1

    print(time() - start)


def use_MSS():

    count = 0

    start = time()

    while count <= 0:

        with mss.mss() as sct:

            mon = sct.monitors[1]

            monitor = {
                "top": mon["top"] + 405,
                "left": mon["left"] + 720,
                "width": 480,
                "height": 270,
                "mon": 1,
            }

            output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

            # screen = np.array(sct.grab(monitor))
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        count += 1

    print(time() - start)

if __name__ == '__main__':
    use_PIL(0,0,480,270)
    use_MSS()
