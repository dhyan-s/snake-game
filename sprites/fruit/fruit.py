import pygame
import random
from typing import Tuple, List, Union

class Fruit:
    """
    Represents a fruit object in a Pygame snake game.
    """
    def __init__(self, 
                 display: pygame.Surface,
                 x: int,
                 y: int,
                 width: int = 32,
                 height: int = 32,
                 outline_width: int = 3,
                 color: Union[str, Tuple[int, int, int]] = "red",
                 outline_color: Union[str, Tuple[int, int, int]] = "white",
                 ) -> None:
        self.display = display
        
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.outline_width = outline_width
        
        self.color = color
        self.outline_color = outline_color
        
        self.rect: pygame.Rect
        
        self.update_rect()
        
    def set_pos_to(self, coords: Tuple) -> None:
        """Set the position of the fruit to the specified coordinates."""
        self.x, self.y = coords
        
    def set_random_pos(self, 
                       x_range: Union[Tuple[int, int], List[int]] = None,
                       y_range: Union[Tuple[int, int], List[int]] = None) -> None:
        """Set the position of the fruit to a random location within the specified range."""
        if x_range is None: x_range = (0, self.display.get_width())
        if y_range is None: y_range = (0, self.display.get_height())
        x_range, y_range = map(list, (x_range, y_range))
        x_range[1] -= self.width
        y_range[1] -= self.height
        
        self.x = random.randint(*x_range)
        self.y = random.randint(*y_range)
        self.update_rect()
        
    def update_rect(self) -> None:
        """Update the rect of the fruit based on the instance attributes."""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def render(self) -> None:
        """Draw the fruit on the display surface."""
        self.update_rect()
        apple = pygame.draw.ellipse(self.display, self.color, self.rect)
        apple_outline = pygame.draw.ellipse(self.display, self.outline_color, self.rect, width=self.outline_width)
        