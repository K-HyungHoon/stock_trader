import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense


class PG:
    def __init__(self,
                 input_shape,
                 optimizer,
                 loss):

        self.memory_reset()

        self.model = self.build(input_shape)
        self.model.compile(optimizer=optimizer,
                           loss=loss)

    @staticmethod
    def build(input_shape):
        model = tf.keras.Sequential()
        model.add(Conv2D(128, kernel_size=(1, 3), strides=1, activation="relu", input_shape=input_shape))
        model.add(MaxPool2D(pool_size=(1, 2)))
        model.add(Conv2D(64, kernel_size=(1, 4), strides=1, activation="relu"))
        model.add(Conv2D(1, kernel_size=(1, 1), activation="relu"))
        model.add(Flatten())
        model.add(Dense(200, activation="sigmoid"))
        model.build()

        return model

    def summary(self):
        self.model.summary()

    def get_action(self, state):
        action = self.model.predict(state, batch_size=1).flatten()

        return action

    def learn(self):
        state = np.vstack(self.state_memory)
        reward = np.vstack(self.reward_memory)

        loss = self.model.train_on_batch(state,
                                         reward)

        self.memory_reset()

        return loss

    def memory_reset(self):
        self.state_memory = []
        self.reward_memory = []

    def memorize(self, state, reward):
        self.state_memory.append(state)
        self.reward_memory.append(reward)
