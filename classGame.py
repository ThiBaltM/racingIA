import pygame as py
from classCar import Car
from classRoad import Road
from classNeuron import NeuralNetwork
py.font.init()

class Game:
    def __init__(self, screen):
        self.screen = screen;
        self.pressed = {py.K_e : False,1: False, py.K_z:False, py.K_s:False, py.K_q:False, py.K_d:False};
        self.compteur = 0;
        self.screenHeight, self.screenWidth = (self.screen.get_height(),self.screen.get_width());
        self.score = 0;
        self.road = py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth, self.screenHeight));
        self.trackBorder = py.mask.from_surface(self.road);
        self.x = 0;
        self.y=0;
        self.roadAdvance = Road(self);
        self.listCar = [];
        for _ in range (5):
            self.listCar.append(Car(self, NeuralNetwork(8, 6, 4)));
        self.lives = 5;


          
    def update(self):
        """Cette fonction met a jour les evenement divers pouvant avoir lieux"""
        py.draw.rect(self.screen, "white", py.Rect(0,0,self.screen.get_width(), self.screen.get_height()));
        print(self.compteur);
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
