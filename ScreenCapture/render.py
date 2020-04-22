import mss
import numpy as np


def get_screen():
    with mss.mss(display=":0") as sct:
        monitor = {"top": 0, "left": 0, "width": 640, "height": 480}
        return np.array(sct.grab(monitor))