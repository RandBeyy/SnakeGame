import pygame
from pygame.sprite import Sprite

class Snake(Sprite):

    def __init__(self, s_game, cell, direction = 'up', next_segment = None):
        super().__init__()
        self.screen = s_game.screen
        self.settings = s_game.settings
        self.color = self.settings.segment_color
        self.x_size = self.settings.cellx_size - 5
        self.y_size = self.settings.celly_size - 5
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

    def __init__(self, s_game, cell):
        super().__init__(s_game,cell)


class SnakeBody(Snake):
    
    def __init__(self, s_game, cell, next_segment):
        super().__init__(s_game,cell)
