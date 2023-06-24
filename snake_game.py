import pygame
import sys
import ctypes

from game import Game

ctypes.windll.shcore.SetProcessDpiAwareness(1)

pygame.init()

SCREENWIDTH = 1150
SCREENHEIGHT = 760
FPS = 30

display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

game = Game(display)

pygame.display.set_caption("Snake game by Dhyanesh!")

icon = pygame.image.load("assets/icon.png").convert_alpha()
pygame.display.set_icon(icon)

while True:
    display.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            game.handle_event(event)
            
    game.render()
            
    pygame.display.update()
    clock.tick(FPS)
    