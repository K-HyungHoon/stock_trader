import gym
import numpy as np
import tensorflow.keras.backend as K
from gym import spaces
from .render import Confusion


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
        if self.first_step is False:
            self.first_step = True

        if self.current_step >= self.period - self.window_size - 1:
            self.current_step = 0
            self.done = True
            self.first_step = False

        self.current_step += 1

        self.action = action[0]
        self.change = self.history[:, self.current_step + self.window_size, -1]

        self.reward = self.action * self.change
        self._reward_scaling()

        return self._get_state(), self.reward, self.done

    def reset(self):
        self.current_step = 0
        self.reward = 0
        self.change = None
        self.action = None
        self.live = None
        self.first_step = False
        self.done = False

        return self._get_state()

    def _get_state(self):
        obs = self.history[:, self.current_step: self.current_step + self.window_size]

        return np.expand_dims(obs, axis=0)

    def _reward_scaling(self):
        self.reward = K.constant(self.reward - np.mean(self.reward)) / (np.std(self.reward) + 1e-7)

    def render(self, mode=None):
        if mode == 'print':
            print(f'STEP : {self.current_step} REWARD : {self.reward}')
        elif mode == 'confusion':
            if self.first_step:
                self.live = Confusion()

            self.live.render(self.change, self.action)

        elif mode is None:
            pass

    def close(self):
        NotImplementedError()