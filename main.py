import pygame as py
from classGame import Game
from classNeuron import NeuralNetwork

#initialisation valeurs plateau
largeurEcran, hauteurEcran = (1280, 720)
#paramétrage de l'affichage
screen = py.display.set_mode((largeurEcran,hauteurEcran))

isRunning = True

game = Game(screen)

"""
#show road advancement points for initializing it
for a in game.roadAdvance.list:
py.draw.circle(screen,'red',a,5,5);
print(game.roadAdvance.list)
"""


