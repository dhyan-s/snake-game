import pygame
import os
from typing import Tuple, Union

from sprites.snake import Snake
from sprites.fruit import Fruit
from .score import Score
from .utils import center_of
from .boundary import Boundary


class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.snake = Snake(display, 15, 15, outline_width=2)
        self.fruit = Fruit(display, 20, 20)
        self.boundary = Boundary(display)
        
        self.change_fruit_pos()
        self.snake.start()
        
        self.game_font = pygame.font.Font("assets/fonts/score_font.ttf", 40)
        
        cur_dir = os.path.dirname(__file__)
        self.scoreboard = Score(
            display = self.display,
            score_icon_path = f"{cur_dir}/apple.png",
            highscore_icon_path = f"{cur_dir}/trophy.png",
            font = self.game_font
            )
        
    def point(self) -> None:
        if self.snake.head.colliding_with(self.fruit.rect):
            self.snake.extend()
            self.change_fruit_pos()
            self.scoreboard.increment_score()
            
    def change_fruit_pos(self) -> None:
        self.fruit.set_random_pos(
            x_range=(self.boundary.left_line.right, self.boundary.right_line.left),
            y_range=(self.boundary.top_line.bottom, self.boundary.stats_separator.top)
        )
        
    def check_game_over(self) -> None:
        if self.snake.body.colliding_with(self.snake.head.rect):
            self.snake.stop()
        elif any(self.snake.colliding_with(rect) for rect in [self.boundary.top_line, 
                                                              self.boundary.bottom_line, 
                                                              self.boundary.left_line, 
                                                              self.boundary.right_line, 
                                                              self.boundary.stats_separator]):
            self.snake.stop()
        
    def handle_event(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.snake.up()
        elif event.key == pygame.K_DOWN:
            self.snake.down()
        elif event.key == pygame.K_LEFT:
            self.snake.left()
        elif event.key == pygame.K_RIGHT:
            self.snake.right()
    
    def render(self) -> None:
        self.check_game_over()
        self.point()
        self.snake.render()
        self.fruit.render()
        self.scoreboard.render(
            score_coords = center_of(
                (self.boundary.score_separator.right, self.boundary.right_line.left),
                (self.boundary.stats_separator.bottom, self.boundary.bottom_line.top)
            ),
            highscore_coords = center_of(
                (self.boundary.left_line.right, self.boundary.highscore_separator.left),
                (self.boundary.stats_separator.bottom, self.boundary.bottom_line.top)
            )
        )
        self.boundary.render()