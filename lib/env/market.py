import os
import gym
from gym import spaces


class Kospi200_Env(gym.Env):
    def __init__(self, history):
        super(Kospi200_Env, self).__init__()
        self.history = history

        period, num_company, num_feature = self.history.shape

        # buy sell
        self.action_space = spaces.Box(0, 100, shape=(2, num_company))
        # open high low close
        self.observation_space = spaces.Box(0, 100, shape=(num_feature, period))

    def step(self, action):
        NotImplementedError()

    def reset(self):
        NotImplementedError()

    def render(self, mode='human'):
        NotImplementedError()

    def close(self):
        NotImplementedError()