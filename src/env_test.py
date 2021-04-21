from tetris_custom_env import TetrisEnv

env = TetrisEnv()
print(env.action_space.sample())

episodes = 10
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score'.format(episode, score))