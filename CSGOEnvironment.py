from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

from ScreenCapture.render import get_screen


class CSOGEnvironment(py_environment.PyEnvironment):


  def __init__(self):

    # Actions the Agent can take. Each will stand for a key press, mouse press, or mouse position.

    self._action_spec = array_spec.BoundedArraySpec(
        shape=(5,), dtype=np.int32, minimum=[0, 0, 0, 0, 0], maximum=[1, 1, 1, 1, 1],  name='action')
    self._observation_spec = {

        # Screenshot of game. Array is the dimensions of the image.
        'image': array_spec.BoundedArraySpec((480, 640, 4), np.float32, minimum=0,
                                             maximum=255),
        # Observation of the current client state in the game. This will change.
        'gamestate': array_spec.BoundedArraySpec((4,), np.int32, minimum=0,
                                              maximum=1)}

    self._state = [0,0,0,0,0]
    self._episode_ended = False


  def action_spec(self):
    return self._action_spec


  def observation_spec(self):
    return self._observation_spec


# Game ends so restart.
  def _reset(self):

    # TODO: Restart CSGO.

    self._state = [0, 0, 0, 0, 0]
    self._episode_ended = False
    return ts.restart(np.array([self._state], dtype=np.int32))


  def _step(self, action):

    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()

    # Execute movement in game.
    self.move(action)

    if self.game_over():
      return ts.termination(np.array(self._state, dtype=np.int32), 0)

    for movement in action:
      if movement:
        reward = 100
        return ts.transition(self.render(), reward=reward, discount=1.0)
      else:
        return ts.transition(self.render(), reward=0.0, discount=1.0)


  def render(self, mode='rgb_array'):

    # Grab screenshot of CSGO and normalize.
    return np.divide(get_screen(), 255, dtype=np.float32)


  def move(self, action):

# TODO: For every action, simulate a key press and then execute.
    if action[0]:
      print('Move Forward')
    if action[1]:
      print('Move Backwards')
    if action[2]:
      print('Move Right')
    if action[3]:
      print('Move Left')
    if action[4]:
      print('Shoot')


  def game_over(self):
    pass


if __name__ == '__main__':

  action_array = np.zeros(shape=(5,), dtype=np.int32)

# Adjust the action array to adjust the actions.

  action_array[3] = 1

  environment = CSOGEnvironment()
  time_step = environment.reset()
  print(time_step)
  cumulative_reward = time_step.reward

  for _ in range(3):
    time_step = environment.step(action_array)
    print(time_step)
    cumulative_reward += time_step.reward

  cumulative_reward += time_step.reward
  print('Final Reward = ', cumulative_reward)


  # utils.validate_py_environment(env, episodes=5)