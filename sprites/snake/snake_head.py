import pygame
from typing import Tuple, Union

from .snake_piece import SnakePiece

class SnakeHead(SnakePiece):
    def __init__(self,
                 display: pygame.Surface,
                 x: int,
                 y: int,
                 velocity: int,
                 width: int = 32,
                 height: int = 32,
                 outline_width: int = 3,
                 color: str = "green",
                 outline_color: str = "white",
                 eye_color: str = "black",
                 eye_width: Union[int, float] = 6.5,
                 eye_height: Union[int, float] = 6.5,
                 eye_front_distance: int = 6,
                 eye_side_distance: int = 5,
                 initial_direction: str = "r") -> None:
        self.eye_color = eye_color
        self.eye_width = eye_width
        self.eye_height = eye_height
        self.eye_front_distance = eye_front_distance
        self.eye_side_distance = eye_side_distance

        self.velocity = velocity
        
        super().__init__(
            display=display,
            x=x,
            y=y,
            width=width,
            height=height,
            color=color,
            outline_color=outline_color,
            outline_width=outline_width,
            initial_direction=initial_direction
        )
        
    def up(self) -> None: self.direction = 'u'
    def down(self) -> None: self.direction = 'd'
    def left(self) -> None: self.direction = 'l'
    def right(self) -> None: self.direction = 'r'
        
    def _get_eye_coordinates(self, rect: pygame.Rect, direction: str) -> Tuple[
                                                                            Union[int, float], 
                                                                            Union[int, float], 
                                                                            Union[int, float], 
                                                                            Union[int, float]
                                                                            ]:
        up_eye_y = rect.top+self.eye_front_distance
        down_eye_y = rect.bottom-self.eye_front_distance-self.eye_height
        left_eye_x = rect.left+self.eye_front_distance
        right_eye_x = rect.right-self.eye_front_distance-self.eye_width

        if direction in {'u', 'd'}:
            eye1_x = rect.right-self.eye_side_distance-self.eye_width
            eye2_x = rect.left+self.eye_side_distance
            eye1_y = eye2_y = up_eye_y if direction == 'u' else down_eye_y
        elif direction in {'l', 'r'}:
            eye1_y = rect.top+self.eye_side_distance
            eye2_y = rect.bottom-self.eye_side_distance-self.eye_height
            eye1_x = eye2_x = left_eye_x if direction == 'l' else right_eye_x
        return eye1_x, eye1_y, eye2_x, eye2_y
    
    def _get_velocity(self, direction: str) -> Tuple[int, int]:
        if direction == 'u':
            x_vel = 0
            y_vel = -self.velocity
        elif direction == 'd':
            x_vel = 0
            y_vel = self.velocity
        elif direction == 'l':
            x_vel = -self.velocity
            y_vel = 0
        elif direction == 'r':
            x_vel = self.velocity
            y_vel = 0
        return x_vel, y_vel
    
    def draw_eye(self) -> None:
        eye1_x, eye1_y, eye2_x, eye2_y = self._get_eye_coordinates(self.rect, self._direction)
        
        eye1 = pygame.draw.ellipse(self.display, self.eye_color, [eye1_x, eye1_y, self.eye_width, self.eye_height])
        eye2 = pygame.draw.ellipse(self.display, self.eye_color, [eye2_x, eye2_y, self.eye_width, self.eye_height])
        
    def move(self) -> None:
        x_vel, y_vel = self._get_velocity(self._direction)
        self.rect.x += x_vel
        self.rect.y += y_vel
    
    def render(self) -> None:
        self.move()
        pygame.draw.rect(self.display, self.color, self.rect)
        pygame.draw.rect(self.display, self.outline_color, self.rect, width=self.outline_width)
        self.draw_eye()
        