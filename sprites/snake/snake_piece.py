import pygame
from typing import Tuple, Union

class SnakePiece:
    """
    Represents a piece of the snake in the snake game.
    """
    
    def __init__(
        self,
        display: pygame.Surface,
        x: int,
        y: int,
        width: int = 16,
        height: int = 32,
        color: str = "green",
        outline_color: str = "white",
        outline_width: int = 3,
        initial_direction: str = 'r'
    ) -> None:
        """
        Parameters:
        - display (pygame.Surface): The display surface to render the piece on.
        - x (int): The x-coordinate of the piece's top-left corner.
        - y (int): The y-coordinate of the piece's top-left corner.
        - width (int): The width of the piece. (default: 16)
        - height (int): The height of the piece. (default: 32)
        - color (str): The color of the piece. (default: "green")
        - outline_color (str): The color of the outline. (default: "white")
        - outline_width (int): The width of the outline. (default: 3)
        - initial_direction (str): The initial direction of the piece. (default: 'r')
        """
        self.display = display
        self.outline_width = outline_width
        self.color = color
        self.outline_color = outline_color
        self.__orient = "v"
        self.__swapped_dimensions = True
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = initial_direction
        
    def colliding_with(self, other_rect: pygame.Rect) -> bool:
        """Check if the piece is colliding with another Rect object."""
        return self.rect.colliderect(other_rect)

    @property
    def direction(self) -> str:
        """Get the direction of the piece."""
        return self.__direction

    @direction.setter
    def direction(self, val: str) -> None:
        """
        Set the direction of the piece.

        Raises:
            ValueError: If the direction value is invalid.
        """
        if val not in {"r", "l", "u", "d"}:
            raise ValueError(f"Invalid direction: {val}")
        self.__direction = val
        self.orient = "h" if val in {"r", "l"} else "v"

    def behind(self, other_piece_width: int, other_piece_height: int) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Calculate the position to place another piece behind this piece.

        Parameters:
            other_piece_width (int): The width of the other piece.
            other_piece_height (int): The height of the other piece.

        Returns:
            Tuple: The top-left coordinates for placing the other piece.
        """
        rect = self.rect
        if self.direction == 'd':
            return (rect.x, rect.top - other_piece_height)
        elif self.direction == 'l':
            return (rect.right, rect.y)
        elif self.direction == 'r':
            return (rect.left - other_piece_width, rect.y)
        elif self.direction == 'u':
            return (rect.x, rect.bottom)

    @property
    def orient(self) -> str:
        """Get the orientation of the piece."""
        return self.__orient

    @orient.setter
    def orient(self, val: str) -> None:
        """
        Set the orientation of the piece.

        The orient adjustment is done by swapping the width and height
        and updating its respective flag.

        Raises:
            ValueError: If the orientation value is invalid.
        """
        if val not in ["vertical", "horizontal", "v", "h"]:
            raise ValueError("Invalid orient. Must be 'v', 'h', 'vertical' or 'horizontal'")
        self.__orient = val.replace("vertical", "v").replace("horizontal", "h")

        if self.__orient == "v":
            if self.__swapped_dimensions:
                self.rect.width, self.rect.height = self.rect.height, self.rect.width
                self.__swapped_dimensions = False

        elif not self.__swapped_dimensions:
            self.rect.width, self.rect.height = self.rect.height, self.rect.width
            self.__swapped_dimensions = True

    def render(self) -> None:
        """Draw the piece on the screen."""
        pygame.draw.rect(self.display, pygame.Color(self.color), self.rect)
        pygame.draw.rect(self.display, pygame.Color(self.outline_color), self.rect, width=self.outline_width)
