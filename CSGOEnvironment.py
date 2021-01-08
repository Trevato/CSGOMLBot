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

from tf_agents.networks import actor_distribution_network

from pynput.keyboard import Key, Controller

from ScreenCapture.render import get_screen
from ClientInput.pressKey import execute_action

import PIL.Image


class CSGOEnvironment(py_environment.PyEnvironment):


  def __init__(self):

    # Actions the Agent can take. Each will stand for a key press, mouse press, or mouse position.

    self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=3, name='action')

    # Screenshot of game. Array is the dimensions of the image.
    self._observation_spec = array_spec.BoundedArraySpec((480, 640, 4), np.float32, minimum=0, maximum=255, name="game")

        # Screenshot of game. Array is the dimensions of the image.
        
        # Observation of the current client state in the game. This will change. This also may become the state.
        # 'gamestate': array_spec.BoundedArraySpec((4,), np.float32, minimum=0,
        #                                       maximum=1, name="gamestate")
                                              

    self._state = 0
    self._episode_ended = False

    # Create a controller object to be passed when executing an action.
    self.controller = Controller()

    # How many actions there are.
    self._num_actions = 4


  def action_spec(self):
    return self._action_spec


  def observation_spec(self):
    return self._observation_spec


# Game ends so restart.
  def _reset(self):

    # TODO: Restart CSGO.

    self._state = 0
    self._episode_ended = False
    return ts.restart(self.render())


  def _step(self, action):

    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()

    # Execute movement in game.
    execute_action(action, self.controller)

    if action == 3:
      self._episode_ended = True
      reward = 0
      return ts.termination(observation = [self.render()], reward=reward)
    elif action == 0:
      reward = 100
      return ts.transition(observation = [self.render()], reward=reward, discount=1.0)
    elif action == 1:
      reward = 100
      return ts.transition(observation = [self.render()], reward=reward, discount=1.0)
    else:
      reward = 0
      return ts.transition(observation = [self.render()], reward=0.0, discount=1.0)


  def render(self, mode='rgb_array'):

    # Grab screenshot of CSGO and normalize.
    return np.zeros(shape=(480, 640, 4), dtype=np.float32), np.divide(get_screen(), 255, dtype=np.float32)

if __name__ == '__main__':
  environment = CSGOEnvironment()
  tf_env = tf_py_environment.TFPyEnvironment(environment)

  time_step = environment.reset()
  print(time_step)
  rewards = []
  steps = []
  num_episodes = 5

  for _ in range(num_episodes):
    episode_reward = 0
    episode_steps = 0
    while not time_step.is_last():
      action = tf.random.uniform([1], 0, 4, dtype=tf.int32)
      time_step = tf_env.step(action)
      episode_steps += 1
      episode_reward += time_step.reward.numpy()
    rewards.append(episode_reward)
    steps.append(episode_steps)
    time_step = tf_env.reset()

  num_steps = np.sum(steps)
  avg_length = np.mean(steps)
  avg_reward = np.mean(rewards)

  print('num_episodes:', num_episodes, 'num_steps:', num_steps)
  print('avg_length', avg_length, 'avg_reward:', avg_reward)