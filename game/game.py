import pygame
from typing import Tuple, Union

from sprites.snake import Snake
from sprites.fruit import Fruit


class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.snake = Snake(display, 15, 15, outline_width=2)
        self.fruit = Fruit(display, 20, 20)
        
        self.boundary_color: Union[str, Tuple[int, int, int]] = "red"
        self.boundary_thickness: int = 6
        
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
        display_width = self.display.get_width()
        display_height = self.display.get_height()

        line_top = pygame.draw.rect(self.display, self.boundary_color, [0, 0, display_width, self.boundary_thickness+1])
        line_left = pygame.draw.rect(self.display, self.boundary_color, [0,0, self.boundary_thickness, display_height])
        line_down = pygame.draw.rect(self.display, self.boundary_color, [0, display_height-self.boundary_thickness, display_width, self.boundary_thickness])
        line_right = pygame.draw.rect(self.display, self.boundary_color, [display_width-self.boundary_thickness, 0, self.boundary_thickness, display_height])
        
        stats_separator = pygame.draw.rect(self.display, self.boundary_color, [0, display_height-65, display_width, self.boundary_thickness])
        
        score_separator_x = int(display_width/4)
        highscore_separator_x = display_width - score_separator_x
        score_separator = pygame.draw.rect(self.display, self.boundary_color, [score_separator_x, display_height-65, self.boundary_thickness, 65])
        highscore_separator = pygame.draw.rect(self.display, self.boundary_color, [highscore_separator_x, display_height-65, self.boundary_thickness, 65])

        
    
    def render(self) -> None:
        self.snake.render()
        self.fruit.render()
        self.render_boundary()