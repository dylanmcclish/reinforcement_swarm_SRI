import pygame

class Robot:
    def __init__(self, screen, x, y):
        # same dimensions for all robots
        self.width, self.height = 20, 20
        self.screen = screen
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(self.screen, (255,0,0), (self.x,self.y,self.width,self.height))


    def draw(self):
        self.rect = pygame.draw.rect(self.screen, (255,0,0), (self.x,self.y,self.width,self.height))
    
        