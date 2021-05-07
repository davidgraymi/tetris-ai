from dqn_agent import DQNAgent
from tetris import Tetris
from datetime import datetime
from statistics import mean, median
import random
from tqdm import tqdm
import pandas as pd
        

# Run dqn with Tetris
def dqn():
    env = Tetris()
    episodes = 500
    max_steps = None
    epsilon_stop_episode = int(episodes*0.75)
    mem_size = 20000
    discount = 0.95
    batch_size = 512
    epochs = 1
    render_every = 50
    log_every = 25
    replay_start_size = 2000
    train_every = 1
    n_neurons = [32, 32]
    render_delay = None
    activations = ['relu', 'relu', 'linear']
    dqn_num = 3
    filepaths = "tetris-nn_"+str(dqn_num)+"-.h5"
    # filepaths = ["tetris-nn_"+str(dqn_num)+"-"+str(i)+".h5" for i in range(0,10)]
    save = len(filepaths)
    save_every = episodes/save
    log_fp = "log.txt"
    csv_fp = "dqn_"+str(dqn_num)+"_training.csv"
    log = open(log_fp,"a")
    log.write("\ntetris-nn="+str(n_neurons)+"-mem="+str(mem_size)+"-bs="+str(batch_size)+"-e="+str(epochs)+"-"+str(datetime.now().strftime("%Y%m%d-%H%M%S"))+"\n\n")
    log.close()

    agent = DQNAgent(env.get_action_space(),
                     n_neurons=n_neurons, activations=activations,
                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
                     discount=discount, replay_start_size=replay_start_size)

    scores = []

    for episode in tqdm(range(episodes)):
        current_state = env.reset()
        done = False
        steps = 0

        if render_every and episode % render_every == 0:
            render = True
        else:
            render = False

        # Game
        while not done and (not max_steps or steps < max_steps):
            next_states = env.get_next_states()
            best_state = agent.best_state(next_states.values())
            
            best_action = None
            for action, state in next_states.items():
                if state == best_state:
                    best_action = action
                    break

            reward, done = env.step(best_action[0], best_action[1], render=render,
                                    render_delay=render_delay)
            
            agent.add_to_memory(current_state, next_states[best_action], reward, done)
            current_state = next_states[best_action]
            steps += 1

        scores.append(env.get_game_score())

        # Train
        if episode % train_every == 0:
            agent.train(batch_size=batch_size, epochs=epochs)

        # Save
        if (episode+1) % save_every == 0:
            agent.save(filepaths)
            # agent.save(filepaths[save-10])
            save += 1

        # Logs
        if log_every and episode and (episode+1) % log_every == 0:
            avg_score = mean(scores[-log_every:])
            min_score = min(scores[-log_every:])
            max_score = max(scores[-log_every:])

            log = open(log_fp,"a")
            logging = "episode: "+str(episode+1)+", avg_score: "+str(avg_score)+", min_score: "+\
                 str(min_score)+", max_score: "+str(max_score)+"\n"
            log.write(logging)
            log.close()
    
    log = open(log_fp,"a")
    log.write("\n------------------------------------------------------------------------------------------------"+"\n")
    log.close()

    df = pd.DataFrame(scores)
    df.to_csv(csv_fp)


if __name__ == "__main__":
    dqn()
