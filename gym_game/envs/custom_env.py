import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from gym_game.envs.game_file import GameFile

class CustomEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = GameFile()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(np.array([]), np.array([]), dtype=np.int)
        self.memory= []

    def step(self, action):
        self.game.action(action)
        obs = self.game.observe()
        reward = self.game.evaluate()
        end = self.game.end()
        return obs, reward, end, {}

    def reset(self):
        del self.game
        self.game = GameFile()
        obs = self.game.observe()
        return obs

    def render(self, mode='human'):
        self.game.view()

    def close(self):
        print("close")

    # def set_view(self, flag):
    #     self.is_view = flag

    # def save_memory(self, file):
    #     np.save(file, self.memory)
    #     print(file + " saved")

    # def remember(self, state, action, reward, next_state, done):
    #     self.memory.append((state, action, reward, next_state, done))