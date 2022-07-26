import pygame
from pygame.sprite import Sprite

class Snake(Sprite):
    #Class represent snake segment 
    
    def __init__(self, s_game, cell, direction = 'up', next_segment = None):
        super().__init__()
        self.screen = s_game.screen
        self.settings = s_game.settings
        self.color = self.settings.segment_color
        self.x_size, self.y_size = self.settings.snake_segment_size
        
        self.direction = direction

        self.segment = pygame.Rect(0,0, self.x_size, self.y_size)
        self.segment.center = cell.center

        self.next_segment = next_segment
    

    def update(self):
        match self.direction:
            case 'up': self.segment.y -= self.settings.celly_size
            case 'down': self.segment.y += self.settings.celly_size
            case 'left': self.segment.x -= self.settings.cellx_size
            case 'right': self.segment.x += self.settings.cellx_size
    
    def draw_segment(self):
        pygame.draw.rect(self.screen, self.color, self.segment)


class SnakeHead(Snake):
    #Subclass for snake head

    def __init__(self, s_game, cell):
        super().__init__(s_game,cell)
