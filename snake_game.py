import sys
import pygame
from settings import Settings
from snake import Snake, SnakeHead

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.game_area = []

        self.screen = pygame.display.set_mode(self.settings.screen_size)

        pygame.display.set_caption("Snake Game")

        self.snake = pygame.sprite.Group()

        self._generate_game_area()
        self._set_screen()
        self._generate_snake()


    def run_game(self):
        while True:
            self._check_events()
            
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.head.update('right')
        elif event.key == pygame.K_LEFT:
            self.head.update('left')
        elif event.key == pygame.K_UP:
            self.head.update('up')
        elif event.key == pygame.K_DOWN:
            self.head.update('down')
        elif event.key == pygame.K_q:
            sys.exit()
        self._set_screen()

    def _generate_snake(self):
        self.head = SnakeHead(self,self.game_area[6][6])

    def _update_screen(self):
        
        self.head.draw_segment()
        pygame.display.flip()


    def _generate_game_area(self):
        color = True
        self.game_area = [[pygame.Rect(x,y,self.settings.cellx_size,self.settings.celly_size) for x in range(0,801)[::self.settings.cellx_size]] 
                                                                                                for y in range(0,801)[::self.settings.celly_size]]

    def _set_screen(self):
        self.screen.fill(self.settings.bg_color)
        color = True
        for row in self.game_area:
            for cell in row:
                if (color):
                    color = False
                    pygame.draw.rect(self.screen, self.settings.gray_cell_color, cell)
                else:
                    color = True
                    pygame.draw.rect(self.screen, self.settings.white_cell_color, cell)
                
        pygame.display.flip()








if __name__ == '__main__':
    sg = SnakeGame()
    sg.run_game()