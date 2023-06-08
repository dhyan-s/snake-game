import pygame
import os
from typing import Tuple, Union
from dataclasses import dataclass

from sprites.snake import Snake
from sprites.fruit import Fruit
from .score import Score
from .utils import center_of

@dataclass
class BoundaryLines:
    line_top: pygame.Rect
    line_left: pygame.Rect
    line_right: pygame.Rect
    line_bottom: pygame.Rect
    
    stats_separator: pygame.Rect
    score_separator: pygame.Rect
    highscore_separator: pygame.Rect


class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.snake = Snake(display, 15, 15, outline_width=2)
        self.fruit = Fruit(display, 20, 20)
        
        self.boundary_color: Union[str, Tuple[int, int, int]] = "red"
        self.boundary_thickness: int = 6
        
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
            self.fruit.set_random_pos(
                x_range=(self.boundary_lines.line_left.right, self.boundary_lines.line_right.left),
                y_range=(self.boundary_lines.line_top.bottom, self.boundary_lines.stats_separator.top)
            )
            self.scoreboard.increment_score()
        
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
        
    def render_boundary(self) -> BoundaryLines:
        display_width = self.display.get_width()
        display_height = self.display.get_height()
        
        highscore_separator_x = int(display_width/4)
        score_separator_x = display_width - highscore_separator_x
        
        return BoundaryLines(
            line_top = pygame.draw.rect(self.display, self.boundary_color, [0, 0, display_width, self.boundary_thickness+1]),
            line_left = pygame.draw.rect(self.display, self.boundary_color, [0,0, self.boundary_thickness, display_height]),
            line_right = pygame.draw.rect(self.display, self.boundary_color, [display_width-self.boundary_thickness, 0, self.boundary_thickness, display_height]),
            line_bottom = pygame.draw.rect(self.display, self.boundary_color, [0, display_height-self.boundary_thickness, display_width, self.boundary_thickness]),
            stats_separator = pygame.draw.rect(self.display, self.boundary_color, [0, display_height-65, display_width, self.boundary_thickness]),
            score_separator = pygame.draw.rect(self.display, self.boundary_color, [score_separator_x, display_height-65, self.boundary_thickness, 65]),
            highscore_separator = pygame.draw.rect(self.display, self.boundary_color, [highscore_separator_x, display_height-65, self.boundary_thickness, 65])
        )

    
    def render(self) -> None:
        self.boundary_lines = self.render_boundary()
        self.point()
        self.snake.render()
        self.fruit.render()
        self.scoreboard.render(
            score_coords = center_of(
                (self.boundary_lines.score_separator.right, self.boundary_lines.line_right.left),
                (self.boundary_lines.stats_separator.bottom, self.boundary_lines.line_bottom.top)
            ),
            highscore_coords = center_of(
                (self.boundary_lines.line_left.right, self.boundary_lines.highscore_separator.left),
                (self.boundary_lines.stats_separator.bottom, self.boundary_lines.line_bottom.top)
            )
        )
        