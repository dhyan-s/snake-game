import pygame
from typing import Tuple, Union, List

from .snake_head import SnakeHead
from .snake_body import SnakeBody

class Snake:
    def __init__(self, 
                 display: pygame.Surface, 
                 x: int, 
                 y: int, 
                 body_color: str = "green",
                 outline_color: str = "white",
                 eye_color: str = "black",
                 piece_width: int = 16,
                 piece_height: int = 32,
                 head_width: int = 32,
                 head_height: int = 32,
                 outline_width: int = 3,
                 eye_width: Union[int, float] = 6.5,
                 eye_height: Union[int, float] = 6.5,
                 eye_front_distance: int = 6,
                 eye_side_distance: int = 5,
                 initial_direction: str = "r",
                 extend_by: int = 3) -> None:
        self.display = display
                
        self.head = SnakeHead(
            display=display,
            x=x,
            y=y,
            velocity=piece_width,
            width=head_width,
            height=head_height,
            outline_width=outline_width,
            color=body_color,
            outline_color=outline_color,
            eye_color=eye_color,
            eye_width=eye_width,
            eye_height=eye_height,
            eye_front_distance=eye_front_distance,
            eye_side_distance=eye_side_distance,
            initial_direction=initial_direction
        )
        self.body = SnakeBody(
            display=display,
            snake_head=self.head,
            piece_width=piece_width,
            piece_height=piece_height,
            color=body_color,
            outline_color=outline_color,
            outline_width=outline_width,
            initial_direction=initial_direction,
            extend_by=extend_by
        )
        
    def up(self) -> None:
        self.head.up()
        self.body.up()
        
    def down(self) -> None:
        self.head.down()
        self.body.down()
        
    def left(self) -> None:
        self.head.left()
        self.body.left()
        
    def right(self) -> None:
        self.head.right()
        self.body.right()
        
    def extend(self) -> None:
        self.body.extend()
        
    def move(self) -> None:
        self.head.move()
        self.body.move()
        
    def render(self) -> None:
        self.head.render()
        self.body.render()
        