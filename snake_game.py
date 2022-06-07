import sys
import pygame
from settings import Settings
from snake import Snake, SnakeHead
from pygame import time

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.game_area = []

        self.screen = pygame.display.set_mode(self.settings.screen_size)

        pygame.display.set_caption("Snake Game")

        self.snake = []

        self._generate_game_area()
        self._set_screen()
        self._generate_snake()


    def run_game(self):
        while True:
            self._check_directions()
            self._check_events()
            self._update_segment()
            if self._check_game_over():
                sys.exit()
            self._update_screen()
            time.wait(300)

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT and self.snake[0].direction != 'left':
            self.snake[0].direction = 'right'
        elif event.key == pygame.K_LEFT and self.snake[0].direction != 'right':
            self.snake[0].direction = 'left'
        elif event.key == pygame.K_UP and self.snake[0].direction != 'down':
            self.snake[0].direction = 'up'
        elif event.key == pygame.K_DOWN and self.snake[0].direction != 'up':
            self.snake[0].direction = 'down'
        elif event.key == pygame.K_q:
            sys.exit()

    def _update_segment(self):
        
        for segment in self.snake:
                segment.update()
        

    def _check_directions(self):
        for segment in reversed(self.snake):
            if type(segment) !=SnakeHead:
                segment.direction = segment.next_segment.direction

    def _check_game_over(self):
        if self.screen.get_at(self.snake[0].segment.center)[0] == 0: return True
        if self.snake[0].segment.x < 0 or self.snake[0].segment.x > 800: return True
        if self.snake[0].segment.y < 0 or self.snake[0].segment.y > 800: return True

    def _update_screen(self):
        self._set_screen()
        for segment in self.snake:
            segment.draw_segment()
        pygame.display.flip()


    def _generate_game_area(self):
        self.game_area = [[pygame.Rect(x,y,self.settings.cellx_size,self.settings.celly_size) for x in range(0,801)[::self.settings.cellx_size]] 
                                                                                                for y in range(0,801)[::self.settings.celly_size]]

    def _generate_segment(self):
        x,y = self.snake[-1].segment.center

        match self.snake[-1].direction:
            case 'up': y += self.settings.celly_size
            case 'down': y -= self.settings.celly_size
            case 'left': x += self.settings.cellx_size
            case 'right': x -= self.settings.cellx_size
        x//=50
        y//=50
        return Snake(self, self.game_area[y][x], self.snake[-1].direction, self.snake[-1])

    def _generate_snake(self):
        head = SnakeHead(self,self.game_area[6][6])
        self.snake.append(head)
        for i in range(5):
            self.snake.append(self._generate_segment())


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