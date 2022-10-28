import torch
import random
import numpy as np
from collections import deque
from swarmAI_v1 import swarmAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot
import helper
from helper import graph

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # parameter to control randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(12,256,4) # hidden size can be adjusted
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    
    def get_state(self, game):
        # state = [danger front, danger right, danger left, danger back, 
        # dir front, dir right, dir left, dir back, 
        # reward front, reward right, reward left, reward back]
        r = game.robot1
        point_l = Point(r.x - 20, r.y)
        point_r = Point(r.x + 20, r.y)
        point_u = Point(r.x, r.y - 20)
        point_d = Point(r.x, r.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # config is always same for robot
        state = [
            # Danger front 
            (game.is_collision(point_u)),

            # Danger right
            (game.is_collision(point_r)),

            # Danger left
            (game.is_collision(point_l)),

            # Danger back
            (game.is_collision(point_d)),


            # Move direction
            dir_u,
            dir_r,
            dir_l,
            dir_d,
            
            # Reward location 
            game.checkpoint.y < r.y,  # food up
            game.checkpoint.x > r.x,  # food right
            game.checkpoint.x < r.x,  # food left
            game.checkpoint.y > r.y  # food down
        ]
        #print(state)
        return np.array(state, dtype=int) # converts bool to int array


    def remember(self, state, action, reward, next_state, done):
        # popleft if MAX_MEMORY is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            #print("training LONG")
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else: 
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #self.memory = deque(maxlen=MAX_MEMORY)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        # does more random moves in beginning
        # self.epsilon = 400 - self.n_games       # highered amount of games until epsilon = 0 
        self.epsilon = 200 - self.n_games   # constant epsilon
        # if self.epsilon < 40:
        #     self.epsilon = 40   # min epsilon
        final_move = [0,0,0,0]
        if random.randint(0,1000) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


    
def train():
    plot_scores = []
    plot_mean_scores = []
    tot_time_and_score = [] # 2D array 
    total_score = 0
    record = 0
    agent = Agent()
    game = swarmAI()
    while agent.n_games<=200:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)
        
        # perform move and get new state

        reward, done, score, times = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory (experience replay) - plot results
            game.reset()
            trial_text = 'Trial ' + str(agent.n_games)
            agent.n_games += 1
            if score == 0 and agent.n_games > 150 and random.random() > 0.75:
                agent.n_games -= 1
            else:
                agent.train_long_memory()

                if score  > record:
                    record = score
                    agent.model.save()
        

                if times:
                    tot_time = sum(times)
                    tot_time_and_score.append([trial_text, tot_time, score])
                else:
                    tot_time_and_score.append([trial_text, 0,0])
                
                print(tot_time_and_score)
                print('Game:', agent.n_games, ', Score:', score, ', Record:', record)

                # plot
                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
    graph(tot_time_and_score)
    print("DONE")







if __name__ == '__main__':
    train()
