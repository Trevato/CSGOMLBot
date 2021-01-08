from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

import tensorflow as tf
from absl import flags, app
from absl import logging
from tf_agents.agents.ppo import ppo_agent
from tf_agents.drivers import dynamic_episode_driver
from tf_agents.environments import parallel_py_environment
from tf_agents.environments import tf_py_environment
from tf_agents.metrics import tf_metrics
from tf_agents.networks.actor_distribution_rnn_network import ActorDistributionRnnNetwork
from tf_agents.networks.value_rnn_network import ValueRnnNetwork
from tf_agents.replay_buffers import tf_uniform_replay_buffer

from CSGOEnvironment import CSGOEnvironment

# from utils.visualization_helper import create_video

# flags.DEFINE_string('videos_dir', os.getenv('TEST_UNDECLARED_OUTPUTS_DIR'), 'Directory to write evaluation videos to')
# FLAGS = flags.FLAGS


def create_networks(observation_spec, action_spec):
	actor_net = ActorDistributionRnnNetwork(
		observation_spec,
		action_spec,
		conv_layer_params=[(16, 8, 4), (32, 4, 2)],
		input_fc_layer_params=(256,),
		lstm_size=(256,),
		output_fc_layer_params=(128,),
		activation_fn=tf.nn.elu)
	value_net = ValueRnnNetwork(
		observation_spec,
		conv_layer_params=[(16, 8, 4), (32, 4, 2)],
		input_fc_layer_params=(256,),
		lstm_size=(256,),
		output_fc_layer_params=(128,),
		activation_fn=tf.nn.elu)

	return actor_net, value_net


def train_eval_doom_simple(
		# Params for collect
		num_environment_steps=30000000,
		collect_episodes_per_iteration=32,
		num_parallel_environments=32,
		replay_buffer_capacity=301,  # Per-environment
		# Params for train
		num_epochs=25,
		learning_rate=4e-4,
		# Params for eval
		eval_interval=500,
		num_video_episodes=10,
		# Params for summaries and logging
		log_interval=50):
	"""A simple train and eval for PPO."""
	# if not os.path.exists(videos_dir):
	# 	os.makedirs(videos_dir)

	# eval_py_env = CSGOEnvironment()
	# eval_tf_env = tf_py_environment.TFPyEnvironment(eval_py_env)
	tf_env = tf_py_environment.TFPyEnvironment(CSGOEnvironment())

	actor_net, value_net = create_networks(tf_env.observation_spec(), tf_env.action_spec())

	global_step = tf.compat.v1.train.get_or_create_global_step()
	optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate, epsilon=1e-5)

	tf_agent = ppo_agent.PPOAgent(
		tf_env.time_step_spec(),
		tf_env.action_spec(),
		optimizer,
		actor_net,
		value_net,
		num_epochs=num_epochs,
		train_step_counter=global_step,
		discount_factor=0.99,
		gradient_clipping=0.5,
		entropy_regularization=1e-2,
		importance_ratio_clipping=0.2,
		use_gae=True,
		use_td_lambda_return=True
	)
	tf_agent.initialize()

	environment_steps_metric = tf_metrics.EnvironmentSteps()
	step_metrics = [
		tf_metrics.NumberOfEpisodes(),
		environment_steps_metric,
	]

	replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(tf_agent.collect_data_spec, batch_size=num_parallel_environments, max_length=replay_buffer_capacity)
	collect_driver = dynamic_episode_driver.DynamicEpisodeDriver(tf_env, tf_agent.collect_policy, observers=[replay_buffer.add_batch] + step_metrics, num_episodes=collect_episodes_per_iteration)


	def train_step():
		trajectories = replay_buffer.gather_all()
		return tf_agent.train(experience=trajectories)


	# def evaluate():
	# 	create_video(eval_py_env, eval_tf_env, tf_agent.policy, num_episodes=num_video_episodes, video_filename=os.path.join(videos_dir, "video_%d.mp4" % global_step_val))


	collect_time = 0
	train_time = 0
	timed_at_step = global_step.numpy()

	while environment_steps_metric.result() < num_environment_steps:

		start_time = time.time()
		collect_driver.run()
		collect_time += time.time() - start_time

		start_time = time.time()
		total_loss, _ = train_step()
		replay_buffer.clear()
		train_time += time.time() - start_time

		global_step_val = global_step.numpy()

		if global_step_val % log_interval == 0:
			logging.info('step = %d, loss = %f', global_step_val, total_loss)
			steps_per_sec = ((global_step_val - timed_at_step) / (collect_time + train_time))
			logging.info('%.3f steps/sec', steps_per_sec)
			logging.info('collect_time = {}, train_time = {}'.format(collect_time, train_time))

			timed_at_step = global_step_val
			collect_time = 0
			train_time = 0

	# 	if global_step_val % eval_interval == 0:
	# 		evaluate()

	# evaluate()


def main(_):
	tf.compat.v1.enable_v2_behavior()  # For TF 1.x users
	logging.set_verbosity(logging.INFO)
	train_eval_doom_simple()


if __name__ == '__main__':
	# flags.mark_flag_as_required('videos_dir')
	app.run(main)