import pygame as py
from math import pi, atan2, degrees, sqrt, cos, sin;


class Car:
    def __init__(self, game, brain):
        self.game = game;
        self.screen = game.screen;
        self.angle = pi/0.95;
        self.outputs = [0,0];
        self.maxTurn = pi/60;
        self.speed = 0;
        self.maxSpeed = 10;
        self.x = 220;
        self.y = 620;
        self.first = False;
        self.imgOrigin = [];
        for i in [0,1,2,3,4,5,6,-1,-2,-3,-4,-5,-6]:
            self.imgOrigin.append( py.transform.scale(py.image.load(f"assets/car{str(i)}.png"),(100, 100)))

        self.turn = 0;
        self.turning = False;
        self.ko = False;
        self.score=0;
        self.scoreFinal =0;
        self.lenRay = 250;
        self.demo = False;
        self.brain = brain;
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
           
            #calcul des lasers
            xStart, yStart = (self.x, self.y)
            tabRes = []
            self.tabInput = []
            angleUnit = pi*5/48

            for angle in [self.angle+4*angleUnit, self.angle+3*angleUnit, self.angle+2*angleUnit, self.angle+angleUnit, self.angle, self.angle-angleUnit, self.angle - 2*angleUnit, self.angle - 3*angleUnit, self.angle-4*angleUnit]:
                for k in range(0, self.lenRay, 4): #4 correspond to the unit of collisionMaker
                   
                    targetX, targetY = (xStart - k * cos(angle), yStart + k * sin(angle))
                    if self.game.trackBorder[round(targetY/4)][round(targetX/4)]:
                        break;
                
                tabRes.append((targetX,targetY));

                # Affichage de la ligne sur l'écran
                if(self.demo):
                    py.draw.line(self.screen, (30, 100, 100), (xStart, yStart), (targetX,targetY), 2)
            for coords in tabRes:
                if(coords!=None):
                    v = sqrt((xStart - coords[0])**2+(yStart - coords[1])**2);
                    lenght = v/self.lenRay;
                    if(v<15):
                        self.die();
                        break;
                    
                    self.tabInput.append(lenght);
                else:
                    self.tabInput.append(1);

            self.acting(self.tabInput);




        img = py.transform.rotate(self.imgOrigin[self.indexImg], degrees(self.angle));

        self.screen.blit(img, (x + self.x*2 - img.get_width()/2, y + self.y*2 - img.get_height()/2));

        
            

    def acting(self, inputs):
        act = self.brain.forward(inputs);
        self.outputs = act;

        self.turn = -self.maxTurn+ act[0] * (2*self.maxTurn)
        self.speed = act[1]*self.maxSpeed
