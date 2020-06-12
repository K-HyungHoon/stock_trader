import tensorflow as tf
import datetime
import argparse
import matplotlib.pyplot as plt
from tqdm import tqdm
from lib.env import Kospi200_Env
from lib.utils import get_data, download
from lib.agents import PGAgent


def main(args):
    # get utils
    datas, changes, code_table, _ = get_data(args.path)
    num_company, period, num_feature = datas.shape

    # parameter
    state_shape = (num_company, args.window_size, num_feature)
    action_shape = num_company

    agent = PGAgent(state_shape,
                    action_shape)

    # env
    env = Kospi200_Env(datas,
                       changes,
                       code_table,
                       window_size=args.window_size)

    # log
    total_reward_log = []

    # train
    for e in tqdm(range(args.num_episode), total=args.num_episode):
        state = env.reset()

        total_reward = 0

        while True:
            action = agent.get_action(state)

            next_state, rewards, done = env.step(action)

            agent.memorize(state, action, rewards)

            total_reward += rewards

            if done:
                agent.learn()
                break

            # env.render(mode='print')
            state = next_state

        total_reward_log.append(sum(total_reward))

        print(f"\n + EPISODE: [{args.num_episode} / {e}] \n"
              f"   + TOTAL REWARD : {sum(total_reward)}")

    plt.plot(total_reward_log)
    plt.show()


if __name__ == "__main__":
    today = datetime.datetime.now().strftime('%Y%m%d')

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_episode', type=int, default=1000)
    parser.add_argument('--window_size', type=int, default=10)
    parser.add_argument('--path', type=str, default="./data")
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--start_date', type=str, default=today)
    parser.add_argument('--end_date', type=str, default=today)
    args = parser.parse_args()

    if args.download:
        print("Data Download...")
        download(args.path, args.start_date, args.end_date, args.window_size)
    else:
        print("Market Start")
        main(args)
