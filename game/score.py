import pygame
from typing import Callable, Tuple, List


class Score:
    """
    This class handles the management and rendering of the score and highscore in the game.
    It provides methods to increment and reset the score, as well as rendering the score and
    highscore on a display surface.
    """
    def __init__(self,
                 display: pygame.Surface,
                 score_icon_path: pygame.Surface,
                 highscore_icon_path: pygame.Surface,
                 font: pygame.font.Font,
                 spacing: int = 10,
                 icon_size: Tuple[int, int] = None,
                 ):
        """
        Parameters:
            display (pygame.Surface): The display surface to render the score on.
            score_icon_path (str): The file path to the score icon image.
            highscore_icon_path (str): The file path to the highscore icon image.
            font (pygame.font.Font): The font used for rendering the score and highscore.
            spacing (int): The spacing between the icon and the score/highscore. (default: 10)
            icon_size (Tuple[int, int]): The size of the score/highscore icons. (default: (32, 32))
        """
        self.display = display
        self.spacing = spacing
        
        self.icon_size: Tuple[int, int] = icon_size
        if self.icon_size is None:
            self.icon_size = (32, 32)
            
        self.score_icon = pygame.image.load(score_icon_path).convert_alpha()
        self.score_icon = pygame.transform.scale(self.score_icon, self.icon_size)
        
        self.highscore_icon = pygame.image.load(highscore_icon_path).convert_alpha()
        self.highscore_icon = pygame.transform.scale(self.highscore_icon, self.icon_size)
        
        self.on_new_highscore: Callable = None
        
        self.font = font
        self._score: int = 0
        self.highscore: int = 0
        
    @property
    def score(self) -> int:
        return self._score
    
    @score.setter
    def score(self, val: int) -> None:
        self._score = val
        self.update_highscore()
        
    def update_highscore(self) -> None:
        if self.score > self.highscore:
            self.highscore = self.score
            if self.on_new_highscore is not None:
                self.on_new_highscore(self.highscore)
            
    def increment_score(self) -> None:
        """Increment the score by 1."""
        self.score += 1
        
    def reset_score(self) -> None:
        """Reset the score to 0."""
        self.score = 0
        
    def __get_rects(self, 
                  icon: pygame.Surface,
                  font: pygame.Surface,
                  spacing: int,
                  coords: Tuple[int, int],
                  ) -> Tuple[pygame.Rect, pygame.Rect]:
        """
        Calculates the positions and generates pygame.Rect objects
        for the icon and the font, based on the provided icon surface,
        font surface, spacing, and coordinates.
        """
        icon_width, icon_height = icon.get_width(), icon.get_height()
        font_width, font_height = font.get_width(), font.get_height()
        total_width = icon_width + spacing + font_width
        total_height = max(icon_height, font_height)
        
        rect_frame = pygame.Rect(0, 0, total_width, total_height)
        rect_frame.center = coords
        
        icon_rect = icon.get_rect(midleft = rect_frame.midleft)
        font_rect = font.get_rect(midright = rect_frame.midright)
        
        return (icon_rect, font_rect)

    def render_score(self, 
                     coords: Tuple[int, int],
                     text: str = "$", 
                     ) -> None:
        """
        Render the score on the display surface.

        Parameters:
            coords (Tuple[int, int]): The coordinates for rendering the score (anchor: center).
            text (str): The text template for the score. '$' is replaced with self.score. (default: "$")
        """
        text = text.replace("$", str(self.score))
        score_font = self.font.render(text, True, "white")
        icon_rect, font_rect = self.__get_rects(
            icon=self.score_icon,
            font=score_font,
            spacing=self.spacing,
            coords=coords,
        )
        self.display.blit(self.score_icon, icon_rect)
        self.display.blit(score_font, font_rect)
        
    def render_highscore(self, 
                         coords: Tuple[int, int],
                         text: str = "$", 
                         ) -> None:
        """
        Render the high score on the display surface.

        Parameters:
            coords (Tuple[int, int]): The coordinates for rendering the high score (anchor: center).
            text (str): The text template for the highscore. '$' is replaced with self.highscore. (default: "$")
        """
        text = text.replace("$", str(self.highscore))
        highscore_font = self.font.render(text, True, "white")
        icon_rect, font_rect = self.__get_rects(
            icon=self.highscore_icon,
            font=highscore_font,
            spacing=self.spacing,
            coords=coords,
        )
        self.display.blit(self.highscore_icon, icon_rect)
        self.display.blit(highscore_font, font_rect)
        
    def render(self, 
               score_coords: Tuple[int, int], 
               highscore_coords: Tuple[int, int],
               score_text: str = "$",
               highscore_text: str = "$"
               ) -> None:
        """
        Render the score and highscore on the display surface.

        Parameters:
            score_coords (Tuple[int, int]): The coordinates for rendering the score.
            highscore_coords (Tuple[int, int]): The coordinates for rendering the highscore.
            score_text (str): The text template for the score. '$' is replaced with self.score. (default: "$")
            highscore_text (str): The text template for the highscore. '$' is replaced with self.highscore. (default: "$")
        """
        self.render_score(score_coords, score_text)
        self.render_highscore(highscore_coords, highscore_text)
        