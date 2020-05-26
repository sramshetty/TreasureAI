from gym.envs.registration import register

register(
    id='game-v0',
    entry_point='treasure_hunt.envs:CustomEnv',
    max_episode_steps = 5000,
)
register(
    id='treasure-v0',
    entry_point='treasure_hunt.envs:Treasure',
)