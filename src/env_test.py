from tetris_custom_env import TetrisEnv

env = TetrisEnv()
# print("sample:", env.action_space.sample())

episodes = 10
# for episode in range(1, episodes+1):
state = env.reset()
done = False
score = 0
i = 0
while i<100:
    action = env.action_space.sample()
    n_state, reward, done, info = env.step(action)
    print(n_state)
    # if (i % 1) == 0:
    #     env.render(n_state)
    score += reward
    i+=1
# env.render(n_state)
print('Episode:{} Score:{}'.format(episode, score))