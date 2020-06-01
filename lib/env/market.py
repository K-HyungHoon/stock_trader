import gym
import numpy as np
import tensorflow.keras.backend as K
import matplotlib

matplotlib.use('TkAgg')

from lib.env.render import Confusion


class Kospi200_Env(gym.Env):
    def __init__(self, history, changes, labels, indices, window_size=5):
        super(Kospi200_Env, self).__init__()
        self.live = Confusion()

        self.history = history
        self.changes = changes

        self.labels = labels
        self.indices = indices
        self.window_size = window_size

        self.num_company = self.history.shape[0]
        self.period = self.history.shape[1]
        self.num_feature = self.history.shape[2]

        print(f'period : {self.period} | num_company : {self.num_company} | num_feature : {self.num_feature}')

    def step(self, action):
        self.action = action
        self.change = self.changes[self.current_step + self.window_size]
        self.reward = self.change * self.action
        # self.reward = np.log(self.change/self.indices)

        if self.current_step >= self.period - self.window_size - 1:
            self.done = True

        self.current_step += 1

        return self._get_state(), self.reward, self.done

    def reset(self):
        self.current_step = 0
        self.reward = 0
        self.done = False

        return self._get_state()

    def _get_state(self):
        obs = self.history[:, self.current_step: self.current_step + self.window_size]
        return np.expand_dims(obs, axis=0)

    def render(self, mode=None):
        if mode == 'print':
            print(f'STEP : {self.current_step} REWARD : {self.reward}')

        elif mode == 'confusion':
            self.live.render(self.change, self.action)

        elif mode is None:
            pass

    def close(self):
        NotImplementedError()
