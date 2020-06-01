import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from treasure import TreasureHunt

class CustomEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = TreasureHunt()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]), np.array([[10, 2], [10, 2], [10, 2], [10, 2], [10, 2], [10, 2], [10, 2], [10, 2]]), dtype=np.array([int, int]))
        self.viewable = True
        self.memory= []

    def step(self, action_x, action_y):
        self.game.action(action_x, action_y)
        obs = self.game.observe()
        reward = self.game.evaluate()
        end = self.game.end()
        return obs, reward, end, {}

    def reset(self):
        del self.game
        self.game = TreasureHunt()
        obs = self.game.observe()
        return obs

    def render(self, mode='human', close=False):
        if self.viewable:
            self.game.view()

    def set_view(self, val):
        self.viewable = val

    # def save_memory(self, file):
    #     np.save(file, self.memory)
    #     print(file + " saved")

    # def remember(self, state, action, reward, next_state, done):
    #     self.memory.append((state, action, reward, next_state, done))