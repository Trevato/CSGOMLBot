import numpy as np
import os


current_file = 0
last_file = 0
previous_reward_index = 0
new_data = []

def get_next_file():
    starting_value = 0

    while True:
        file_name = 'training_data_adjusted_reward/training_data-{}.npy'.format(starting_value)

        if os.path.isfile(file_name):
            print('File exists.',starting_value)
            starting_value += 1
        else:
            return 'training_data_adjusted_reward/training_data-{}.npy'.format(starting_value)


def discount_rewards():
    global current_file
    global last_file
    global previous_reward_index
    global new_data

    while(current_file <= last_file):
        data = np.load('training_data/training_data-{}.npy'.format(current_file))
        print('File loaded!')
        data_points = len(data)

        x = previous_reward_index + 1

        if(x < data_points):
            print(x)
            if data[x][2] != 0:
                print('Test')
                i = x
                while(i > previous_reward_index + 1):
                    new_data[i-1][2] = np.log(data[i][2])
                    i -= 1

                previous_reward_index = x
                print(str(x) + 'of' + str(data_points))
                x += 1

        np.save(get_next_file(), new_data)
        new_data = []
        current_file += 1

if __name__ == '__main__':
    discount_rewards()

#Use Discounted Rewards and Normalized rewards to create better data
