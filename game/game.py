import pygame

from sprites.snake import Snake
from sprites.fruit import Fruit

class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.snake = Snake(display, 15, 15, outline_width=2)
        self.fruit = Fruit(display, 20, 20)
        
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.up()
            elif event.key == pygame.K_DOWN:
                self.snake.down()
            elif event.key == pygame.K_LEFT:
                self.snake.left()
            elif event.key == pygame.K_RIGHT:
                self.snake.right()
            elif event.key == pygame.K_SPACE:
                self.snake.extend()
                self.fruit.set_random_pos()
        
    def render_boundary(self) -> None:
        width = 6
        display_width = self.display.get_width()
        display_height = self.display.get_height()

        pygame.draw.rect(self.display, "red", [0, 0, display_width, width+1])
        pygame.draw.rect(self.display, "red", [0,0, width, display_height])
        pygame.draw.rect(self.display, "red", [0, display_height-width, display_width, width])
        pygame.draw.rect(self.display, "red", [display_width-width, 0, width, display_height])
        
        pygame.draw.rect(self.display, "red", [0, display_height-65, display_width, width])
        score_sep_x = int(display_width/4)
        highscore_sep_x = display_width-score_sep_x
        pygame.draw.rect(self.display, "red", [score_sep_x, display_height-65, width, 65])
        pygame.draw.rect(self.display, "red", [highscore_sep_x, display_height-65, width, 65])
        
    
    def render(self) -> None:
        self.snake.render()
        self.fruit.render()
        self.render_boundary()