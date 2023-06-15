import pygame
from typing import Tuple, Callable

from sprites.snake import Snake
from .boundary import Boundary
from .utils import center_of, center_of_rect

class GameOver:
    def __init__(self, 
                 display: pygame.Surface, 
                 snake: Snake, 
                 boundary: Boundary,
                 gameover_font: pygame.font.Font,
                 message_font: pygame.font.Font,
                 gameover_callback: Callable = None,
                 restart_callback: Callable = None
                 ):
        self.display = display
        self.snake = snake
        self.boundary = boundary
        
        self.gameover_font = gameover_font
        self.message_font = message_font
        
        self.gameover_callback = gameover_callback
        self.restart_callback = restart_callback
        
        self.game_over = False
        self.reset()
        
    def reset(self) -> None:
        if not self.game_over: 
            return
        self.game_over = False
        self.reason = ""
        if self.restart_callback is not None:
            self.restart_callback()
    
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
            if self.game_over and self.gameover_callback is not None:
                self.gameover_callback()
        self.render_gameover_text()
    
    def render_gameover_text(self) -> None:
        if not self.game_over: return
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
        