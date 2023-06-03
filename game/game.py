import pygame
import os
from typing import Tuple, Union
from dataclasses import dataclass

from sprites.snake import Snake
from sprites.fruit import Fruit

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
        
        self.score = 0
        self.high_score = 0
        
        cur_dir = os.path.dirname(__file__)
        self.trophy_icon = pygame.image.load(f"{cur_dir}/trophy.png").convert_alpha()
        self.trophy_icon = pygame.transform.scale(self.trophy_icon, (35, 35))
        
        self.apple_icon = pygame.image.load(f"{cur_dir}/apple.png").convert_alpha()
        self.apple_icon = pygame.transform.scale(self.apple_icon, (40, 40))
        
        self.game_font = pygame.font.Font("assets/fonts/score_font.ttf", 40)
        
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
                self.score += 1
        
    def render_boundary(self) -> None:
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
        
    def generate_rects(self, 
                       icon: pygame.Surface,
                       font: pygame.Surface,
                       spacing: int,
                       frame_x_coords: Tuple[int, int],
                       frame_y_coords: Tuple[int, int],
                       ) -> Tuple[pygame.Rect, pygame.Rect]:
        icon_width = icon.get_width()
        font_width = font.get_width()
        total_length = icon_width + spacing + font_width
        
        frame_start_x, frame_end_x = frame_x_coords
        frame_length = frame_end_x - frame_start_x
        
        center_y = frame_y_coords[0] + ((frame_y_coords[1] - frame_y_coords[0]) // 2)
        gap = (frame_length - total_length) // 2
        
        icon_rect = self.apple_icon.get_rect(left=frame_start_x+gap, centery=center_y)
        font_rect = font.get_rect(right=frame_end_x-gap, centery=center_y)
        
        return (icon_rect, font_rect)
        
    def render_score(self, boundary_lines: BoundaryLines) -> None:
        score_font = self.game_font.render(str(self.score), True, "white")
        apple_rect, font_rect = self.generate_rects(
            icon=self.apple_icon,
            font=score_font,
            spacing=10,
            frame_x_coords=(boundary_lines.score_separator.right, boundary_lines.line_right.left),
            frame_y_coords=(boundary_lines.stats_separator.bottom, boundary_lines.line_bottom.top)
        )
        self.display.blit(self.apple_icon, apple_rect)
        self.display.blit(score_font, font_rect)
        
    def render_high_score(self, boundary_lines: BoundaryLines) -> None:
        high_score_font = self.game_font.render(str(self.high_score), True, "white")
        trophy_rect, font_rect = self.generate_rects(
            icon=self.trophy_icon,
            font=high_score_font,
            spacing=10,
            frame_x_coords=(boundary_lines.line_left.right, boundary_lines.highscore_separator.left),
            frame_y_coords=(boundary_lines.stats_separator.bottom, boundary_lines.line_bottom.top)
        )
        self.display.blit(self.trophy_icon, trophy_rect)
        self.display.blit(high_score_font, font_rect)
        
    def render_scoreboard(self, boundary_lines: BoundaryLines) -> None:
        self.render_score(boundary_lines)
        self.render_high_score(boundary_lines)
    
    def render(self) -> None:
        self.snake.render()
        self.fruit.render()
        boundary_lines = self.render_boundary()
        self.render_scoreboard(boundary_lines)