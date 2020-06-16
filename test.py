import numpy as np
import argparse
from lib.utils import get_data
from lib.agents.PG import PGAgent


def main(args):
    # get utils
    datas, changes, code_table, indices_mv = get_data(args.data_path)
    num_company, period, num_feature = datas.shape

    # parameter
    state_shape = (num_company, args.window_size, num_feature)
    action_shape = num_company

    code_table = list(code_table.items())

    agent = PGAgent(state_shape,
                    action_shape,
                    load_path=args.load_path)

    total_reward = 0
    pos_count = 0
    neg_count = 0

    for p in range(period - args.window_size + 1):
        obs = datas[:, p: p + args.window_size]
        obs = np.expand_dims(obs, axis=0)

        action = agent.get_action(obs)
        one_hot_action = np.zeros_like(action)
        prop_action = np.random.choice(range(num_company), 1, p=action, replace=False)
        for p in prop_action:
            one_hot_action[p] = 1

        dict_actions = {i: r for i, r in enumerate(action)}

        sorted_dict_actions = sorted(dict_actions.items(),
                                     reverse=True,
                                     key=lambda item: item[1])

        for i, a in enumerate(sorted_dict_actions[:1]):
            print(f"TOP {i + 1} [{code_table[a[0]]}]")

    print(f"TOTAL REWARD : {total_reward}")
    print(f"POS : {pos_count}")
    print(f"NEG : {neg_count}")


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--window_size', type=int, default=15)
    parser.add_argument('--data_path', type=str, default="./data")
    parser.add_argument('--load_path', type=str, default="./checkpoint/4f_15w_001_norm.h5")
    args = parser.parse_args()

    main(args)
