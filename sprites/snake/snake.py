import pygame
from typing import Tuple, Union, List

class Snake:
    def __init__(self, 
                 display: pygame.Surface, 
                 x: int, 
                 y: int, 
                 body_color: str = "green",
                 outline_color: str = "white",
                 eye_color: str = "black",
                 width: int = 32,
                 height: int = 32,
                 outline_width: int = 3,
                 eye_width: Union[int, float] = 6.5,
                 eye_height: Union[int, float] = 6.5,
                 eye_front_distance: int = 6,
                 eye_side_distance: int = 5,
                 initial_direction: str = "r") -> None:
        self.display = display
                
        self.x = x
        self.y = y
        self.body_color = pygame.Color(body_color)
        self.outline_color = pygame.Color(outline_color)
        self.eye_color = pygame.Color(eye_color)
        self.outline_width = outline_width
        self.eye_width = eye_width
        self.eye_height = eye_height
        self.eye_front_distance = eye_front_distance
        self.eye_side_distance = eye_side_distance
        self.width = width
        self.height = height
        
        self.coordinates: List[List[int, int]] = [[x, y]]
        self.velocity = 5
        
        self.up, self.down, self.left, self.right = "u", "d", "l", "r"
        self.direction = initial_direction
        
    def draw_square(self, coord_idx: int) -> None:
        x, y = self.coordinates[coord_idx][0], self.coordinates[coord_idx][1]
        body = pygame.draw.rect(self.display, self.body_color, [x, y, self.width, self.height])
        outline = pygame.draw.rect(self.display, self.outline_color, [x, y, self.width, self.height], width=self.outline_width)
        return body, outline
    
    def _get_eye_coordinates(self, body: pygame.Rect, direction: str) -> Tuple[
                                                                            Union[int, float], 
                                                                            Union[int, float], 
                                                                            Union[int, float], 
                                                                            Union[int, float]
                                                                            ]:
        # sourcery skip: extract-duplicate-method, split-or-ifs
        up_eye_y = body.top+self.eye_front_distance
        down_eye_y = body.bottom-self.eye_front_distance-self.eye_height
        left_eye_x = body.left+self.eye_front_distance
        right_eye_x = body.right-self.eye_front_distance-self.eye_width
        
        if direction in [self.up, self.down]:
            eye1_x = body.right-self.eye_side_distance-self.eye_width
            eye2_x = body.left+self.eye_side_distance
            eye1_y = eye2_y = up_eye_y if direction == self.up else down_eye_y
        elif direction in [self.left, self.right]:
            eye1_y = body.top+self.eye_side_distance
            eye2_y = body.bottom-self.eye_side_distance-self.eye_height
            eye1_x = eye2_x = left_eye_x if direction == self.left else right_eye_x
        return eye1_x, eye1_y, eye2_x, eye2_y
        
    def draw_head(self) -> None:
        body, outline = self.draw_square(0)
        
        eye1_x, eye1_y, eye2_x, eye2_y = self._get_eye_coordinates(body, self.direction)
        
        eye1 = pygame.draw.ellipse(self.display, self.eye_color, [eye1_x, eye1_y, self.eye_width, self.eye_height])
        eye2 = pygame.draw.ellipse(self.display, self.eye_color, [eye2_x, eye2_y, self.eye_width, self.eye_height])
        
    def move(self):
        direction_map = {
            self.up: (0, -self.velocity),
            self.down: (0, self.velocity),
            self.left: (-self.velocity, 0),
            self.right: (self.velocity, 0),
        }
        self.coordinates[0][0] += direction_map[self.direction][0]
        self.coordinates[0][1] += direction_map[self.direction][1]
        
    def render(self):
        self.move()
        self.draw_head()