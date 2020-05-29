import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten


class PG:
    def __init__(self,
                 input_shape,
                 optimizer,
                 loss,
                 lr=0.0001):

        self.lr = lr

        self.model = self.build(input_shape)
        self.model.compile(optimizer=optimizer,
                           loss=loss)

    @staticmethod
    def build(input_shape):
        model = tf.keras.Sequential()
        model.add(Conv2D(128, kernel_size=(1, 3), strides=1, activation="relu", input_shape=input_shape))
        model.add(MaxPool2D(pool_size=(1, 2)))
        model.add(Conv2D(64, kernel_size=(1, 4), strides=1, activation="relu"))
        model.add(Conv2D(1, kernel_size=1, activation="sigmoid"))
        model.add(Flatten())
        model.build()

        return model

    def summary(self):
        self.model.summary()

    def get_action(self, state):
        output = self.model(state)

        output = output.numpy()

        # output[output >= 0.5] = 1
        # output[output < 0.5] = 0

        return output

    def learn(self, state, reward):
        loss = self.model.train_on_batch(state, reward)

        return loss
