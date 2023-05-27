import pygame
import sys

pygame.init()

SCREENWIDTH = 1150
SCREENHEIGHT = 760
FPS = 30

display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Snake game by Dhyanesh!")

while True:
    display.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    clock.tick(FPS)