import sys
import pygame
from settings import Settings

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.game_area = []

        self.screen = pygame.display.set_mode(self.settings.screen_size)


    def run_game(self):
        self._generate_game_area()
        self._set_screen()
        while True:
            self._update_screen()
            self._check_events()

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


    def _update_screen(self):
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