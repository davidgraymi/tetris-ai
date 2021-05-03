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
    # model.add(Flatten(input_shape=(1,20,10)))
    # model.add(Flatten(input_shape=(1,7)))
    # model.add(Flatten(input_shape=(1,4)))
    model.add(Flatten(input_shape=(1,11)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    # model.compile(optimizer='adam', loss='mse')
    return model

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=20000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, target_model_update=1e-2)
    return dqn

def train(env, dqn, lfp, sfp):
    dqn.load_weights(lfp)
    dqn.fit(env, nb_steps=300000, log_interval=10000, visualize=False, verbose=1)
    dqn.save_weights(sfp, overwrite=True)

def test(env, dqn, lfp):
    env.renderer = True
    dqn.load_weights(lfp)
    scores = dqn.test(env, nb_episodes=50, visualize=False)
    print(np.mean(scores.history['episode_reward']))

def main():
    load_filepath = "64n_11s_agent_1.hdf5"
    save_filepath = "64n_11s_agent_2.hdf5"
    env = TetrisEnv()

    actions = env.action_space.n
    states = env.observation_space.shape
    model = build_model(actions, states)

    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    
    # train(env, dqn, load_filepath, save_filepath)

    test(env, dqn, load_filepath)
 
main()