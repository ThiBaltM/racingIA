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
        self.maxSpeed = 4;
        self.x = 220;
        self.y = 620;
        self.first = False;
        self.imgOrigin = [];
        for i in [0,1,2,3,4,5,6,-1,-2,-3,-4,-5,-6]:
            self.imgOrigin.append(py.transform.scale(py.image.load(f"assets/car{str(i)}First.png"),(100, 100)))

        self.turn = 0;
        self.turning = False;

        self.compteurMouv = 0;
    
        self.indexImg = 0;

    def disp(self,x,y):

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


        self.turning = False;

        img = py.transform.rotate(self.imgOrigin[self.indexImg], degrees(self.angle));

        self.screen.blit(img, (x + self.x*2 - img.get_width()/2, y + self.y*2 - img.get_height()/2));


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
            self.speed +=0.025;

    def brake(self):
        self.brakeA=True;
        if(self.speed >0.4):
            self.speed -=0.08;