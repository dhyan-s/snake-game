import pygame
from typing import Tuple, Union
from .snake_piece import SnakePiece


class SnakeHead(SnakePiece):
    """
    Represents the head of the snake in the snake game.
    """

    def __init__(
        self,
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
        initial_direction: str = "r"
    ) -> None:
        """
        Initialize the SnakeHead instance.

        Parameters:
            - display: The pygame.Surface object representing the display surface.
            - x: The x-coordinate of the head's initial position.
            - y: The y-coordinate of the head's initial position.
            - velocity: The velocity of the head, determines the speed of movement.
            - width: The width of the head.
            - height: The height of the head.
            - outline_width: The width of the outline around the head.
            - color: The color of the head.
            - outline_color: The color of the outline around the head.
            - eye_color: The color of the eyes.
            - eye_width: The width of each eye.
            - eye_height: The height of each eye.
            - eye_front_distance: The distance of the eyes from the front of the head.
            - eye_side_distance: The distance of the eyes from the sides of the head.
            - initial_direction: The initial direction of the head ('u' for up, 'd' for down, 'l' for left, 'r' for right).
        """
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
        self.__moving: bool = False
        self.__initial_direction: str = initial_direction
        self.__start_x: int = x
        self.__start_y: int = y
        
    def start(self) -> None:
        """Start the movement of the snake head."""
        self.__moving = True
        
    def stop(self) -> None:
        """Stop the movement of the snake head."""
        self.__moving = False
        
    def reset(self) -> None:
        """
        Reset the direction and coordinates of the snake head to the
        initial values specified during initialization.
        """
        self.direction = self.__initial_direction
        self.rect.topleft = (self.__start_x, self.__start_y)
        
    @property
    def moving(self) -> bool:
        """Get the current movement status of the snake head."""
        return self.__moving

    def up(self) -> None:
        """Change the direction of the head to up."""
        if not self.__moving: return
        self.direction = 'u'

    def down(self) -> None:
        """Change the direction of the head to down."""
        if not self.__moving: return
        self.direction = 'd'

    def left(self) -> None:
        """Change the direction of the head to left."""
        if not self.__moving: return
        self.direction = 'l'

    def right(self) -> None:
        """Change the direction of the head to right."""
        if not self.__moving: return
        self.direction = 'r'

    def _get_eye_coordinates(self, 
                             rect: pygame.Rect, direction: str
                             ) -> Tuple[Union[int, float], 
                                        Union[int, float], 
                                        Union[int, float], 
                                        Union[int, float]]:
        """
        Calculate the coordinates of the eyes based on the head's rectangle and direction.

        Parameters:
            - rect: The pygame.Rect object representing the head's rectangle.
            - direction: The current direction of the head.

        Returns:
            - A tuple of four coordinates (eye1_x, eye1_y, eye2_x, eye2_y) representing the position of the eyes.
        """
        up_eye_y = rect.top + self.eye_front_distance
        down_eye_y = rect.bottom - self.eye_front_distance - self.eye_height
        left_eye_x = rect.left + self.eye_front_distance
        right_eye_x = rect.right - self.eye_front_distance - self.eye_width

        if direction in {'u', 'd'}:
            eye1_x = rect.right - self.eye_side_distance - self.eye_width
            eye2_x = rect.left + self.eye_side_distance
            eye1_y = eye2_y = up_eye_y if direction == 'u' else down_eye_y
        elif direction in {'l', 'r'}:
            eye1_y = rect.top + self.eye_side_distance
            eye2_y = rect.bottom - self.eye_side_distance - self.eye_height
            eye1_x = eye2_x = left_eye_x if direction == 'l' else right_eye_x

        return eye1_x, eye1_y, eye2_x, eye2_y

    def __get_velocity(self, direction: str) -> Tuple[int, int]:
        """
        Calculate the x and y velocity for the head based on the current direction.

        Parameters:
            - direction: The current direction of the head.
        """
        if direction == 'u': return (0, -self.velocity)
        elif direction == 'd': return (0, self.velocity)
        elif direction == 'l': return (-self.velocity, 0)
        elif direction == 'r': return (self.velocity, 0)

    def draw_eye(self) -> None:
        """Draw the eyes inside the head."""
        eye1_x, eye1_y, eye2_x, eye2_y = self._get_eye_coordinates(self.rect, self.direction)
        eye1 = pygame.draw.ellipse(self.display, self.eye_color, [eye1_x, eye1_y, self.eye_width, self.eye_height])
        eye2 = pygame.draw.ellipse(self.display, self.eye_color, [eye2_x, eye2_y, self.eye_width, self.eye_height])

    def move(self) -> None:
        """Move the head according to the current direction."""
        if not self.__moving: return
        x_vel, y_vel = self.__get_velocity(self.direction)
        self.rect.x += x_vel
        self.rect.y += y_vel

    def render(self) -> None:
        """Draw the head on the screen."""
        self.move()
        pygame.draw.rect(self.display, self.color, self.rect)
        pygame.draw.rect(self.display, self.outline_color, self.rect, width=self.outline_width)
        self.draw_eye()
