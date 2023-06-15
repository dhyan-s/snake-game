import pygame
from typing import Tuple, Union, List

from .snake_head import SnakeHead
from .snake_body import SnakeBody

class Snake:
    """
    A class that represents the snake object in the game.

    ### Advantages:
    - The snake is visually represented by outlining each piece of the head and body, creating a grid-like appearance that enhances the game's visual experience.
    - The snake's body pieces are smaller than the head, resulting in smoother movement.

    ### Drawbacks:
    - The current version of the Snake class does not support custom velocity. The velocity is determined by the width of each piece.
        - Since each piece is positioned at the previous location of the next piece, the velocity must be equal to the width of each individual piece to enable smooth turning.
        - So more the width, faster the snake moves.

    #### Movement:
    - The snake's head is controlled using keyboard inputs.
    - The first body piece always follows the head, and each subsequent piece moves to the previous position of the next piece, starting from the tail.
    - For example, suppose the snake has 3 pieces: Piece3 at position a, Piece2 at position b, Piece1 at position c, and the Head at position d.
    - With each movement, the Head moves to position e (new position), Piece1 moves to position d (previous Head's position), Piece2 moves to position c (previous Piece1's position), and Piece3 moves to position b (previous Piece2's position).
    - This creates a smooth visual effect as the entire snake moves x pixels in a particular direction.
    """

    
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
        """
        Parameters:
            - display (pygame.Surface): The display surface to render the snake on.
            - x (int): The x-coordinate of the snake's top-left corner.
            - y (int): The y-coordinate of the snake's top-left corner.
            - body_color (str): The color of the snake's body. (default: "green")
            - outline_color (str): The color of the snake's outline. (default: "white")
            - eye_color (str): The color of the snake's eyes. (default: "black")
            - piece_width (int): The width of each snake piece. (default: 16)
            - piece_height (int): The height of each snake piece. (default: 32)
            - head_width (int): The width of the snake's head. (default: 32)
            - head_height (int): The height of the snake's head. (default: 32)
            - outline_width (int): The width of the snake's outline. (default: 3)
            - eye_width (Union[int, float]): The width of the snake's eyes. (default: 6.5)
            - eye_height (Union[int, float]): The height of the snake's eyes. (default: 6.5)
            - eye_front_distance (int): The distance of the snake's eyes from the front of the head. (default: 6)
            - eye_side_distance (int): The distance of the snake's eyes from the sides of the head. (default: 5)
            - initial_direction (str): The initial direction of the snake. (default: 'r')
            - extend_by (int): The number of pieces to extend the snake's body by when it eats food. (default: 3)
        """
        
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
            extend_by=extend_by
        )
        
    def colliding_with(self, other_rect: pygame.Rect) -> bool: 
        return self.head.colliding_with(other_rect) or self.body.colliding_with(other_rect)
        
    def start(self) -> None:
        self.head.start()
        self.body.start()
        
    def stop(self) -> None:
        self.head.stop()
        self.body.stop()
        
    def up(self) -> None:
        """Makes the snake travel upwards."""
        self.head.up()
        
    def down(self) -> None:
        """Makes the snake travel downwards."""
        self.head.down()
        
    def left(self) -> None:
        """Makes the snake travel towards the left."""
        self.head.left()
        
    def right(self) -> None:
        """Makes the snake travel towards the right."""
        self.head.right()
        
    def extend(self) -> None:
        """Extends the snake's body by adding more pieces."""
        self.body.extend()
        
    def move(self) -> None:
        """Handles movement of the snake"""
        self.head.move()
        self.body.move()
        
    def render(self) -> None:
        """Draws the snake onto the screen."""
        self.head.render()
        self.body.render()
        