import numpy as np
import matplotlib.pyplot as plt
from collections import deque


class Plot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.memory_size = 10
        self.reward_memory = deque(maxlen=self.memory_size)
        self.total_reward_memory = deque(maxlen=self.memory_size)

    def _render_plot(self):
        self.ax.clear()
        self.ax.plot(self.reward_memory)
        self.ax.set_xticks(np.arange(self.memory_size))
        self.ax.set_yticks([-0.1, 0, 0.1])
        self.ax.set_yticklabels([])

    def render(self, reward):
        self.reward_memory.append(reward)

        if len(self.reward_memory) == self.memory_size:
            self._render_plot()
            plt.pause(0.05)


# class Confusion:
#     def __init__(self):
#         self.fig, self.ax = plt.subplots()
#         self.label = ['DOWN', 'UP']
#
#     def _render_confusion(self, change, action):
#         self.ax.clear()
#
#         action = np.where(action > 0.5, 1, 0)
#         change = np.where(change > 0, 1, 0)
#
#         cm = confusion_matrix(change, action)
#
#         self.ax.imshow(cm, cmap='Blues')
#         self.ax.set_xticks(np.arange(len(self.label)))
#         self.ax.set_yticks(np.arange(len(self.label)))
#
#         self.ax.set_xticklabels(self.label)
#         self.ax.set_yticklabels(self.label)
#
#         # 전부 맞을때
#         if len(cm) == 1:
#             if action[0] == 0:
#                 cm = np.array([[len(action), 0], [0, 0]])
#             else:
#                 cm = np.array([[0, 0], [len(action), 0]])
#
#         for i in range(len(self.label)):
#             for j in range(len(self.label)):
#                 self.ax.text(j, i, cm[i, j], fontsize=15, ha="center", va="center", color="yellow")
#
#     def render(self, change, action):
#         self._render_confusion(change, action)
#         plt.pause(0.05)