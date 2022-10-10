from gettext import dpgettext
import pygame, random
import obstacle, robot, checkpoint
from enum import Enum
from collections import namedtuple
import numpy as np

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

SPEED = 1000


class swarmAI:

    # ENVIRONMENT 1
    # 1 ROBOT, 1 OBSTACLE, 2 CHECKPOINTS

    def __init__(self):
        # init display
        # init pygame
        self.screen_width, self.screen_height = 500, 500
        self.screen = pygame.display.set_mode([self.screen_width,self.screen_height])
        self.clock = pygame.time.Clock()
     
        # init game state
        self.direction = Direction.RIGHT
        self.vel = 2
        
        self.reset()


    def reset(self):
        # robots
        self.robot1 = robot.Robot(self.screen, 30, 30)
        self.robots = [self.robot1]
        self.r_rects = [self.robot1.rect]

        # obstacles (- rewards)
        self.obstacle1 = obstacle.Obstacle(75,75, random.random() * 300 + 100, random.random() * 300 + 100, self.screen)
        self.obstacles = [self.obstacle1]
        self.o_rects = [self.obstacle1.rect]

        # checkpoints (+ rewards)
        self.add_reward()
    
        # reset score
        self.score = 0
        self.frame_iteration = 0

    def add_reward(self):
            new_x, new_y = random.random() * 300 + 100, random.random() * 300 + 100
            new_check = pygame.Rect(new_x,new_y,40,40)
            # prevent overlap between checkpoint and obstacles
            # while any(self.checkpoint.rect.colliderect(t) for t in self.o_rects):
            #     self.checkpoint = checkpoint.Checkpoint(self.screen, random.random() * 300 + 100, random.random() * 300 + 100)   # ensures that position is within frame
            if new_check.collidelist(self.o_rects) != -1 or new_check.collidelist(self.r_rects) != -1:
                self.add_reward()
            
            # draws after confirms rect is valid
            self.checkpoint = checkpoint.Checkpoint(self.screen, new_x, new_y)   # ensures that position is within frame

            
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
        self.obstacles = [self.obstacle1]
        self.o_rects = [self.obstacle1.rect]

        self.frame_iteration += 1
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
        reward = 0
        game_over = False
        if self.is_collision():
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. check reward - place more if reached
        if self.is_reward():
            self.score +=1
            reward = 10
            self.add_reward()


        # 5. update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)
        # 6. return game over andd score
        return reward, game_over, self.score
        
    def is_collision(self, pt=None):
        # test collision - returns true if collision
        # TODO: make code cleaner
        for robot in self.robots:
            if pt is None:  # used to end game
                # walls
                if robot.rect.left <= 0 or robot.rect.right >= self.screen_width or robot.rect.top <= 0 or robot.rect.bottom >= self.screen_height:
                    return True
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
                if pt.x > self.screen_width - 20 or pt.x < 0 or pt.y > self.screen_height - 20 or pt.y < 0:
                    return True
                # obstacles
                for o in self.obstacles:
                    if pt.x == robot.x: # danger y
                        if abs(pt.y - o.y) < 20:    # arbitrary threshold
                            return True
                    if pt.y == robot.y: # danger x
                        if abs(pt.x - o.x) < 20:
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
            print("rewarded")
            return True
        return False


    def update_ui(self):
        self.screen.fill(BLACK)

        self.robot1.draw()
        for obstacle in self.obstacles:
            obstacle.draw()
        self.checkpoint.draw()

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(text, [0,0])
        pygame.display.update()

    def move(self, action):
        # [forward, right, left, backward]
        
        if np.array_equal(action, [1,0,0,0]):
            new_dir = Direction.UP
        elif np.array_equal(action, [0,1,0,0]):
            new_dir = Direction.RIGHT
        elif np.array_equal(action, [0,0,1,0]):
            new_dir = Direction.LEFT
        else:
            new_dir = Direction.DOWN
        

        self.direction = new_dir
        
        if self.direction == Direction.RIGHT:
            self.robot1.x += self.vel
        if self.direction == Direction.LEFT:
            self.robot1.x -= self.vel  
        if self.direction == Direction.DOWN:
            self.robot1.y += self.vel   
        if self.direction == Direction.UP:
            self.robot1.y -= self.vel       


