import os
import gym
from gym import spaces


class Kospi200_Env(gym.Env):
    def __init__(self, root_path, period):
        super(Kospi200_Env, self).__init__()

        self.company_list = [os.path.join(root_path, path) for path in os.listdir(root_path)]
        self.period = period

        self.action_space = spaces.Box(0, 100, shape=(len(self.company_list)))
        self.observation_space = spaces.Box(0, 100, shape=(None, period))

    def step(self, action):
        NotImplementedError()

    def reset(self):
        NotImplementedError()

    def render(self, mode='human'):
        NotImplementedError()

    def close(self):
        NotImplementedError()