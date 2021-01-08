import keyboard


def execute_action(action):
    print("Action:", action)
    keys = ['w', 's', 'a', 'd']

    keyboard.press(keys[action])
    print('Pressing: ' + keys[action])