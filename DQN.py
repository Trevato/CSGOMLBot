from __future__ import absolute_import, division, print_function

import base64
import imageio
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image

import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from CSGOEnvironment import CSGOEnvironment


def compute_avg_return(environment, policy, num_episodes=10):

  total_return = 0.0
  for _ in range(num_episodes):

    time_step = environment.reset()
    episode_return = 0.0

    while not time_step.is_last():
      action_step = policy.action(time_step)
      time_step = environment.step(action_step.action)
      episode_return += time_step.reward
    total_return += episode_return

  avg_return = total_return / num_episodes
  return avg_return.numpy()[0]


if __name__ == '__main__':

  num_iterations = 20000 # @param {type:"integer"}

  initial_collect_steps = 1000  # @param {type:"integer"} 
  collect_steps_per_iteration = 1  # @param {type:"integer"}
  replay_buffer_max_length = 100000  # @param {type:"integer"}

  # batch_size = 4  # @param {type:"integer"}
  learning_rate = 1e-3  # @param {type:"number"}
  log_interval = 200  # @param {type:"integer"}

  num_eval_episodes = 10  # @param {type:"integer"}
  eval_interval = 1000  # @param {type:"integer"}

  train_env = tf_py_environment.TFPyEnvironment(CSGOEnvironment())
  eval_env = tf_py_environment.TFPyEnvironment(CSGOEnvironment())
 
  fc_layer_params = (100,)

  preprocessing_layers = {
  'image': tf.keras.models.Sequential([tf.keras.layers.Conv2D(8, 4),
                                      tf.keras.layers.Flatten()]),
  'gamestate': tf.keras.layers.Dense(5)
  }
  preprocessing_combiner = tf.keras.layers.Concatenate(axis=-1)

  q_net = q_network.QNetwork(
      train_env.observation_spec(),
      train_env.action_spec(),
      preprocessing_layers=preprocessing_layers,
      preprocessing_combiner=preprocessing_combiner,
      fc_layer_params=fc_layer_params)
  
 
  optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

  train_step_counter = tf.Variable(0)

  agent = dqn_agent.DqnAgent(
      train_env.time_step_spec(),
      train_env.action_spec(),
      q_network=q_net,
      optimizer=optimizer,
      td_errors_loss_fn=common.element_wise_squared_loss,
      train_step_counter=train_step_counter)

  agent.initialize()

  eval_policy = agent.policy
  collect_policy = agent.collect_policy

  random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())

  time_step = train_env.reset()
  random_policy.action(time_step)
  print(random_policy.action(time_step))

  print(compute_avg_return(eval_env, random_policy, num_eval_episodes))

  replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=1,
    max_length=replay_buffer_max_length)

  print(agent.collect_data_spec)