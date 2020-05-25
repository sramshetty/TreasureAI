from gym.envs.registration import register

register(
    id='game-v0',
    entry_point='gym_game.envs:CustomEnv',
    max_episode_steps = 5000,
)
register(
    id='game-file-v0',
    entry_point='gym_foo.envs:GameFile',
)