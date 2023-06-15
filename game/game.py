import pygame
import os
from typing import Tuple, Union

from sprites.snake import Snake
from sprites.fruit import Fruit
from .score import Score
from .boundary import Boundary
from .gameover import GameOver
from .utils import center_of_rect


class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.load_fonts()
        self.load_game_objects()
        self.load_scoreboard()
        
    def load_game_objects(self) -> None:
        self.snake = Snake(self.display, 15, 15, outline_width=2)
        self.fruit = Fruit(self.display, 20, 20)
        self.boundary = Boundary(self.display)
        self.gameover_handler = GameOver(
            display = self.display, 
            snake = self.snake, 
            boundary = self.boundary, 
            gameover_font = self.gameover_font, 
            message_font = self.message_font,
            gameover_callback = self.snake.stop,
            restart_callback = self.restart_game,
        )
        self.change_fruit_pos()
        self.snake.start()
        
    def load_fonts(self) -> None:
        font_path = "assets/fonts"
        
        game_font_path = f"{font_path}/game_font.ttf"
        self.game_font = pygame.font.Font(game_font_path, 40)
        self.gameover_font = pygame.font.Font(game_font_path, 110)
        
        message_font_path = f"{font_path}/message_font.ttf"
        self.message_font = pygame.font.Font(message_font_path, 35)
        
    def load_scoreboard(self) -> None:
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
        
    def restart_game(self) -> None:
        self.scoreboard.reset_score()
        self.snake.reset()
        self.change_fruit_pos()
        self.snake.start()
        
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
        elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
            self.gameover_handler.reset()
            
    def render_title(self) -> None:
        title_text = self.game_font.render("SNAKE GAME BY DHYANESH !!" , True , "white")
        title_rect = title_text.get_rect(center=center_of_rect(
            (self.boundary.highscore_separator.right, self.boundary.score_separator.left),
            (self.boundary.stats_separator.bottom, self.boundary.bottom_line.top+2)
        ))
        self.display.blit(title_text, title_rect)
    
    def render(self) -> None:
        self.gameover_handler.handle_game_over()
        self.point()
        self.snake.render()
        self.fruit.render()
        self.scoreboard.render(
            score_coords = center_of_rect(
                (self.boundary.score_separator.right, self.boundary.right_line.left),
                (self.boundary.stats_separator.bottom, self.boundary.bottom_line.top)
            ),
            highscore_coords = center_of_rect(
                (self.boundary.left_line.right, self.boundary.highscore_separator.left),
                (self.boundary.stats_separator.bottom, self.boundary.bottom_line.top)
            )
        )
        self.boundary.render()
        self.render_title()
        self.gameover_handler.render_gameover_text()
        