import pygame as py
from math import pi, atan2, degrees, sqrt, cos, sin;

class CarPlayer:
    def __init__(self, game):
        self.game = game;
        self.screen = game.screen;
        self.angle = pi/0.95;
        self.outputs = [0,0];
        self.maxTurn = pi/120;
        self.speed = 0;
        self.maxSpeed = 5;
        self.x = 220;
        self.y = 620;
        self.first = False;
        self.imgOrigin = [{'blue':{}, 'green':{}},{'blue':{}, 'green':{}}];
        for i in [0,1,2,3,4,5,6,-1,-2,-3,-4,-5,-6]:
            self.imgOrigin[0]['blue'][i] = py.transform.scale(py.image.load(f"assets/car{str(i)}First.png"),(50, 50))
            self.imgOrigin[0]['green'][i] = py.transform.scale(py.image.load(f"assets/car{str(i)}First.png"),(50, 50))
            self.imgOrigin[1]['blue'][i] = py.transform.scale(py.image.load(f"assets/car{str(i)}First.png"),(100, 100))
            self.imgOrigin[1]['green'][i] = py.transform.scale(py.image.load(f"assets/car{str(i)}First.png"),(100, 100))
        self.turn = 0;
        self.turning = False;
        self.ko = False;
        self.score=0;
        self.scoreFinal =0;
        self.lenRay = 250;
        self.demo = False;
        self.compteurMouv = 0;
    
        self.indexImg = 0;
        self.tabInput = [0 for _ in range(11)];

    def disp(self,x,y):
        if(not self.ko):
            if(not self.turning):
                if(self.turn > 0):
                    self.turn -= pi/4800;
                elif(self.turn<0):
                    self.turn += pi/4800;
                
            self.x -= cos(self.angle)*self.speed;
            self.y += sin(self.angle)*self.speed;
            self.angle += self.turn;

            if(self.speed <1):
                self.indexImg = round(self.turn/self.maxTurn)*6;
            else:
                self.indexImg = round(round(self.turn/self.maxTurn)*6/(round(self.speed)*(2/9)+(7/9)));



            """
            #collide
            carMask = py.mask.from_surface(self.img);
            offset = (int((self.x-self.img.get_width()/2)- self.game.x), int((self.y-self.img.get_height()/2) - self.game.y));
            poi = self.game.trackBorder.overlap(carMask, offset);
            
            if(poi != None):
                self.die();
            """
            self.turning = False;
        if(self.first):
            img = py.transform.rotate(self.imgOrigin[int(self.game.actionCamera)]['green'][self.indexImg], degrees(self.angle));
        else:
            img = py.transform.rotate(self.imgOrigin[int(self.game.actionCamera)]['blue'][self.indexImg], degrees(self.angle));

    def left(self):
        self.leftA=True;
        if(self.turn<= self.maxTurn and self.speed !=0):
            self.turn += pi/1200;
        self.turning = True;

    def right(self):
        self.rightA=True;
        if(self.turn >= -self.maxTurn and self.speed !=0):
            self.turn -= pi/1200;
        self.turning = True;

    def accelerate(self):
        self.engineA = True;
        if(self.speed < self.maxSpeed):
            self.speed +=0.1;

    def brake(self):
        self.brakeA=True;
        if(self.speed >self.minSpeed):
            self.speed -=0.4;