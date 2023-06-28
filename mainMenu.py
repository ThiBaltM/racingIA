import pygame
from classMenu import *
from main import *


# générer la fenêtre de notre jeu
pygame.display.set_caption("Intellicar")
screen = pygame.display.set_mode((1280, 720))

running = True
mode = Menu(screen)
game = Game(screen)

while running:
    pygame.display.flip()
    if mode.jeuLance:
        game.update()
    else:
         mode.update()

    for event in pygame.event.get():
        # evenement quitte
        if event.type == py.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == py.KEYUP:
            game.pressed[event.key] = False
        elif event.type == py.MOUSEBUTTONDOWN:
            if mode.rectJouer.collidepoint(event.pos):
                mode.menuLance = False 
                mode.jeuLance = True 

            if mode.rectQuitter.collidepoint(event.pos):
                running = False 
            game.pressed[event.button] = True
            #initializing road
            game.roadAdvance.draw()
        
        elif event.type == py.MOUSEBUTTONUP:
            game.pressed[event.button] = False

        elif event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            # enlever la selection si on ne passe pas sur les boutons 
            mode.cliquerJouer = False 
            mode.cliquerQuitter = False 

            if mode.rectJouer.collidepoint(pygame.mouse.get_pos()):
                mode.cliquerJouer = True 
            elif mode.rectQuitter.collidepoint(pygame.mouse.get_pos()):
                mode.cliquerQuitter = True