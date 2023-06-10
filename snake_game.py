import pygame
import sys

from game import Game

pygame.init()

SCREENWIDTH = 1150
SCREENHEIGHT = 760
FPS = 30

display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

game = Game(display)

pygame.display.set_caption("Snake game by Dhyanesh!")

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
    