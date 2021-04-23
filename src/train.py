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
    model.add(Flatten(input_shape=(1,20,10)))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
            nb_actions=actions, nb_steps_warmup=100, target_model_update=1e-2)
    return dqn

def main():
    env = TetrisEnv()

    actions = env.action_space.n
    states = env.observation_space.shape
    print(states)
    model = build_model(actions, states)
    print(model.summary())

    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)

    scores = dqn.test(env, nb_episodes=500, visualize=False)
    print(np.mean(scores.history['episode_reward']))

main()