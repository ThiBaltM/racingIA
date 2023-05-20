import pygame as py
from classCar import Car
from classRoad import Road
from classNeuron import NeuralNetwork
import random
import json
py.font.init()

class Game:
    def __init__(self, screen):
        self.screen = screen;
        self.pressed = {py.K_e : False,1: False, py.K_z:False, py.K_s:False, py.K_q:False, py.K_d:False};
        self.compteur = 0;
        self.screenHeight, self.screenWidth = (self.screen.get_height(),self.screen.get_width());
        self.score = 0;
        self.pop = 15;
        self.road = py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth, self.screenHeight));
        self.trackBorder = json.load(open("roadCollides.json"))
        self.x = 0;
        self.y=0;
        self.roadAdvance = Road(self);
        self.tmpSurface = py.Surface((self.screenWidth, self.screenHeight), py.SRCALPHA)
        self.listCar = [];
        for _ in range (self.pop):
            self.listCar.append(Car(self, NeuralNetwork(10, 7, 4), self.tmpSurface));
        self.lives = self.pop;


          
    def update(self):
        """Cette fonction met a jour les evenement divers pouvant avoir lieux"""
        py.draw.rect(self.screen, "white", py.Rect(0,0,self.screen.get_width(), self.screen.get_height()));
        print(self.compteur);
        print(self.lives);
        self.listCar.sort(key=lambda x:x.score);
        self.listCar[-1].showData();
        if(self.lives<=0):
            self.listCar.sort(key=lambda x:x.scoreFinal, reverse=True);

            self.lives = self.pop;
            nListCar =[];
            for k in range (3):
                nListCar.append(Car(self, self.listCar[k].brain, self.tmpSurface ));
            for k in range (3, 12):
                p1 = self.listCar[random.randint(0,3)]
                p2 = self.listCar[random.randint(0,3)]
                nListCar.append(Car(self, NeuralNetwork(data=p1.brain.export(), data2=p2.brain.export()), self.tmpSurface));
            for k in range(12,15):
                nListCar.append(Car(self,NeuralNetwork(10,7,4), self.tmpSurface))
            
            self.listCar = nListCar;


        #myfont = py.font.SysFont('Impact', self.screen.get_width() // 74)
        #textScoreSurface = myfont.render(f"your score :{self.car.calculScore()}", False, (0,0,0))
        #self.screen.blit(textScoreSurface,(10,10))

        """
        #gestion joueur
        if self.pressed[py.K_z]:
            self.listCar[0].accelerate()
        if self.pressed[py.K_s]:
            self.listCar[0].brake()
        if self.pressed[py.K_q]:
            self.listCar[0].left()
        if self.pressed[py.K_d]:
            self.listCar[0].right()
        """
        
        

        
            
        self.screen.blit(self.road, (0,0));
        for car in self.listCar:
            car.disp();
        
        self.compteur += 1;
