import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


class Confusion:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.label = ['DOWN', 'UP']

    def _render_confusion(self, change, action):
        self.ax.clear()

        action = np.where(action > 0.5, 1, 0)
        change = np.where(change > 0, 1, 0)

        cm = confusion_matrix(change, action)

        self.ax.imshow(cm)
        self.ax.set_xticks(np.arange(len(self.label)))
        self.ax.set_yticks(np.arange(len(self.label)))

        self.ax.set_xticklabels(self.label)
        self.ax.set_yticklabels(self.label)


        if len(cm) >= 2:
            for i in range(len(self.label)):
                for j in range(len(self.label)):
                    self.ax.text(j, i, cm[i, j], ha="center", va="center", color="w")
        else:
            print(action)
            print(change)
            print(cm)

    def render(self, change, action):
        self._render_confusion(change, action)
        plt.pause(0.05)

