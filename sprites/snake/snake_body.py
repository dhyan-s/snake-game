import pygame
from typing import List, Tuple, Union

from .snake_head import SnakeHead
from .snake_piece import SnakePiece

class SnakeBody:
    """
    Represents the body of a snake in the snake game.
    """
    
    def __init__(self, 
                 display: pygame.Surface,
                 snake_head: SnakeHead,
                 piece_width: int = 16,
                 piece_height: int = 32,
                 color: str = "green",
                 outline_color: str = "white",
                 outline_width: str = 3,
                 extend_by: int = 3) -> None:
        """
        Parameters:
            - display (pygame.Surface): The display surface to render the body on.
            - snake_head (SnakeHead): The snake head object.
            - piece_width (int): The width of each snake piece. (default: 16)
            - piece_height (int): The height of each snake piece. (default: 32)
            - color (str): The color of the snake body. (default: "green")
            - outline_color (str): The color of the outline. (default: "white")
            - outline_width (int): The width of the outline. (default: 3)
            - initial_direction (str): The initial direction of the snake body. (default: "r")
            - extend_by (int): The number of pieces to extend the snake body by. (default: 3)
        """
        self.display = display
        self.head = snake_head
        
        self.outline_width = outline_width
        self.piece_width = piece_width
        self.piece_height = piece_height
        
        self.color = color
        self.outline_color = outline_color

        self.extend_by = extend_by
        
        self.pieces: List[SnakePiece] = []
        self.no_pieces: int = 0
        
        self.__moving: bool = False
        
    def start(self) -> None:
        """Start the movement of the snake body."""
        self.__moving = True
        
    def stop(self) -> None:
        """Stop the movement of the snake body."""
        self.__moving = False
        
    def reset(self) -> None:
        """Delete all the pieces of the snake body."""
        self.pieces.clear()
        self.no_pieces = 0
        
    @property
    def moving(self) -> bool:
        """Get the current movement status of the snake head."""
        return self.__moving
        
    def colliding_with(self, other_rect: pygame.Rect) -> bool:
        """Check if the body is colliding with another Rect object."""
        return any(piece.colliding_with(other_rect) for piece in self.pieces)
    
    def add_piece(self) -> None:
        """Add a new SnakePiece to the body right behind the tail of the snake, making it the new tail."""
        previous_piece: SnakePiece = self.pieces[-1] if self.pieces else self.head
        new_piece = SnakePiece(display=self.display, 
                               x=0, 
                               y=0, 
                               width=self.piece_width, 
                               height=self.piece_height,
                               color=self.color,
                               outline_color=self.outline_color,
                               outline_width=self.outline_width,
                               initial_direction=previous_piece.direction)
        new_piece.rect.topleft = previous_piece.behind(new_piece.rect.width, new_piece.rect.height)
        self.pieces.append(new_piece)
        return new_piece
        
    def extend(self) -> None:
        """Increase the number of pieces the body has."""
        self.no_pieces += 3
        
    def __len__(self) -> int:
        """Get the number of pieces in the body."""
        return len(self.pieces)
    
    length = __len__

    def move(self) -> None:
        """Handles movement of the snake body."""
        if not (self.pieces and self.__moving): return
        reversed_pieces = list(reversed(self.pieces))
        for idx, piece in enumerate(reversed_pieces[:-1]):
            piece.direction = reversed_pieces[idx+1].direction
            piece.rect.x = reversed_pieces[idx+1].rect.x
            piece.rect.y = reversed_pieces[idx+1].rect.y
        self.pieces[0].direction = self.head.direction
        x, y = self.head.behind(self.pieces[0].rect.width, self.pieces[0].rect.height)
        self.pieces[0].rect.x = x
        self.pieces[0].rect.y = y
        
    def render(self) -> None:
        """Draw the snake body on the screen."""
        if len(self.pieces) < self.no_pieces: # Change 'if' to 'while' to add all pieces in one frame.
            self.add_piece()
        self.move()
        for piece in self.pieces:
            piece.render()
            