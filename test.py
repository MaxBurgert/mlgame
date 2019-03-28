import gym
import gym_block_world

env = gym.make('block_world-v0')
for i_episode in range(1):
    observation = env.reset()
    for t in range(20):
        env.render()
        # print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            break
env.close()
