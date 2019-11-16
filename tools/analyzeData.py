import numpy as np
import cv2
import time
import tensorflow as tf


def analyze():
    data_length = 3
    data_points = 0
    i = 0
    x = 0

    while(i < data_length):
        data = np.load('training_data/training_data-{}.npy'.format(i))
        data_points = len(data)
        while(x < data_points):
            img = data[x][0]
            output = data[x][1]
            reward = data[x][2]
            print(str(output) + '\t\t' + str(reward))
            cv2.imshow('Test Image', img)
            cv2.waitKey(100)
            x += 1
        i += 1

def check_version():
    print(tf.version())

if __name__ == '__main__':
    check_version()
