import pygame
import os
from typing import Tuple, Union

from sprites.snake import Snake
from sprites.fruit import Fruit
from .score import Score
from .utils import center_of_rect, center_of
from .boundary import Boundary


class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.game_over = False

        self.load_game_objects()
        self.load_fonts()
        self.load_scoreboard()
        
    def load_game_objects(self) -> None:
        self.snake = Snake(self.display, 15, 15, outline_width=2)
        self.fruit = Fruit(self.display, 20, 20)
        self.boundary = Boundary(self.display)
        
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
        
    def check_game_over(self) -> Tuple[bool, str]:
        if self.snake.body.colliding_with(self.snake.head.rect):
            return (True, "SNAKE BUMPED INTO ITSELF")
        elif any(self.snake.colliding_with(rect) for rect in [self.boundary.top_line, 
                                                              self.boundary.bottom_line, 
                                                              self.boundary.left_line, 
                                                              self.boundary.right_line, 
                                                              self.boundary.stats_separator]):
            return (True, "SNAKE MOVED OUT OF THE BOUNDARY")
        return (False, "")
        
    def handle_game_over(self) -> None:
        if not self.game_over:
            self.game_over, self.reason = self.check_game_over()
        
    def render_gameover_text(self) -> None:
        game_over_text = self.gameover_font.render("GAMEOVER!" , True , "white")
        reason_text = self.message_font.render(f"REASON: {self.reason}" , False , "white") 
        restart_text = self.message_font.render("PRESS ENTER OR SPACEBAR TO CONTINUE" , False , "white")  
        
        y_spacing = 20
        x_range = (self.boundary.left_line.right, self.boundary.right_line.left)
        
        game_over_rect = game_over_text.get_rect(midbottom=center_of_rect(
            x_range,
            (self.boundary.top_line.bottom, self.boundary.stats_separator.top)
        ))
        
        reason_rect = reason_text.get_rect(midtop=(
            center_of(x_range), game_over_rect.bottom + y_spacing
        ))
        
        restart_rect = restart_text.get_rect(midtop=(
            center_of(x_range), reason_rect.bottom + y_spacing
        ))
        
        self.display.blit(game_over_text, game_over_rect)
        self.display.blit(reason_text, reason_rect)
        self.display.blit(restart_text, restart_rect)
        
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
        self.handle_game_over()
        if self.game_over:
            self.snake.stop()
            self.render_gameover_text()
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