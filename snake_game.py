import pygame
import sys

from sprites.snake import Snake

pygame.init()

SCREENWIDTH = 1150
SCREENHEIGHT = 760
FPS = 30

display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

snake = Snake(display, 15, 15, outline_width=2)

pygame.display.set_caption("Snake game by Dhyanesh!")

while True:
    display.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.up()
            elif event.key == pygame.K_DOWN:
                snake.down()
            elif event.key == pygame.K_LEFT:
                snake.left()
            elif event.key == pygame.K_RIGHT:
                snake.right()
            elif event.key == pygame.K_SPACE:
                snake.extend()
            
    snake.render()
            
    pygame.display.update()
    clock.tick(FPS)
    