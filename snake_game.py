import sys
import pygame
from settings import Settings
from snake import Snake, SnakeHead
from pygame import time
from random import randint, choice

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.game_area = []         #List for game area
        self._generate_game_area()
        self.access_to_change_direction = True

        self.fruit = pygame.Rect((0,0), self.settings.fruit_size)
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        self.score = 0

        self.screen.fill(self.settings.bg_color)

        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.score_text = self.font.render(f'Your score - {self.score}', True, self.settings.black)
        self.rect_score_text = self.score_text.get_rect()
        self.rect_score_text.x,self.rect_score_text.y = (0,0)
        
        pygame.display.set_caption("Snake Game")

        self.snake = []
        
        

    def start_screen(self):
        #Set start screen
        self.screen.fill(self.settings.bg_color)
        
        text1 = self.font.render('Welcome to Snake Game!', True, self.settings.black)
        rect_text1 = text1.get_rect()
        rect_text1.x, rect_text1.y = (250,300)
        text2 = self.font.render("To start press 'space' or 'Q' to quit", True, self.settings.black)
        rect_text2 = text2.get_rect()
        rect_text2.center = rect_text1.center
        rect_text2.y += 100
        
        self.screen.blit(text1, rect_text1)
        self.screen.blit(text2, rect_text2)
        pygame.display.flip()
        #Start game or quit by pressing keys
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.run_game()
                        elif event.key == pygame.K_q:
                            sys.exit

    def run_game(self):
        #Generate game area, snake and fruit
        self.score = 0
        self.snake = []
        self.score_text = self.font.render(f'Your score - {self.score}', True, self.settings.black)

        self._set_screen()
        self._generate_fruit()
        self._generate_snake()

        while True:
            self.access_to_change_direction = True
            self._check_directions()
            self._check_events()
            last_segm_coordinate = self.snake[-1].segment.center
            self._update_segment()
            if self._check_game_over(last_segm_coordinate):
                self._game_over_screen()
            self._check_for_fruit()
            self._update_screen()
            time.wait(self.settings.snake_speed)

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

    
    def _check_keydown_events(self, event):
        #On keydown events snake head will change direction
        if (self.access_to_change_direction):
            if event.key == pygame.K_RIGHT and self.snake[0].direction != 'left':
                self.snake[0].direction = 'right'
                self.access_to_change_direction = False
            elif event.key == pygame.K_LEFT and self.snake[0].direction != 'right':
                self.snake[0].direction = 'left'
                self.access_to_change_direction = False
            elif event.key == pygame.K_UP and self.snake[0].direction != 'down':
                self.snake[0].direction = 'up'
                self.access_to_change_direction = False
            elif event.key == pygame.K_DOWN and self.snake[0].direction != 'up':
                self.snake[0].direction = 'down'
                self.access_to_change_direction = False
            elif event.key == pygame.K_q:
                sys.exit()

    def _update_segment(self):
        #For every snake segment call method to update it's coordinate according to it's direction
        for segment in self.snake:
                segment.update()
        
    def _check_directions(self):
        #Every snake segment except head will change it's direction according to direction of next segment to it in reversed way
        for segment in reversed(self.snake):
            if type(segment) !=SnakeHead:
                segment.direction = segment.next_segment.direction

    def _check_game_over(self, last_segm_cord):
        #If Snake head will touch themself or border of game area - return True to stop the game
        try:
            if self.screen.get_at(self.snake[0].segment.center)[0] == 0 and self.snake[0].segment.center != last_segm_cord: return True
            if self.snake[0].segment.x < 0 or self.snake[0].segment.x > 800: return True
            if self.snake[0].segment.y < 0 or self.snake[0].segment.y > 800: return True
        except:
            return True

    def _check_for_fruit(self):
        if self.snake[0].segment.center == self.fruit.center:
            self.snake.append(self._generate_segment())
            self._generate_fruit()
            self.score +=5
            self.score_text = self.font.render(f'Your score - {self.score}', True, (0,0,0))


    def _update_screen(self):
        #Update snake and fruit postition
        self._set_screen()
        for segment in self.snake:
            segment.draw_segment()                                          #update snake
        pygame.draw.rect(self.screen,self.settings.fruit_color,self.fruit)  #update fruit
        self.screen.blit(self.score_text, self.rect_score_text)             #update score text
        pygame.display.flip()

    def _generate_game_area(self):
        #Generate 2D list of cells that represent the game area
        self.game_area = [[pygame.Rect(x,y,self.settings.cellx_size,self.settings.celly_size) for x in range(0,801)[::self.settings.cellx_size]] 
                                                                                                for y in range(0,801)[::self.settings.celly_size]]

    def _generate_segment(self):
        #Generate Snake segment after last segment and return it
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
        #Generate snake at start
        head = SnakeHead(self,self.game_area[6][6])
        self.snake.append(head)
        for i in range(self.settings.amount_of_segment_at_start - 1):
            self.snake.append(self._generate_segment())

    def _generate_fruit(self):
        #Generate rectangle, that represent fruit
        #First try to find free cell, using random function
        n = 5
        for t in range (n):
            i = randint(0,15)
            j = randint(0,15)
            color = self.screen.get_at(self.game_area[i][j].center)

            if color != (0,0,0,255):
                self.fruit.center = self.game_area[i][j].center
                return 1
        
        #If snake is too big, and it can't find free cell then iterate through the whole list
        slices = (slice(0,15,1), slice(-1,-16,-1))

        for i in range(0,15)[choice(slices)]:
            for j in range(0,15)[choice(slices)]:
                color = self.screen.get_at(self.game_area[i][j].center)

                if color != (0,0,0,255):
                    self.fruit.center = self.game_area[i][j].center
                    return 1


    def _game_over_screen(self):
        #Set start screen
        self.screen.fill((0,0,0))
        
        text1 = self.font.render(f'Your score is {self.score}', True, self.settings.red)
        rect_text1 = text1.get_rect()
        rect_text1.x, rect_text1.y = (300,300)
        text2 = self.font.render("To restart press 'R' or 'Q' to quit", True, self.settings.red)
        rect_text2 = text2.get_rect()
        rect_text2.center = rect_text1.center
        rect_text2.y += 100
        
        self.screen.blit(text1, rect_text1)
        self.screen.blit(text2, rect_text2)
        pygame.display.flip()
        #Start game or quit by pressing keys
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.run_game()
                        elif event.key == pygame.K_q:
                            sys.exit

    def _set_screen(self):
        #Generate game area according to list of cells
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


if __name__ == '__main__':
    sg = SnakeGame()
    sg.start_screen()