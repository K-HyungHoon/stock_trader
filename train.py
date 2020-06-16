import os
import argparse
from tqdm import tqdm
from lib.env import Kospi200_Env
from lib.utils import get_data, save_pkl
from lib.agents.PG import PGAgent


def main(args):
    # get utils
    datas, changes, code_table, indices_mv = get_data(args.data_path)
    num_company, period, num_feature = datas.shape

    # parameter
    state_shape = (num_company, args.window_size, num_feature)
    action_shape = num_company

    agent = PGAgent(state_shape,
                    action_shape,
                    load_path=None)

    # env
    env = Kospi200_Env(datas,
                       changes,
                       code_table,
                       indices_mv,
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

            env.render(mode='print')
            state = next_state

        total_reward_log.append(total_reward)

        print(f"\n + EPISODE: [{args.num_episode} / {e}] \n"
              f"   + TOTAL REWARD : {total_reward}")

    save_pkl(total_reward_log, os.path.join(args.log_path, f"{num_feature}f"
                                                           f"_{args.window_size}w"
                                                           f"_{args.output}"
                                                           f"_reward.pkl"))

    agent.model.save_weights(os.path.join(args.checkpoint, f"{num_feature}f"
                                                           f"_{args.window_size}w"
                                                           f"_{args.output}.h5"))


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--num_episode', type=int, default=500)
    parser.add_argument('--window_size', type=int, default=15)
    parser.add_argument('--data_path', type=str, default="./data")
    parser.add_argument('--log_path', type=str, default="./log")
    parser.add_argument('--load_path', type=str, default=None)
    parser.add_argument('--checkpoint', type=str, default="./checkpoint")
    args = parser.parse_args()

    # log
    if not os.path.exists(args.log_path):
        os.mkdir(args.log_path)

    if not os.path.exists(args.checkpoint):
        os.mkdir(args.checkpoint)

    main(args)
