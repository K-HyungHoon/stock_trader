import os
import tensorflow as tf
import numpy as np
import argparse
from lib.env import Kospi200_Env
from lib.data import get_data
from lib.agent.PG import PG
# parser
parser = argparse.ArgumentParser()
parser.add_argument('--num_episode', type=int, default=1000)
parser.add_argument('--window_size', type=int, default=10)
parser.add_argument('--path', type=str, default="data/KOSPI200")
args = parser.parse_args()

# get data
# 'CO', 'HO', 'LO', 'OO', '대비율'
datas, changes, labels = get_data(args.path)

num_company, period, num_feature = datas.shape

# parameter
input_shape = (num_company, args.window_size, num_feature)

optimizer = tf.keras.optimizers.Adam()
loss = 'binary_crossentropy'

# agent
agent = PG(input_shape, optimizer, loss)
agent.summary()

# env
env = Kospi200_Env(datas, labels, window_size=args.window_size)

# train
for e in range(args.num_episode):
    state = env.reset()
    total_reward = 0
    while True:
        env.render()

        action = agent.get_action(state)
        next_state, reward, done = env.step(action)

        loss = agent.learn(state, reward)
        total_reward += reward

        if done:
            break

        state = next_state