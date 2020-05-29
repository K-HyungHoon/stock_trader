import seaborn
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from lib.data import get_data

datas, changes, labels = get_data('../data/KOSPI200')
plt.bar()


class Confusion:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 7))

        _, self.ax = plt.subplots(1)

        plt.show(block=False)

    def _render_confusion(self, change, action):
        self.ax.clear()

        action = np.where(action > 0, 1, 0)
        change = np.where(change > 0, 1, 0)

        cm = confusion_matrix(change, action)

        df = pd.DataFrame(cm, index=['DOWN', 'UP'], columns=['DOWN', 'UP'])

        plt.figure(figsize=(10, 7))
        self.ax = seaborn.heatmap(df, annot=True, annot_kws={"size": 16}, cmap='Blues', fmt="d")

    def render(self, change, action):
        self._render_confusion(change, action)

        plt.pause(0.001)