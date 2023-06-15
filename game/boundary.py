import pygame

class Boundary:
    def __init__(self, 
                 display: pygame.Surface,
                 color: str = "red",
                 thickness: int = 8,
                 stats_sep_y_offset = 65,
                 ) -> None:
        self.display = display
        
        self.color = color
        self.thickness = thickness
        self.stats_sep_y_offset = stats_sep_y_offset
        self.update_rects()
        
    def update_rects(self) -> None:
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
        pygame.draw.rect(self.display, self.color, self.top_line)
        pygame.draw.rect(self.display, self.color, self.bottom_line)
        pygame.draw.rect(self.display, self.color, self.left_line)
        pygame.draw.rect(self.display, self.color, self.right_line)
        
        pygame.draw.rect(self.display, self.color, self.stats_separator)
        pygame.draw.rect(self.display, self.color, self.score_separator)
        pygame.draw.rect(self.display, self.color, self.highscore_separator)
        