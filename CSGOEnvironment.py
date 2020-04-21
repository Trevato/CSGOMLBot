import numpy as np

from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
from tf_agents.specs import array_spec


class CSOGEnvironment(py_environment.PyEnvironment):


  def __init__(self):
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
    self._state = [0, 0, 0, 0, 0]
    self._episode_ended = False
    return ts.restart(np.array([self._state], dtype=np.int32))


  def _step(self, action):

    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()

    # Make sure episodes don't go on forever.
    self.move(action)

    if self.game_over():
      return ts.termination(np.array(self._state, dtype=np.int32), 0)

    for movement in action:
      if movement:
        reward = 100
        return ts.transition(
            np.array([self._state], dtype=np.int32), reward=reward, discount=1.0)
      else:
        return ts.transition(
            np.array([self._state], dtype=np.int32), reward=0.0, discount=1.0)


  def move(self, action):

# TODO: For every action, simulate a key press and then execute.
    if action[0]:
      # Move forward (W)
      pass
    if action[1]:
      # Move backwards (S)
      pass
    if action[2]:
      # Move left (A)
      pass
    if action[3]:
      # Move right (D)
      pass
    if action[3]:
      # Shoot (Left Click)
      pass


  def game_over(self):

    pass


if __name__ == '__main__':
  env = CSOGEnvironment()
  utils.validate_py_environment(env, episodes=5)