import pygame as py
from classMenu import *
from classGame import Game
from playingMode.classGame import Game as PlayingGame


# générer la fenêtre de notre jeu
pygame.display.set_caption("Intellicar")
screen = pygame.display.set_mode((1280, 720))

running = True
mode = Menu(screen)

while running:
    pygame.display.flip()
    if mode.jeuLance:
        playingGame.update()
    elif mode.simuLance:
        game.update()
    else:
        mode.update()

    for event in pygame.event.get():
        # evenement quitte
        if event.type == py.KEYDOWN and mode.jeuLance:
            playingGame.pressed[event.key] = True
        elif event.type == py.KEYUP and mode.jeuLance:
            playingGame.pressed[event.key] = False
        elif event.type == py.MOUSEBUTTONDOWN and mode.menuLance:
            if mode.rectJouer.collidepoint(event.pos):
                playingGame = PlayingGame(screen)
                mode.menuLance = False 
                mode.jeuLance = True 
            
            if mode.rectSimuler.collidepoint(event.pos):

                game = Game(screen)
                mode.menuLance = False 
                mode.simuLance = True 

            if mode.rectQuitter.collidepoint(event.pos):
                running = False 

        elif event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION and mode.menuLance:
            # enlever la selection si on ne passe pas sur les boutons 
            mode.cliquerJouer = False 
            mode.cliquerQuitter = False
            mode.cliquerSimuler = False 

            if mode.rectJouer.collidepoint(pygame.mouse.get_pos()):
                mode.cliquerJouer = True 
            elif mode.rectQuitter.collidepoint(pygame.mouse.get_pos()):
                mode.cliquerQuitter = True
            elif mode.rectSimuler.collidepoint(pygame.mouse.get_pos()):
                mode.cliquerSimuler = True