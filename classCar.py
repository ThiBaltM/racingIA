import pygame as py
from math import pi, atan2, degrees, sqrt, cos, sin;

class Car:
    def __init__(self, game):
        self.game = game;
        self.screen = game.screen;
        self.angle = 0.5*pi;
        self.maxTurn = pi/4;
        self.speed = 0;
        self.x = 100;
        self.y = 300;
        self.imgOrigin = py.transform.scale(py.image.load(f"assets/car.png"),(50, 50));
        self.img = self.imgOrigin;
        self.turn = 0;
        self.turning = False;
        self.ko = False;
        self.score=0;
    
    def disp(self):
        
        if(not self.ko):
            if(not self.turning):
                if(self.turn > 0):
                    self.turn -= pi/4800;
                elif(self.turn<0):
                    self.turn += pi/4800;
                
            self.x -= cos(self.angle)*self.speed;
            self.y += sin(self.angle)*self.speed;
            self.angle += self.turn;

            self.img = py.transform.rotate(self.imgOrigin, degrees(self.angle));

            #collide
            carMask = py.mask.from_surface(self.img);
            offset = (int((self.x-self.img.get_width()/2)- self.game.x), int((self.y-self.img.get_height()/2) - self.game.y));
            poi = self.game.trackBorder.overlap(carMask, offset);
            
            if(poi != None):
                self.ko = True;
            self.turning = False;
        
            self.score = self.game.roadAdvance.advance(self);

        self.screen.blit(self.img, (self.x-self.img.get_width()/2, self.y-self.img.get_height()/2));

    def left(self):
        if(self.turn<= pi/120):
            self.turn += pi/1200;
        self.turning = True;

    def right(self):
        if(self.turn >= -pi/120):
            self.turn -= pi/1200;
        self.turning = True;

    def accelerate(self):
        if(self.speed < 10):
            self.speed +=0.1;

    def brake(self):
        if(self.speed >0.5):
            self.speed -=0.2;