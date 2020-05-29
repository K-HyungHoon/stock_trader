import os
import numpy as np
import gym
from gym import spaces
import tensorflow.keras.backend as K


class Kospi200_Env(gym.Env):
    def __init__(self, history, labels, window_size=5):
        super(Kospi200_Env, self).__init__()
        self.history = history
        self.labels = labels
        self.window_size = window_size

        self.num_company = self.history.shape[0]
        self.period = self.history.shape[1]
        self.num_feature = self.history.shape[2]

        print(f'period : {self.period} | num_company : {self.num_company} | num_feature : {self.num_feature}')

        # buy sell
        self.action_space = spaces.Box(0, 100, shape=(2, self.num_company))
        # open high low close
        self.observation_space = spaces.Box(0, 100, shape=(self.num_feature, self.period))

    def step(self, action):
        if self.current_step >= self.period - self.window_size - 1:
            self.current_step = 0
            self.done = True

        self.current_step += 1

        action = action[0]

        action[action < 0] = 0
        action[action >= 0] = 1

        self.reward = action * self.history[:, self.current_step + self.window_size, -1]

        self.reward = K.constant(self.reward)

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
        elif mode is None:
            pass

    def close(self):
        NotImplementedError()