from tetris import Tetris
from dqn_agent import DQNAgent

env = Tetris()
episodes = 10
max_steps = None
epsilon = 0
epsilon_stop_episode = 1500
mem_size = 20000
discount = 0.95
batch_size = 512
epochs = 1
replay_start_size = 2000
n_neurons = [32, 32]
render_delay = None
activations = ['relu', 'relu', 'linear']
filepath = "tetris-nn_4-8.h5"

agent = DQNAgent(env.get_action_space(),
                     n_neurons=n_neurons, activations=activations, epsilon=0,
                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
                     discount=discount, replay_start_size=replay_start_size)

agent.load(filepath)

scores = []

for episode in range(episodes):
    current_state = env.reset()
    done = False
    steps = 0

    # Game
    while not done and (not max_steps or steps < max_steps):
        next_states = env.get_next_states()
        # print(next_states)
        best_state = agent.best_state(next_states.values())
        # print(best_state)
        
        best_action = None
        for action, state in next_states.items():
            if state == best_state:
                best_action = action
                break

        reward, done = env.step(best_action[0], best_action[1], render=True,
                                render_delay=render_delay)
        
        # agent.add_to_memory(current_state, next_states[best_action], reward, done)
        current_state = next_states[best_action]
        steps += 1

    score = env.get_game_score()
    print(score)
    scores.append(score)