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
        self.pop = 500;
        self.batchTry = 25;
        self.numBatch = 0;
        self.road = py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth, self.screenHeight));
        self.trackBorder = json.load(open("roadCollides.json"))
        self.x = 0;
        self.y=0;
        self.roadAdvance = Road(self);
        self.tmpSurface = py.Surface((self.screenWidth, self.screenHeight), py.SRCALPHA)
        self.listCar = [];
        for _ in range (self.pop):
            self.listCar.append(Car(self, NeuralNetwork(10, 7, 4), self.tmpSurface));
        self.lives = self.batchTry;
        self.gen = 0;


          
    def update(self):
        """Cette fonction met a jour les evenement divers pouvant avoir lieux"""
        py.draw.rect(self.screen, "white", py.Rect(0,0,self.screen.get_width(), self.screen.get_height()));
        if(self.lives<=0):
            self.lives = self.batchTry;
            if((self.numBatch+1)*self.batchTry>=self.pop):
                self.gen +=1;
                self.numBatch = 0;
                self.listCar.sort(key=lambda x:x.scoreFinal, reverse=True);

                nListCar =[];
                for k in range (25):
                    nListCar.append(Car(self, self.listCar[k].brain, self.tmpSurface ));
                for k in range (25, 475):
                    
                    r1 = random.choices(population=[k for k in range(200)], weights=[250-k for k in range(200)], k=1)
                    tmp = [k for k in range(200)]
                    tmp.remove(r1[0])
                    tmp2 = [250-k for k in range(200)]
                    tmp2.remove(250-r1[0])
                    r2 = random.choices(population=tmp, weights=tmp2, k=1)

                    p1 = self.listCar[r1[0]]
                    p2 = self.listCar[r2[0]]
                    nListCar.append(Car(self, NeuralNetwork(data=p1.brain.export(), data2=p2.brain.export()), self.tmpSurface));
                for k in range(475,500):
                    nListCar.append(Car(self,NeuralNetwork(10,7,4), self.tmpSurface))
                
                self.listCar = nListCar;
            else:
                self.numBatch +=1;
                


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
        for car in self.listCar[(self.numBatch*self.batchTry):(self.batchTry*(self.numBatch+1))]:
            car.disp();
        
        #afficher génération
        font = py.font.SysFont(None, 24)
        img = font.render('gen : '+str(self.gen), True, (0,0,0))
        self.screen.blit(img, (20, 10))
        img = font.render('remain : '+str(self.lives), True, (0,0,0))
        self.screen.blit(img, (120, 10))
        img = font.render('batch : '+str(self.numBatch), True, (0,0,0))
        self.screen.blit(img, (240, 10))
        
        self.compteur += 1;
