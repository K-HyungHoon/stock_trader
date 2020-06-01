import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense
from keras.optimizers import Adam
from keras import backend as K

class PG:
    def __init__(self,
                 state_shape,
                 action_shape):
        self.memory_reset()
        self.state_shape = state_shape
        self.action_shape = action_shape

        self.learning_rate = 0.01

        self.model = self.build_model()
        self.optimizer = self.build_optimizer()

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(128, kernel_size=(1, 3), strides=1, activation="relu", input_shape=self.state_shape))
        model.add(MaxPool2D(pool_size=(1, 2)))
        model.add(Conv2D(64, kernel_size=(1, 4), strides=1, activation="relu"))
        model.add(Conv2D(1, kernel_size=(1, 1), activation="relu"))
        model.add(Flatten())
        model.add(Dense(100, activation="relu"))
        model.add(Dense(200, activation="sigmoid"))
        model.build()

        return model

    def build_optimizer(self):
        action = K.placeholder(shape=[None, self.action_shape])
        rewards = K.placeholder(shape=[None, ])

        action_prob = K.sum(action * self.model.output, axis=1)
        cross_entropy = K.log(action_prob) * rewards
        loss = -K.sum(cross_entropy)

        optimizer = Adam(lr=self.learning_rate)
        updates = optimizer.get_updates(self.model.trainable_weights, [], loss)
        train = K.function([self.model.input, action, rewards], [], updates=updates)

        return train

    def summary(self):
        self.model.summary()

    def get_action(self, state):
        action = self.model.predict(state, batch_size=1).flatten()

        return action

    def learn(self):
        states = np.vstack(self.state_memory)
        rewards = np.vstack(self.reward_memory)
        actions = np.vstack(self.action_memory)

        rewards = (rewards - np.mean(rewards)) / (np.std(rewards) + 1e-5)
        rewards /= np.std(rewards)

        rewards = rewards.sum(axis=1)

        self.optimizer([states, actions, rewards])
        self.memory_reset()

    def memory_reset(self):
        self.state_memory = []
        self.reward_memory = []
        self.action_memory = []

    def memorize(self, state, action, reward):
        self.state_memory.append(state)
        self.reward_memory.append(reward)
        self.action_memory.append(action)
