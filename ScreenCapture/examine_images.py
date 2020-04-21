import numpy as np
from PIL import Image


d = np.load('test.npy')

for image in d:
    img = Image.fromarray(image, 'BGRA')
    img.show()