import numpy as np
import cv2
import time


d = np.load(
    'c:/Users/trevo/OneDrive/TrevorProgramming/Laptop/CSGOMLBot/ScreenCapture/test.npy')

for image in d:
<<<<<<< HEAD
    print(image)
    cv2.imshow("OpenCV/Numpy normal", image)
    time.sleep(.5)
=======
    img = Image.fromarray(image, 'BGRA')
    img.show()
>>>>>>> 02b85f2d49623df612116541201c618936171e2f
