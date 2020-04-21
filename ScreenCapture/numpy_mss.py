import numpy as np
import cv2
import mss
import mss.tools
import time
from PIL import Image


def fast_method_with_screenshots():
    with mss.mss(display=":1") as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 640, "height": 480}

        count = 0

        while count < 10:
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img_array = np.array(sct.grab(monitor))

            im = sct.grab(monitor)

            mss.tools.to_png(im.rgb, im.size, output="screenshot" + str(count) + '.png')

            print("fps: {}".format(1 / (time.time() - last_time)))
            count+=1
            time.sleep(1)

def test():
    with mss.mss(display=":0") as sct:
        for filename in sct.save():
            print(filename)


def fast_method():
    with mss.mss(display=":1") as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 640, "height": 480}

        while True:
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img_array = np.array(sct.grab(monitor))

            print(img_array.shape)

            print("fps: {}".format(1 / (time.time() - last_time)))


def to_np(images):
    return np.asarray(images, dtype=np.float32)

def fast_method_with_array():
    array_of_images = []
    with mss.mss(display=":1") as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 640, "height": 480}

        for _ in range(50):
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            sct_img = sct.grab(monitor)

            # print(dir(sct_img))

            array_of_images.append(np.array(sct_img))

            print("fps: {}".format(1 / (time.time() - last_time)))

    np.save('test', array_of_images)


def show_images(array):
     for image in array:
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('Test', image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        time.sleep(.1)


if __name__ == '__main__':
    # resp = input('Enter mode:')
    # if resp == 'fast':
    #     fast_method()
    # elif resp == 'test':
    #     test()   

    fast_method_with_array()
