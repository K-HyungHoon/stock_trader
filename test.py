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

    print(code_table)

    agent = PGAgent(state_shape,
                    action_shape,
                    output=args.output,
                    load_path=args.load_path)

    obs = datas[:, -args.window_size-1:-1]

    print(obs)

    obs = np.expand_dims(obs, axis=0)

    action = agent.get_action(obs)

    dict_actions = {i: r for i, r in enumerate(action)}

    sorted_dict_actions = sorted(dict_actions.items(),
                                 reverse=True,
                                 key=lambda item: item[1])

    for i, a in enumerate(sorted_dict_actions[:5]):
        print(f"TOP {i + 1} [{code_table[a[0]]}]")


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--window_size', type=int, default=30)
    parser.add_argument('--data_path', type=str, default="./data")
    parser.add_argument('--load_path', type=str, default="./checkpoint/4f_30w_0001_softmax.h5")
    parser.add_argument('--output', type=str, default="softmax", help="[tanh | sigmoid | softmax]")
    args = parser.parse_args()

    print(f"PG {args.output} Start")

    main(args)
