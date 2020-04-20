import os
import pygame
import time
import mss
import random
import numpy as np
from PIL import Image
from matplotlib.pyplot import imshow

import timeit


WIDTH = 1920
HEIGHT = 1080

class pyscope :
    screen = None;

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib', 'dummy']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        # size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        # Technically the screen "doesn't exist" so give it a hard value. This will
        # match the game screen.
        size = (WIDTH,HEIGHT)
        print("Framebuffer size: %d x %d" % (size[0], size[1]))
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def screenshot(self):

        # Take "screenshot".

        data = pygame.image.tostring(self.screen, 'RGB')  # Take screenshot

        # Again placing a hardcoded region for testing.
        image = Image.frombytes('RGB', (WIDTH,HEIGHT), data)
        image.show()
        return image

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

    def fast_method(self):
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

# Create an instance of the PyScope class
scope = pyscope()
scope.test()
scope.screenshot()
scope.fast_method()
# print(timeit.Timer(scope.screenshot).timeit(120))
