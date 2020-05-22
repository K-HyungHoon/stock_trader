import numpy as np
from lib.env import Kospi200_Env

data_path = './kospi200.npy'

samples = np.load(data_path)

env = Kospi200_Env(samples)

print(env.action_space)
print(env.observation_space)

# for _ in range(1000):
    # state = env.step(action)
    # action = Network(state)
