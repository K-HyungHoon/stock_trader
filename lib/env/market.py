import os
import numpy as np
import gym
from gym import spaces


class Kospi200_Env(gym.Env):
    def __init__(self, history, labels, window_size=5):
        super(Kospi200_Env, self).__init__()
        self.history = history
        self.labels = labels
        self.window_size = window_size

        period, num_company, num_feature = self.history.shape

        # buy sell
        self.action_space = spaces.Box(0, 100, shape=(2, num_company))
        # open high low close
        self.observation_space = spaces.Box(0, 100, shape=(num_feature, period))

    def step(self, action):
        self.current_step += 1

    def reset(self):
        self.current_step = 0

        return self._next_observation()

    def _next_observation(self):
        obs = np.array([])

        return obs

    def render(self, mode='human'):
        if mode == 'print':
            print(f'STEP : {self.current_step}')

    def close(self):
        NotImplementedError()