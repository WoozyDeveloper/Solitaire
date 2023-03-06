import pygame


img = pygame.image.load('img/BACK.png')

white = (255, 64, 64)

w = 640
h = 480
screen = pygame.display.set_mode((w, h))

screen.fill((white))

running = 1
x = 5
y = 5
while running:
    x += 1
    y += 1
    screen.fill((white))
    screen.blit(img, (x, y))
    pygame.display.flip()
    pygame.display.update()
