import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from tetris_custom_env import TetrisEnv

def build_model(actions, states):
    model = Sequential()
    model.add(Flatten(input_shape=(1,7)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    # model.compile(optimizer='adam', loss='mse')
    return model

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=20000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, target_model_update=1e-2)
    return dqn

def main():
    load_filepath = "agent_1.hdf5"
    save_filepath = "agent_2.hdf5"
    env = TetrisEnv()

    actions = env.action_space.n
    states = env.observation_space.shape
    model = build_model(actions, states)

    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    dqn.load_weights(load_filepath)
    dqn.fit(env, nb_steps=600000, log_interval=10000, visualize=False, verbose=1)

    dqn.save_weights(save_filepath, overwrite=True)
    # dqn.load_weights(filepath)
 
    # scores = dqn.test(env, nb_episodes=10, visualize=False)
    # print(np.mean(scores.history['episode_reward']))

main()