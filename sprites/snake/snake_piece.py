import pygame
from typing import Tuple, Union

class SnakePiece:
    def __init__(self,
                 display: pygame.Surface,
                 x: int,
                 y: int,
                 width: int = 16,
                 height: int = 32,
                 color: str = "green",
                 outline_color: str = "white",
                 outline_width: int = 3,
                 initial_direction: str = 'r') -> None:
        self.display = display
        
        self.outline_width = outline_width
        self.color = color
        self.outline_color = outline_color

        self._orient = "v"
        self._swapped_dimensions = True
        
        self.rect = pygame.Rect(x, y, width, height)  
        self.direction = initial_direction      
    
    @property
    def direction(self) -> str:
        return self._direction
    
    @direction.setter
    def direction(self, val: str) -> None:
        if val not in {"r", "l", "u", "d"}:
            raise ValueError(f"Invalid direction: {val}")
        self._direction = val
        self.orient = "h" if val in {"r", "l"} else "v"
            
    def behind(self, other_piece_width: int, other_piece_height: int) -> Tuple[Union[int, float], Union[int, float]]:
        rect = self.rect
        if self.direction == 'd':
            return (rect.x, rect.top-other_piece_height)
        elif self.direction == 'l':
            return (rect.right, rect.y)
        elif self.direction == 'r':
            return (rect.left-other_piece_width, rect.y)
        elif self.direction == 'u':
            return (rect.x, rect.bottom)
        
    @property
    def orient(self) -> str: 
        return self._orient
    
    @orient.setter
    def orient(self, val) -> None:
        if val not in ["vertical", "horizontal", "v", "h"]:
            raise ValueError("Invalid orient. Must be 'v', 'h', 'vertical' or 'horizontal'")
        self._orient = val.replace("vertical", "v").replace("horizontal", "h")
        if self._orient == "v":
            if self._swapped_dimensions:
                self.rect.width, self.rect.height = self.rect.height, self.rect.width
                self._swapped_dimensions = False
        elif not self._swapped_dimensions:
            self.rect.width, self.rect.height = self.rect.height, self.rect.width
            self._swapped_dimensions = True
        
    def render(self) -> None:
        pygame.draw.rect(self.display, pygame.Color(self.color), self.rect)
        pygame.draw.rect(self.display, pygame.Color(self.outline_color), self.rect, width=self.outline_width)
        