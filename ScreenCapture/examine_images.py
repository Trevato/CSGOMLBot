import numpy as np
import cv2
import time


d = np.load(
    'c:/Users/trevo/OneDrive/TrevorProgramming/Laptop/CSGOMLBot/test.npy')


for image in d:
    print(image)
    cv2.imshow("OpenCV/Numpy normal", image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    time.sleep(.1)
