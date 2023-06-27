import pygame as py
from classGame import Game
from classNeuron import NeuralNetwork

#initialisation valeurs plateau
largeurEcran, hauteurEcran = (1280, 720)
#paramétrage de l'affichage
screen = py.display.set_mode((largeurEcran,hauteurEcran))




isRunning = True

game = Game(screen)

while isRunning:
    #gestion des touches
    for event in py.event.get():
        """
        k = py.key.get_pressed()
        if k[py.K_UP]:
            game.car.pressed[py.K_UP]=True;
        if k[py.K_DOWN]:
            game.car.brake();
        if k[py.K_RIGHT]:
            game.car.right();
        if k[py.K_LEFT]:
            game.car.left();
        """
        if event.type == py.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == py.KEYUP:
            game.pressed[event.key] = False
        elif event.type == py.QUIT: #fermeture de la page
            isRunning = False
        elif event.type == py.MOUSEBUTTONDOWN:
            game.pressed[event.button] = True
            #initializing road
            game.roadAdvance.draw()
        
        elif event.type == py.MOUSEBUTTONUP:
            game.pressed[event.button] = False
    game.update()

    """
    #show road advancement points for initializing it
    for a in game.roadAdvance.list:
        py.draw.circle(screen,'red',a,5,5);
    print(game.roadAdvance.list)
    """
    
    
    py.display.flip()

