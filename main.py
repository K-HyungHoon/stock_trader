import os
import tensorflow as tf
import numpy as np
import argparse
from lib.env import Kospi200_Env
from lib.data import get_data
from lib.agent.PG import PG
# parser
parser = argparse.ArgumentParser()
parser.add_argument('--num_episode', type=int, default=1)
parser.add_argument('--window_size', type=int, default=5)
parser.add_argument('--path', type=str, default="data/KOSPI200")
args = parser.parse_args()

# get data
datas, labels = get_data(args.path)

# parameter
input_shape = (datas.shape[1], args.window_size, datas.shape[2])
optimizer = tf.keras.optimizers.Adam()
loss = 'binary_crossentropy'

# agent
agent = PG(input_shape, optimizer, loss)
agent.summary()

# env
env = Kospi200_Env(datas, labels, window_size=args.window_size)

# train
for e in range(args.num_episode):
    # state = np.random.random((1, 200, 10, 5))
    state = env.reset()

    while True:
        env.render(mode='print')

        action = agent.get_action(state)
        next_state, reward = env.step(action)

        loss = agent.learn(state, reward, action)

        print(loss)

        state = next_state

        break