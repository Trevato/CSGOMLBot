from pynput.keyboard import Key, Controller


def execute_action(action, controller):
    action = action[0]
    print("Action:", action)
    keys = ['w', 's', 'a', 'd']

    controller.press(keys[action])
    print('Pressing: ' + keys[action])

    for key in keys:
        controller.release(keys[action])
