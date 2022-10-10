from pickle import NEWOBJ_EX
import pygame

class Robot:
    def __init__(self, screen, x, y):
        # same dimensions for all robots
        self.width, self.height = 20, 20
        self.color = (0,0,255)
        self.screen = screen
        self.x = x
        self.y = y
        self.draw()


    def draw(self):
        self.rect = pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.width,self.height))
    
