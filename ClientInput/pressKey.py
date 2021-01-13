import keyboard
import time
import mouse


def execute_action(action):
    keys = ['w', 's', 'a', 'd']

    keyboard.press(keys[action])

def execute_action_mouse(x, y, action):
    mouse.move(x, y, duration=.02)
    if action == 0:
        pass
    elif action == 1:
        mouse.click(button='left')
    elif action == 2:
        mouse.click(button='right')

if __name__ == '__main__':
    execute_action_mouse(500,500,2)