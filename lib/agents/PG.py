import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense
from keras.optimizers import Adam
from keras import backend as K


class PGAgent:
    def __init__(self,
                 state_size,
                 action_size,
                 load_path=None):
        self.memory_reset()
        self.state_size = state_size
        self.action_size = action_size

        self.learning_rate = 0.001

        self.model = self.build_model()
        self.optimizer = self.build_optimizer()

        if load_path is not None:
            self.model.load_weights(load_path)

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(128, kernel_size=(1, 3), strides=1, activation="relu", input_shape=self.state_size))
        model.add(MaxPool2D(pool_size=(1, 2)))
        model.add(Conv2D(64, kernel_size=(1, 4), strides=1, activation="relu"))
        model.add(Conv2D(1, kernel_size=(1, 1), activation="linear"))
        model.add(Flatten())
        model.add(Dense(self.action_size, activation="softmax"))
        model.build()

        model.summary()

        return model

    def build_optimizer(self):
        action = K.placeholder(shape=[None, self.action_size])
        rewards = K.placeholder(shape=[None, ])

        action_prob = K.sum(self.model.output * action, axis=1)
        cross_entropy = K.log(action_prob) * rewards
        loss = -K.sum(cross_entropy)

        optimizer = Adam(lr=self.learning_rate)
        updates = optimizer.get_updates(self.model.trainable_weights, [], loss)
        train = K.function([self.model.input, action, rewards], [], updates=updates)

        return train

    def get_action(self, state):
        action = self.model.predict(state).flatten()

        one_hot_action = np.zeros_like(action)

        prop_action = np.random.choice(range(self.action_size), 1, p=action, replace=False)

        for p in prop_action:
            one_hot_action[p] = 1

        return one_hot_action

    def learn(self):
        states = np.vstack(self.state_memory)
        rewards = np.vstack(self.reward_memory).reshape(-1)
        actions = np.vstack(self.action_memory)

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