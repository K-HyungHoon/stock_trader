import tensorflow as tf
import argparse
import matplotlib.pyplot as plt
from tqdm import tqdm
from lib.env import Kospi200_Env
from lib.utils import get_data, download
from lib.agents import A2CAgent


def main(args):
    # get utils
    datas, changes, labels, indices = get_data(args.path)
    num_company, period, num_feature = datas.shape

    # parameter
    state_shape = (num_company, args.window_size, num_feature)
    action_shape = num_company

    agent = A2CAgent(state_shape,
                     action_shape)

    # env
    env = Kospi200_Env(datas, changes, labels, indices, window_size=args.window_size)

    # log
    total_reward_log = []

    # train
    for e in tqdm(range(args.num_episode), total=args.num_episode):
        state = env.reset()

        total_reward = 0

        while True:
            action = agent.get_action(state)

            next_state, reward, done = env.step(action)

            env.render(mode='plot')
            total_reward += reward

            agent.train_model(state, action, reward, next_state, done)

            if done:
                break

            state = next_state

        total_reward_log.append(total_reward)

        print(f"\n + EPISODE: [{args.num_episode} / {e}] \n"
              f"   + REWARD : {total_reward}")

    plt.plot(total_reward_log)
    plt.show()


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_episode', type=int, default=1000)
    parser.add_argument('--window_size', type=int, default=10)
    parser.add_argument('--path', type=str, default="./data")
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()

    if args.download:
        print("Data Download...")
        download(args.path)
    else:
        print("Market Start")
        main(args)