import pygame
from classMenu import *


# générer la fenêtre de notre jeu
pygame.display.set_caption("Intellicar")
screen = pygame.display.set_mode((1280, 720))

running = True
mode = Menu(screen)

while running:
    pygame.display.flip()
    mode.update()