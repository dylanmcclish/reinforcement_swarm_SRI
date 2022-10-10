import pygame

# spread randomly throughout environment, collision will be -10

class Obstacle:
    def __init__(self, width, height, x, y, screen):
        self.width = width
        self.height = height
        self.color = (255,0,0)
        self.x = x
        self.y = y
        self.screen = screen
        self.draw()

    def draw(self):
        self.rect = pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.width,self.height))
