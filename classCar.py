import pygame as py
from math import pi, atan2, degrees, sqrt, cos, sin;

class Car:
    def __init__(self, game, brain, tmpSurface):
        self.game = game;
        self.screen = game.screen;
        self.angle = pi;
        self.maxTurn = pi/120;
        self.speed = 0;
        self.maxSpeed = 10;
        self.minSpeed = 1;
        self.x = 90;
        self.y = 660;
        self.tmpSurface = tmpSurface;
        self.first = False;
        self.imgOrigin = {'blue':{}, 'green':{}};
        for i in [0,1,2,3,4,5,6,-1,-2,-3,-4,-5,-6]:
            self.imgOrigin['blue'][i] = py.transform.scale(py.image.load(f"assets/car{str(i)}.png"),(100, 100))
            self.imgOrigin['green'][i] = py.transform.scale(py.image.load(f"assets/car{str(i)}First.png"),(100, 100))

        self.imgControl = {
            "left":[py.transform.scale(py.image.load(f"assets/left.png"),(50, 50)),py.transform.scale(py.image.load(f"assets/leftPushed.png"),(50, 50))],
            "right":[py.transform.scale(py.image.load(f"assets/right.png"),(50, 50)),py.transform.scale(py.image.load(f"assets/rightPushed.png"),(50, 50))],
            "engine":[py.transform.scale(py.image.load(f"assets/engine.png"),(50, 50)),py.transform.scale(py.image.load(f"assets/enginePushed.png"),(50, 50))],
            "brake":[py.transform.scale(py.image.load(f"assets/brake.png"),(50, 50)),py.transform.scale(py.image.load(f"assets/brakePushed.png"),(50, 50))],
                           }

        self.turn = 0;
        self.turning = False;
        self.ko = False;
        self.score=0;
        self.scoreFinal =0;
        self.lenRay = 400;
        self.demo = False;
        self.brain = brain;
        self.compteurMouv = 0;
    
        #controls
        self.leftA=False;
        self.rightA=False;
        self.engineA=False;
        self.brakeA=False;

        self.indexImg = 0;
    
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
            self.leftA = False;
            self.rightA = False;
            self.brakeA = False;
            self.engineA = False;
        
            score = self.score
            self.score = self.game.roadAdvance.advance(self, self.game.compteur, self.score);
            if(score < self.score):
                self.compteurMouv =0;
            else:
                self.compteurMouv +=1;
                if(self.compteurMouv >=70):
                    self.die();
           
            #calcul des lasers
            xStart, yStart = (self.x, self.y)
            tabRes = []
            tabInput = []
            angleUnit = pi*5/48

            for angle in [self.angle+4*angleUnit, self.angle+3*angleUnit, self.angle+2*angleUnit, self.angle+angleUnit, self.angle, self.angle-angleUnit, self.angle - 2*angleUnit, self.angle - 3*angleUnit, self.angle-4*angleUnit]:
                self.tmpSurface.fill((0,0,0,0));
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
                    
                    tabInput.append(lenght*2-1);
                else:
                    tabInput.append(1);
            
            #ajout moteur et volant aux données
            tabInput.append(self.speed/self.maxSpeed);
            tabInput.append(self.turn/self.maxTurn);

            self.acting(tabInput);



            if self.score == len(self.game.roadAdvance.listPts):
                self.die()

        if(self.first):
            img = py.transform.rotate(self.imgOrigin['green'][self.indexImg], degrees(self.angle));
        else:
            img = py.transform.rotate(self.imgOrigin['blue'][self.indexImg], degrees(self.angle));


        self.screen.blit(img, (x + self.x*2 - img.get_width()/2, y + self.y*2 - img.get_height()/2));

        self.first = False;
            

    def acting(self, inputs):
        act = self.brain.forward(inputs);
        for k in range(4):
            if(act[k]>0.75 and k ==0):
                self.accelerate();
            if(act[k]>0.75 and k==1):               
                self.brake();
            if(act[k]>0.75 and k==2):
                self.left();
            if(act[k]>0.75 and k==3):
                self.right();

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
        if(self.speed < 10):
            self.speed +=0.1;

    def brake(self):
        self.brakeA=True;
        if(self.speed >self.minSpeed):
            self.speed -=0.4;

    def calculScore(self):
        return self.score*400 - self.game.compteur;

    def die(self):
        self.ko = True;
        self.game.lives -= 1;
        if self.score == len(self.game.roadAdvance.listPts):
                        self.scoreFinal = self.calculScore();
                        self.scoreFinal += 500;
        else:
            self.scoreFinal = self.calculScore();

    def showData(self):
        self.first = True;
        if(self.engineA):
            self.screen.blit(self.imgControl["engine"][1], (90, 80));
        else:
            self.screen.blit(self.imgControl["engine"][0], (90, 80));

        if(self.brakeA):
            self.screen.blit(self.imgControl["brake"][1], (30, 80));
        else:
            self.screen.blit(self.imgControl["brake"][0], (30, 80));

        if(self.leftA):
            self.screen.blit(self.imgControl["left"][1], (30, 30));
        else:
            self.screen.blit(self.imgControl["left"][0], (30, 30));

        if(self.rightA):
            self.screen.blit(self.imgControl["right"][1], (90, 30));
        else:
            self.screen.blit(self.imgControl["right"][0], (90, 30));
