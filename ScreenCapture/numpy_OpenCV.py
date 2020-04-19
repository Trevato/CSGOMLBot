import numpy as np
import cv2
import mss
import time
from PIL import Image


def fast_method():
    with mss.mss(display="0.0") as sct:
        # Part of the screen to capture
        monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

        while "Screen capturing":
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(monitor))

            # Display the picture
            # cv2.imshow("OpenCV/Numpy normal", img)

            # Display the picture in grayscale
            # cv2.imshow('OpenCV/Numpy grayscale',
            #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

            print("fps: {}".format(1 / (time.time() - last_time)))

            # Press "q" to quit
            # if cv2.waitKey(25) & 0xFF == ord("q"):
            #     cv2.destroyAllWindows()
            #     break

def test():
    with mss.mss(display=":0.0") as sct:
        for filename in sct.save():
            print(filename)

if __name__ == '__main__':
    resp = input('Enter mode:')
    if resp == 'fast':
        fast_method()
    elif resp == 'test':
        import pdb
        pdb.set_trace()
        test()   
