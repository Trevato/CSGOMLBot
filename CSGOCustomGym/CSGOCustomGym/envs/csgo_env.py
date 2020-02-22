import cv2, gym, numpy as np
from retro_contest.local import make
from retro import make as make_retro
from baselines.common.atari_wrappers import FrameStack

cv2.ocl.setUseOpenCL(False)

class PreprocessFrame(gym.ObservationWrapper):
    """
    Grayscaling image from three dimensional RGB pixelated images
    - Set frame to gray
    - Resize the frame to 96x96x1
    """
    def __init__(self, environment, width, height):
        gym.ObservationWrapper.__init__(self, environment)
        self.width = width
        self.height = height
        self.observation_space = gym.spaces.Box(low=0,
                                                high=255,
                                                shape=(self.height, self.width, 1),
                                                dtype=np.uint8)

    def observation(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_AREA)
        image = image[:, :, None]
        return image


class ActionsDiscretizer(gym.ActionWrapper):
    """
    Wrap a gym-retro environment and make it use discrete
    actions for the CSGO game.
    """
    def __init__(self, env):
        super(ActionsDiscretizer, self).__init__(env)
        buttons = ['W', 'S', 'A', 'D', 'SPACE', 'CTRL', 'SHIFT', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'LC', 'RC', 'R', 'LL', 'LR', 'LU', 'LD']

        actions = ['MOVE_FORWARD', 'MOVE_BACKWARD', 'MOVE_LEFT', 'MOVE_RIGHT', 'JUMP', 'CROUCH', 'WALK',
                    'SWAP_1', 'SWAP_2', 'SWAP_3', 'SWAP_4', 'SWAP_5', 'SWAP_6', 'SWAP_7', 'SWAP_8', 'SWAP_9',
                    'SHOOT', 'AIM', 'RELOAD', 'LOOK_LEFT', 'LOOK_RIGHT', 'LOOK_UP', 'LOOK_DOWN']
                    
        self._actions = []

        """
        What we do in this loop:
        For each action in actions
            - Create an array of 12 False (12 = nb of buttons) THESE WILL BE CHANGED!!!
            For each button in action: (for instance ['LEFT']) we need to make that left button index = True
                - Then the button index = LEFT = True
            In fact at the end we will have an array where each array is an action and each elements True of this array
            are the buttons clicked.
        """
        for action in actions:
            _actions = np.array([False] * len(buttons))
            for button in action:
                _actions[buttons.index(button)] = True
            self._actions.append(_actions)
        self.action_space = gym.spaces.Discrete(len(self._actions))

    def action(self, a):
        return self._actions[a].copy()

class RewardScaler(gym.RewardWrapper):
    """
    Bring rewards to a reasonable scale for PPO.
    This is incredibly important and effects performance
    drastically.
    """
    def reward(self, reward):

        return reward * 0.01

def wrap_environment(environment, n_frames=4):
    environment = ActionsDiscretizer(environment)
    environment = RewardScaler(environment)
    environment = PreprocessFrame(environment)
    environment = FrameStack(environment, n_frames)
    return environment

def create_new_environment(n_frames=4):
    """
    Create an environment with some standard wrappers.

    Trying to understand the make function.
    """

    environment = make(game="Counter-Strike Global Offensive", #Assuming just the name of the game?
                       state=None, #Not sure what this does at the moment so giving None.
                       bk2dir="./records")#Believe this is just a directory for records.

    environment = wrap_environment(environment=environment,
                                   n_frames=n_frames)

    return environment


def make_test_level_Green():
    return make_test()


def make_test(n_frames=4):
    """
    Create an environment with some standard wrappers.
    """

    # See comments on 'create_new_environment'
    environment = make_retro(game="Counter-Strike Global Offensive",
                             state=None,
                             record="./records")

    environment = wrap_environment(environment=environment,
                                   n_frames=n_frames)

    return environment
