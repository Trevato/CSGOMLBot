import os
import pygame
import time
import random
import numpy as np
from PIL import Image


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
        size = (100,100)
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

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()


        # Take "screenshot".

        data = pygame.image.tostring(self.screen, 'RGB')  # Take screenshot
        # image = Image.frombytes('RGB', (self._screen_width, self._screen_height), data)
        
        # Again placing a hardcoded region for testing.
        image = Image.frombytes('RGB', (100,100), data)
        image = image.convert('L')  # Convert to greyscale
        image = image.resize((INPUT_HEIGHT, INPUT_WIDTH))
        matrix = np.asarray(image.getdata(), dtype=np.uint8)
        matrix = (matrix - 128)/(128 - 1)  # Normalize from -1 to 1
        return matrix.reshape(image.size[0], image.size[1])

# Create an instance of the PyScope class
scope = pyscope()
scope.test()
time.sleep(10)
