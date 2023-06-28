import pygame as py
from playingMode.classCar import Car
from playingMode.classCarPlayer import CarPlayer
from playingMode.classRoad import Road
from playingMode.classNeuron import NeuralNetwork
import random
import json

py.font.init()

class Game:
    def __init__(self, screen):
        self.screen = screen;
        self.pressed = {py.K_e : False,1: False, py.K_z:False, py.K_s:False, py.K_q:False, py.K_d:False};
        self.compteur = 0;
        self.screenHeight, self.screenWidth = (self.screen.get_height(),self.screen.get_width());

        self.road = [py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth, self.screenHeight)),py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth*2, self.screenHeight*2))];
        self.trackBorder = json.load(open("roadCollides.json"))
        self.x = 0;
        self.y=0;
        self.roadAdvance = Road(self);
        self.layer = [9,12,8,2]

        self.car = CarPlayer(self);

        try:
            file = open("genSave.json", 'r')
            data = json.load(file)

            self.ennemiCar = Car(self, NeuralNetwork(data = data["listCar"][0]));
            print("fichier sauvegarde lu")
            


        except IOError:
            print("pas de sauvegarde trouvée, lancement d'une nouvelle simulation")

            self.ennemiCar = Car(self, NeuralNetwork(self.layer[0],self.layer[1],self.layer[2],self.layer[3]));


        self.clock = py.time.Clock();
        self.fps = 60;


          
    def update(self):
        """Cette fonction met a jour les evenement divers pouvant avoir lieux"""
        self.clock.tick(self.fps);
        py.draw.rect(self.screen, (22,73,0), py.Rect(0,0,self.screen.get_width(), self.screen.get_height()));
        self.car.disp(0,0);

        #myfont = py.font.SysFont('Impact', self.screen.get_width() // 74)
        #textScoreSurface = myfont.render(f"your score :{self.car.calculScore()}", False, (0,0,0))
        #self.screen.blit(textScoreSurface,(10,10))

        #gestion joueur
        if self.pressed[py.K_z]:
            self.car.accelerate()
        if self.pressed[py.K_s]:
            self.car.brake()
        if self.pressed[py.K_q]:
            self.car.left()
        if self.pressed[py.K_d]:
            self.car.right()


        x,y = self.car.x, self.car.y;
        x,y = (-2*x+self.screenWidth/2,-2*y+self.screenHeight/2)
        self.screen.blit(self.road[int(self.actionCamera)], (x,y));

        self.ennemiCar.disp(x,y);
        
        self.compteur += 1;
