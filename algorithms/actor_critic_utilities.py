import time, tensorflow as tf, numpy as np
from baselines.common.runners import AbstractEnvRunner
from baselines.common import explained_variance

def mse(pred, target):
    return tf.square(pred-target)/2.

def find_trainable_variables(key):
    with tf.variable_scope(key):
        return tf.trainable_variables()

def swap_flatten_axes(array):
    return arrary.swapaxes(0, 1).reshape(array.shape[0] * array.shape[1], * array.shape[2:])

class Model(object):

    def __init__(self, session, policy_model, observation_space, action_space, n_environments,
                 n_steps, entropy_coefficient, value_coefficient, max_grad_norm):

        session.run(tf.global_variables_initializer())
        actions_ = tf.placeholder(tf.int32, [None], name='actions')
        advantages_ = tf.placeholder(tf.float32, [None], name='advantages')
        rewards_ = tf.placeholder(tf.float32, [None], name='rewards')
        learning_rate = tf.placeholder(tf.float32, name='learning_rate')
        step_model = policy_model(session, observation_space, action_space, n_environments, 1, reuse=False)
        train_model = policy_model(session, observation_space, action_space, n_environments*n_steps, n_steps, reuse=tf.AUTO_REUSE)

        error_rate = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=train_model.logits, labels=actions_)
        mean_squared_error = tf.reduce_mean(advantages_ * error_rate)

        value_loss = tf.reduce_mean(mse(tf.squeeze(train_model.value_function),rewards_))
        entropy = tf.reduce_mean(train_model.distribution.entropy())
        loss = mean_squared_error - entropy * entropy_coefficient + value_loss * value_coefficient

        params = find_trainable_variables('model')
        gradients = tf.gradients(loss, params)
        if max_grad_norm is not None:
            gradients, grad_norm = tf.clip_by_global_norm(gradients, max_grad_norm)

        gradients = list(zip(gradients, params))
        trainer = tf.train.RMSPropOptimizer(learning_rate=learning_rate, decay=0.99, epsilon=1e-5)
        _train = trainer.apply_gradients(gradients)

        def train(states_in, actions, returns, values, learning_rate):
            advantages = returns - values

            dictionary = {train_model.inputs_: states_in,
                         actions_: actions,
                         advantages_: advantages,
                         rewards_: returns,
                         learning_rate: learning_rate}

            with tf.Session() as session:
                _policy_loss, _value_loss, _policy_entropy, _= session.run([mean_squared_error,
                                                                            value_loss,
                                                                            entropy,
                                                                            _train], dictionary)
            return _policy_loss, _value_loss, _policy_entropy

        def save(save_path):
            saver = tf.train.Saver()
            saver.save(session, save_path)

        def load(load_path):
            saver = tf.train.Saver()
            print('Loading ' + load_path)
            saver.restore(session, load_path)

        self.train = train
        self.train_model = train_model
        self.step_model = step_model
        self.step = step_model.step
        self.value = step_model.value
        self.initial_state = step_model.initial_state
        self.save = save
        self.load = load
        tf.global_variables_initializer().run(session=tf.Session())

