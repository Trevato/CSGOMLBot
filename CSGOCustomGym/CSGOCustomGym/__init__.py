from gym.envs.registration import register

register(
    id='CSGO-v0',
    entry_point='CSGOCustomGym.envs:CSGOEnv',
)
