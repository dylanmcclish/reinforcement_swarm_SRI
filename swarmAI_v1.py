from gettext import dpgettext
from re import L
import pygame, random
import obstacle, robot, checkpoint
from enum import Enum
from collections import namedtuple
import numpy as np
import time

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', ['x', 'y'])

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

SPEED = 10000


class swarmAI:

    # ENVIRONMENT 1
    # 1 ROBOT, 1 OBSTACLE, 2 CHECKPOINTS

    def __init__(self):
        # init display
        # init pygame
        self.screen_width, self.screen_height = 1000, 500
        self.screen = pygame.display.set_mode([self.screen_width,self.screen_height])
        self.clock = pygame.time.Clock()
     
        # init game state
        self.direction = Direction.RIGHT
        self.vel = 20
        self.collision_type = ""
        self.reset()


    def reset(self):
        # robots
        
        self.robot1 = robot.Robot(self.screen, 20, 20)
        self.f_robot1 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot2 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot3 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot4 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot5 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot6 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot7 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot8 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)
        self.f_robot9 = robot.Robot(self.screen, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50)


        self.robots = [self.robot1]
        self.r_rects = [self.robot1.rect]

        # obstacles (- rewards)
        self.obstacle1 = obstacle.Obstacle(60,60, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50, self.screen)
        self.obstacle2 = obstacle.Obstacle(60,60, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50, self.screen)
        self.obstacle3 = obstacle.Obstacle(60,60, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50, self.screen)
        # self.obstacle4 = obstacle.Obstacle(60,60, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50, self.screen)
        # self.obstacle5 = obstacle.Obstacle(60,60, random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50, self.screen)
        self.obstacles = [self.obstacle1,self.obstacle2,self.obstacle3]
        self.o_rects = [self.obstacle1.rect,self.obstacle2.rect,self.obstacle3.rect]

        # checkpoints (+ rewards)
        self.add_reward()
    
        # reset score
        self.score = 0
        self.frame_iteration = 0

        # reset time collection
        self.time_elapsed = 0
        self.times = []
        self.old_time = time.time()

    def add_reward(self):
            new_x, new_y = random.random() * (self.screen_width - 100) + 50, random.random() * (self.screen_height - 100) + 50
            new_check = pygame.Rect(new_x,new_y,40,40)
            # prevent overlap between checkpoint and obstacles
            # while any(self.checkpoint.rect.colliderect(t) for t in self.o_rects):
            #     self.checkpoint = checkpoint.Checkpoint(self.screen, random.random() * 300 + 100, random.random() * 300 + 100)   # ensures that position is within frame
            # if new_check.collidelist(self.o_rects) != -1 or new_check.collidelist(self.r_rects) != -1:
            #     self.add_reward()

            for o in self.obstacles:
                if (new_check.colliderect(o)):
                    if new_check.bottom > o.rect.top:
                        overlap = new_check.bottom - o.rect.top
                        new_check.bottom -= overlap
                    if new_check.top < o.rect.bottom:
                        overlap = o.rect.bottom - new_check.top
                        new_check.top += overlap
                    if new_check.right > o.rect.left:
                        overlap = new_check.right - o.rect.left
                        new_check.right -= overlap
                    if new_check.left < o.rect.right:
                        overlap = o.rect.right - new_check.left
                        new_check.left += overlap



            


            # draws after confirms rect is valid
            self.checkpoint = checkpoint.Checkpoint(self.screen, new_check.x, new_check.y)   # ensures that position is within frame

            
            # for o in self.obstacles:
            #     if o.rect.bottom > self.checkpoint.rect.bottom:
            #         overlap = o.rect.bottom - self.checkpoint.rect.bottom
            #         o.rect.bottom -= overlap
            #     if o.rect.top > self.checkpoint.rect.top:
            #         overlap = o.rect.top - self.checkpoint.rect.top
            #         o.rect.top += overlap 
    
    def play_step(self, action):
        # update arrays for is_reward and is_collision - BAD CODE
        self.robots = [self.robot1]
        self.r_rects = [self.robot1.rect]
        
        self.frame_iteration += 1
        self.time_elapsed = 0 # only graph time_elapsed if greater than 0 

        # CHANGE TO RUN A SINGLE EPISODE - LOOP IN MAIN 
        # MAIN WILL HAVE TRAINING OF AGENT???? - DEPENDS ON SNAKE

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 


        # 2. move
        self.move(action)

        # 3. check if game over
        reward = -2
        game_over = False
        multiplier = 1
        if (self.score>0):
            multiplier = self.score

        if self.is_collision() or self.frame_iteration > 1000 * (multiplier):
            game_over = True
            reward = -20
            if self.frame_iteration > 1000 * (multiplier):
                reward = -10
                #print("TIME ELAPSED")
            return reward, game_over, self.score, self.times

        # 4. check reward - place more if reached
        if self.is_reward():
            self.score +=1
            self.time_elapsed = self.get_time()
            self.times.append(self.time_elapsed)
            #print(self.time_elapsed)
            reward = 30
            self.add_reward()


        # 5. update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)
        # 6. return game over andd score
        return reward, game_over, self.score, self.times
        
    def is_collision(self, pt=None):
        # test collision - returns true if collision
        # TODO: make code cleaner
        for robot in self.robots:
            if pt is None:  # used to end game
                # walls
                # if robot.rect.left <= 0 or robot.rect.right >= self.screen_width or robot.rect.top <= 0 or robot.rect.bottom >= self.screen_height:
                #     self.collision_type = "wall"
                #     return True
                # obstacles
                for o in self.obstacles:
                    if pygame.Rect.colliderect(robot.rect,o.rect):
                        return True
                # other robots
                for other_robot in self.robots: # swarm collision
                    if robot != other_robot and pygame.Rect.colliderect(robot.rect,other_robot.rect):
                        return True
            else: # used for danger states
                # walls
                # if pt.x > self.screen_width or pt.x < 0 or pt.y > self.screen_height - 20 or pt.y < 0:
                #     return True
                # obstacles
                for o in self.obstacles:
                    if abs(pt.y - o.y) < 20 and abs(pt.x - o.x):    # arbitrary threshold
                        return True
                # other robots
                for o_robot in self.robots: # swarm collision
                    if robot != o_robot:
                        if pt.x == robot.x: # danger y
                            if abs(pt.y - o_robot.y) < 20:    # arbitrary threshold
                                return True
                        if pt.y == robot.y: # danger x
                            if abs(pt.x - o_robot.x) < 20:
                                return True

        return False # if no other conditions met
                        

    def is_reward(self):
        # test collision w/ reward rect
        if self.checkpoint.rect.collidelist(self.r_rects) != -1:
            return True
        return False


    def update_ui(self):
        self.screen.fill(BLACK)
        self.f_robot1.draw()
        self.f_robot2.draw()
        self.f_robot3.draw()
        self.f_robot4.draw()
        self.f_robot5.draw()
        self.f_robot6.draw()
        self.f_robot7.draw()
        self.f_robot8.draw()
        self.f_robot9.draw()
        for robot in self.robots:
            robot.draw()
            
        for obstacle in self.obstacles:
            obstacle.draw()
        self.checkpoint.draw()

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(text, [0,0])
        pygame.display.update()

    def move(self, action):
        # [forward, right, left, backward]
    # if np.array_equal(action, [1,0,0,0]) and self.robot1.rect.top > 0:
    #             self.direction = Direction.UP
    #         elif np.array_equal(action, [0,1,0,0]) and self.robot1.rect.right < self.screen_width :
    #             self.direction = Direction.RIGHT
    #         elif np.array_equal(action, [0,0,1,0]) and self.robot1.rect.left > 0:
    #             self.direction = Direction.LEFT
    #         elif np.array_equal(action, [0,0,0,1]) and self.robot1.rect.bottom < self.screen_height:
    #             self.direction = Direction.DOWN
        if np.array_equal(action, [1,0,0,0]):
            self.direction = Direction.UP
        elif np.array_equal(action, [0,1,0,0]):
            self.direction = Direction.RIGHT
        elif np.array_equal(action, [0,0,1,0]):
            self.direction = Direction.LEFT
        elif np.array_equal(action, [0,0,0,1]):
            self.direction = Direction.DOWN

        self.vel = 10
        if self.direction == Direction.RIGHT and self.robot1.rect.right >= self.screen_width:
            self.vel = 0
        elif self.direction == Direction.LEFT and self.robot1.rect.left <= 0:
            self.vel = 0
        elif self.direction == Direction.DOWN and self.robot1.rect.bottom >= self.screen_height:
            self.vel = 0
        elif self.direction == Direction.UP and self.robot1.rect.top <= 0:
            self.vel = 0         
        
        if self.direction == Direction.RIGHT:
            self.robot1.x += self.vel
        if self.direction == Direction.LEFT:
            self.robot1.x -= self.vel  
        if self.direction == Direction.DOWN:
            self.robot1.y += self.vel   
        if self.direction == Direction.UP:
            self.robot1.y -= self.vel       

    def get_time(self):
        time_elapsed = time.time() - self.old_time
        self.old_time = time.time()
        return time_elapsed


