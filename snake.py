import pygame
from pygame.sprite import Sprite

class Snake(Sprite):

    def __init__(self, s_game, cell):
        super().__init__()
        self.screen = s_game.screen
        self.settings = s_game.settings
        self.color = self.settings.segment_color
        self.x_size = self.settings.cellx_size - 5
        self.y_size = self.settings.celly_size - 5
        self.directions = 'up'

        self.segment = pygame.Rect(0,0, self.x_size, self.y_size)
        self.segment.center = cell.center

    

    def update(self, direction):
        match direction:
            case 'up': self.segment.y -= 50
            case 'down': self.segment.y += 50
            case 'left': self.segment.x -= 50
            case 'right': self.segment.x += 50
    
    def draw_segment(self):
        pygame.draw.rect(self.screen, self.color, self.segment)


class SnakeHead(Snake):

    def __init__(self, s_game, cell):
        super().__init__(s_game,cell)


class SnakeBody(Snake):
    
    def __init__(self, s_game, cell):
        super().__init__(s_game,cell)
