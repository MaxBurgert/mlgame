from gym.envs.registration import register

register(
    id='block_world-v0',
    entry_point='gym_block_world.envs:BlockWorldEnv',
)