import pygame

class Boundary:
    """
    Represents the boundary lines in the game display.

    This class is responsible for rendering the boundary lines on a display surface.
    It defines the visual appearance and positioning of the boundary lines, including the top,
    bottom, left, right lines, as well as the separators for displaying game statistics.
    """
    def __init__(self, 
                 display: pygame.Surface,
                 color: str = "red",
                 thickness: int = 8,
                 stats_sep_y_offset = 65,
                 ) -> None:
        """
        Parameters:
            - display (pygame.Surface): The display surface to render the boundary on.
            - color (str): The color of the boundary lines. (default: "red")
            - thickness (int): The thickness of the boundary lines. (default: 8)
            - stats_sep_y_offset (int): The y-offset for the stats separator line. (default: 65)
        """
        self.display = display
        
        self.color = color
        self.thickness = thickness
        self.stats_sep_y_offset = stats_sep_y_offset
        self.update_rects()
        
    def update_rects(self) -> None:
        """Update the boundary and stat Rects based on the display size."""
        display_width = self.display.get_width()
        display_height = self.display.get_height()
        
        highscore_separator_x = int(display_width / 4)
        score_separator_x = display_width - highscore_separator_x
        
        self.top_line = pygame.Rect(0, 0, display_width, self.thickness + 1.5)
        self.left_line = pygame.Rect(0, 0, self.thickness, display_height)
        self.right_line = pygame.Rect(display_width - self.thickness, 0, self.thickness, display_height)
        self.bottom_line = pygame.Rect(0, display_height - self.thickness, display_width, self.thickness)
        
        stats_sep_y = display_height - self.stats_sep_y_offset
        
        self.stats_separator = pygame.Rect(0, stats_sep_y, display_width, self.thickness)
        self.score_separator = pygame.Rect(score_separator_x, stats_sep_y, self.thickness, self.stats_sep_y_offset)
        self.highscore_separator = pygame.Rect(highscore_separator_x, stats_sep_y, self.thickness, self.stats_sep_y_offset)
        
    def render(self) -> None:
        """Render the boundary lines on the display surface."""
        pygame.draw.rect(self.display, self.color, self.top_line)
        pygame.draw.rect(self.display, self.color, self.bottom_line)
        pygame.draw.rect(self.display, self.color, self.left_line)
        pygame.draw.rect(self.display, self.color, self.right_line)
        
        pygame.draw.rect(self.display, self.color, self.stats_separator)
        pygame.draw.rect(self.display, self.color, self.score_separator)
        pygame.draw.rect(self.display, self.color, self.highscore_separator)
        