class ModelTrainer(AbstractEnvRunner):

    def __init__(self, environment, model, n_steps, n_timesteps, gamma, _lambda):
        self.environment = environment
        self.model = model
        self.n_steps = n_steps
        self.gamma = gamma
        self._lambda = _lambda
        self.n_timesteps = n_timesteps
        self.observations = environment.reset()
        self.dones = False

    def step(self):

        _observations, _actions, _rewards, _values, _dones = [],[],[],[],[]

        for _ in range(self.n_steps):
            actions, values = self.model.step(self.observations, self.dones)
            _observations.append(np.copy(self.observations))
            _actions.append(actions)
            _values.append(values)
            _dones.append(self.dones)
            if self.dones: self.environment.reset()

            for action in actions:
                self.environment.render()
                self.observations[:], rewards, self.dones, _ = self.environment.step(action)
                _rewards.append(rewards)

        #batch of steps to batch of rollouts
        _observations = np.asarray(_observations, dtype=np.uint8)
        _rewards = np.asarray(_rewards, dtype=np.float32)
        _actions = np.asarray(_actions, dtype=np.int32)
        _values = np.asarray(_values, dtype=np.float32)
        _dones = np.asarray(_dones, dtype=np.bool)
        last_values = self.model.value(self.observations)
        _returns = np.zeros_like(_rewards)
        _advantages = np.zeros_like(_rewards)
        last_lambda = 0

        for t in reversed(range(self.n_steps)):
            if t == self.nsteps - 1:
                next_nonterminal = 1.0 - self.dones
                next_values = last_values
            else:
                next_nonterminal = 1.0 - _dones[t+1]
                next_values = _values[t+1]

            delta = _rewards[t] + self.gamma * nextvalues * nextnonterminal - _values[t]
            _advantages[t] = last_lambda = delta + self.gamma * self._lambda * nextnonterminal * last_lambda

        _returns = _advantages + _values
        return map(swap_flatten_axes, (_observations, _actions, _returns, _values))


def train_model(policy_model, environment, n_steps, max_steps, gamma, _lambda,
                value_coefficient, entropy_coefficient, learning_rate, max_grad_norm, log_interval):

    n_epochs = 4
    n_batches = 8
    n_environments = 1 #environment.num_envs
    observation_space = environment.observation_space
    action_space = environment.action_space
    batch_size = n_environments * n_steps
    batch_train_size = batch_size // n_batches
    assert batch_size % n_batches == 0
    session = tf.Session()

    model = Model(session=session,
                      policy_model=policy_model,
                      observation_space=observation_space,
                      action_space=action_space,
                      n_environments=1,
                      n_steps=1,
                      entropy_coefficient=0,
                      value_coefficient=0,
                      max_grad_norm=0)

    model_trainer = ModelTrainer(environment=environment,
                            model=model,
                            n_steps=n_steps,
                            n_timesteps=max_steps,
                            gamma=gamma,
                            _lambda=_lambda)

    initial_start_time = time.time()


    for update in range(1, max_steps//batch_size+1):

        timer_start = time.time()
        observations, actions, returns, values = model_trainer.step()
        mb_losses = []
        total_batches_train = 0
        indices = np.arange(batch_size)

        for _ in range(n_epochs):
            np.random.shuffle(indices)
            for start in range(0, batch_size, batch_train_size):
                end = start + batch_train_size
                mbinds = indices[start:end]
                slices = (arr[mbinds] for arr in (obs, actions, returns, values))
                mb_losses.append(model.train(*slices, lr))

        loss = np.mean(mb_losses, axis=0)
        frames_per_second = int(batch_size / (time.time() - initial_start_time))

        if update % log_interval == 0 or update == 1:

            """
            Computes fraction of variance that ypred explains about y.
            Returns 1 - Var[y-ypred] / Var[y]
            interpretation:
            explained_variance = 0  =>  might as well have predicted zero
            explained_variance = 1  =>  perfect prediction
            explained_variance < 0  =>  worse than just predicting zero
            """
            _explained_variance = explained_variance(values, returns)
            logger.record_tabular("nupdates", update)
            logger.record_tabular("total_timesteps", update*batch_size)
            logger.record_tabular("fps", frames_per_second)
            logger.record_tabular("policy_loss", float(loss[0]))
            logger.record_tabular("policy_entropy", float(loss[2]))
            logger.record_tabular("value_loss", float(loss[1]))
            logger.record_tabular("explained_variance", float(_explained_variance))
            logger.record_tabular("time elapsed", float(time.time() - initial_start_time))
            logger.dump_tabular()

            savepath = "./models/" + str(update) + "/model.ckpt"
            model.save(savepath)
            print('Saving to', savepath)

    environment.close()
    return model
