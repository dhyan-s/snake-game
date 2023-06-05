import pygame
from typing import Tuple, List


class Score:
    def __init__(self,
                 display: pygame.Surface,
                 score_icon_path: pygame.Surface,
                 highscore_icon_path: pygame.Surface,
                 font: pygame.font.Font,
                 spacing: int = 10,
                 icon_size: Tuple[int, int] = None,
                 ):
        self.display = display
        self.spacing = spacing
        
        self.icon_size = icon_size
        if self.icon_size is None:
            self.icon_size = (32, 32)
            
        self.score_icon = pygame.image.load(score_icon_path).convert_alpha()
        self.score_icon = pygame.transform.scale(self.score_icon, self.icon_size)
        
        self.highscore_icon = pygame.image.load(highscore_icon_path).convert_alpha()
        self.highscore_icon = pygame.transform.scale(self.highscore_icon, self.icon_size)
        
        self.font = font
        self._score = 0
        self.highscore = 0
        
    @property
    def score(self) -> int:
        return self._score
    
    @score.setter
    def score(self, val: int) -> None:
        self._score = val
        self.update_highscore()
        
    def update_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            
    def increment_score(self):
        self.score += 1
        
    def reset_score(self):
        self.score = 0
        
    def get_rects(self, 
                       icon: pygame.Surface,
                       font: pygame.Surface,
                       spacing: int,
                       coords: Tuple[int, int],
                       ) -> Tuple[pygame.Rect, pygame.Rect]:
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
        text = text.replace("$", str(self.score))
        score_font = self.font.render(text, True, "white")
        icon_rect, font_rect = self.get_rects(
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
        text = text.replace("$", str(self.highscore))
        highscore_font = self.font.render(text, True, "white")
        icon_rect, font_rect = self.get_rects(
            icon=self.highscore_icon,
            font=highscore_font,
            spacing=self.spacing,
            coords=coords,
        )
        self.display.blit(self.highscore_icon, icon_rect)
        self.display.blit(highscore_font, font_rect)
        
    def render(self, 
                score_coords: Tuple[int, int], 
                highscore_coords: Tuple[int, int]
            ) -> None:
        self.render_score(score_coords)
        self.render_highscore(highscore_coords)
        