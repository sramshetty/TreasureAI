import gym
import treasure_hunt
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

from collections import deque

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class DQN:
    def __init__(self, env):
        self.env     = env
        self.memory  = deque(maxlen=2000)
        
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model        = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model   = Sequential()
        
        state_shape  = self.env.observation_space.shape

        model.add(Dense(8, input_dim=state_shape[0], activation="relu"))
        model.add(Dense(100, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))

        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))

        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size: 
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:

            state, action, reward, new_state, done = sample
            
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

def simulate(env, gamma, epsilon, num_trials, trial_length, diff):
    dqn_agent = DQN(env=env)
    steps = []
    total_reward = 0
    env.set_view(True)
    env.set_difficulty(diff)
    for trial in range(num_trials):
        cur_state = np.array(env.reset()).reshape(1, 8)

        total_reward = 0
        for step in range(trial_length):
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = env.step(action)

            total_reward += reward

            new_state = np.array(new_state).reshape(1, 8)
            dqn_agent.remember(cur_state, action, reward, new_state, done) #same as environment's store function
            
            dqn_agent.replay()       # internally iterates default (prediction) model
            dqn_agent.target_train() # iterates target model

            cur_state = new_state
            env.render()
            if done or step >= trial_length-1:
                print("Episode %d finished after %i time steps with total reward = %f."
                      % (trial, step, total_reward))
                break
        if total_reward < 5000:
            print("Failed to complete in trial {}".format(trial))
        elif total_reward > 0:
            print("Failed to complete in trial {}".format(trial))
            dqn_agent.save_model("trial-{}.model".format(trial))
        else:
            print("Completed in {} trials".format(trial))
            dqn_agent.save_model("success.model")
            break

if __name__ == "__main__":
    env     = gym.make("TreasureHunt-v0")
    gamma   = 0.9
    epsilon = .95

    trials  = 1000
    trial_len = 1000

    diff = input("Difficulty (simple, easy, medium, or full): ")

    simulate(env, gamma, epsilon, trials, trial_len, diff)