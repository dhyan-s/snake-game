import pygame
from typing import List, Tuple, Union

from .snake_head import SnakeHead
from .snake_piece import SnakePiece

class SnakeBody:
    def __init__(self, 
                 display: pygame.Surface,
                 snake_head: SnakeHead,
                 piece_width: int = 16,
                 piece_height: int = 32,
                 color: str = "green",
                 outline_color: str = "white",
                 outline_width: str = 3,
                 initial_direction: str = "r",
                 extend_by: int = 3) -> None:
        self.display = display
        self.head = snake_head
        
        self.outline_width = outline_width
        self.piece_width = piece_width
        self.piece_height = piece_height
        
        self.color = color
        self.outline_color = outline_color
        
        self.direction = initial_direction
        self.extend_by = extend_by
        
        self.pieces: List[SnakePiece] = []
        self.no_pieces = 0
        
    @property
    def direction(self) -> str:
        return self._direction
    
    @direction.setter
    def direction(self, val: str) -> None:
        if val in {"r", "l", "u", "d"}:
            self._direction = val
        else:
            raise ValueError(f"Invalid direction: {val}")
        
    def up(self) -> None: self.direction = 'u'
    def down(self) -> None: self.direction = 'd'
    def left(self) -> None: self.direction = 'l'
    def right(self) -> None: self.direction = 'r'
    
    def add_piece(self) -> None:
        previous_piece = self.pieces[-1] if self.pieces else self.head
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
        self.no_pieces += 3

    def move(self) -> None:
        if not self.pieces: return
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
        if len(self.pieces) < self.no_pieces: # Change 'if' to 'while' to add all pieces in one frame.
            self.add_piece()
        self.move()
        for piece in self.pieces:
            piece.render()
            