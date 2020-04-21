import numpy as np
import cv2
import time


d = np.load(
    'c:/Users/trevo/OneDrive/TrevorProgramming/Laptop/CSGOMLBot/ScreenCapture/test.npy')

for image in d:
    print(image)
    cv2.imshow("OpenCV/Numpy normal", image)
    time.sleep(.5)