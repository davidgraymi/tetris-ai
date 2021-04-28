from tetris_custom_env import TetrisEnv
from time import sleep

env = TetrisEnv()
# print("sample:", env.action_space.sample())

episodes = 10
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0
    i = 0
    while not done:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        # print(n_state)
        if (i % 1) == 0:
            env.render()
            # sleep(0.1)
        score += reward
        i+=1
    # env.render(n_state)
    print('Score:{}'.format(score))
# print('Episode:{} Score:{}'.format(episode, score))