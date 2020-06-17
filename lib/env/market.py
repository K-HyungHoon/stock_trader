import gym
import numpy as np
from lib.env.render import Plot


class Kospi200_Env(gym.Env):
    def __init__(self, history, changes, code_table, indices_mv, window_size=5):
        super(Kospi200_Env, self).__init__()
        self.plot_live = Plot()

        self.history = history
        self.changes = changes
        self.indices_mv = indices_mv

        self.code_table = list(code_table.items())
        self.window_size = window_size

        self.num_company = self.history.shape[0]
        self.period = self.history.shape[1]
        self.num_feature = self.history.shape[2]

        print(f'period : {self.period} | '
              f'num_company : {self.num_company} | '
              f'num_feature : {self.num_feature} | ')

    def step(self, action):
        """
        :param  action : softmax output (포트폴리오 비중)
        :return        : state, reward (포트폴리오 비중 * 대비율), done
        """
        change = self.changes[self.current_step + self.window_size]

        self.action = action
        self.rewards = sum(change * action)

        if self.current_step >= self.period - self.window_size - 1:
            self.done = True

        self.current_step += 1

        return self._get_state(), self.rewards, self.done

    def reset(self):
        self.current_step = 0
        self.rewards = []
        self.done = False

        return self._get_state()

    def render(self, mode=None):
        if mode == 'plot':
            reward = sum(self.rewards)

            self.plot_live.render(reward)

        elif mode == 'print':
            self._render_print()

        elif mode is None:
            pass

    def _get_state(self):
        obs = self.history[:, self.current_step: self.current_step + self.window_size]
        return np.expand_dims(obs, axis=0)

    def _render_print(self, view=1):
        dict_actions = {i: a for i, a in enumerate(self.action)}
        dict_changes = {i: c for i, c in enumerate(self.changes[self.current_step + self.window_size - 1])}

        sorted_dict_actions = sorted(dict_actions.items(),
                                     reverse=True,
                                     key=lambda item: item[1])

        sorted_dict_changes = sorted(dict_changes.items(),
                                     reverse=True,
                                     key=lambda item: item[1])

        # Predict Top@10
        for i, (a, c) in enumerate(zip(sorted_dict_actions[:view], sorted_dict_changes[:view])):
            print(f"TOP {i + 1} [{self.code_table[a[0]]} / {self.rewards} || {self.code_table[c[0]]} / {c[1]}]")

        print(f"==========================================================================")