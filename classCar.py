import pygame as py
from math import pi, atan2, degrees, sqrt, cos, sin;

class Car:
    def __init__(self, game, brain, tmpSurface):
        self.game = game;
        self.screen = game.screen;
        self.angle = pi;
        self.outputs = [0,0];
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
        self.tabInput = [0 for _ in range(10)];
    
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
            self.tabInput = []
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
                    
                    self.tabInput.append(lenght);
                else:
                    self.tabInput.append(1);
            
            #ajout moteur et volant aux données
            self.tabInput.append(self.speed/self.maxSpeed);
            self.tabInput.append(self.turn/self.maxTurn);

            self.acting(self.tabInput);



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
        self.outputs = act;
        for k in range(2):
            if(act[k]>0.52 and k ==0):
                self.accelerate();
            elif(act[k]<0.48 and k == 0):
                self.brake();
            if(act[k]>0.52 and k==1):               
                self.left();
            elif(act[k]<48 and k==1):
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
        
        self.dispNeuralNetwork()
    

    def dispNeuralNetwork(self):
        x = 800;
        y = 10;
        font = py.font.SysFont(None, 16)

        #input layer
        for i in range(10):
            if(self.tabInput[i]>0):
                img = font.render(str(round(self.tabInput[i],2)), True, (10,200,10))
            else:
                img = font.render(str(round(self.tabInput[i],2)), True, (200,10,10))
            
            self.screen.blit(img, (x,y+24*i))

            for j in range(8):
                if(self.brain.weights1[j][i] > 0):
                    py.draw.line(self.screen, (10,200,10), (x+20,y+24*i+12), (x+115,y+30*j+15), width=round(self.brain.weights1[j][i]*3))
                else:
                    py.draw.line(self.screen, (200,10,10), (x+20,y+24*i+12), (x+115,y+30*j+15), width=abs(round(self.brain.weights1[j][i]*3)))

        #hidden layer 1
        for i in range(8):
            if(self.brain.bias1[i] >0):
                py.draw.circle(self.screen, (10,200,10), (x+115,y+30*i+15), self.brain.bias1[i]*10);
            else:
                py.draw.circle(self.screen, (200,10,10), (x+115,y+30*i+15), abs(self.brain.bias1[i]*10));
            
            for j in range(5):
                if(self.brain.weights2[j][i] > 0):
                    py.draw.line(self.screen, (10,200,10), (x+115,y+30*i+15), (x+215,y+48*j+24), width=round(self.brain.weights2[j][i]*3))
                else:
                    py.draw.line(self.screen, (200,10,10), (x+115,y+30*i+15), (x+215,y+48*j+24), width=abs(round(self.brain.weights2[j][i]*3)))

        #hidden layer 2
        for i in range(5):
            if(self.brain.bias2[i] >0):
                py.draw.circle(self.screen, (10,200,10), (x+215,y+48*i+24), self.brain.bias2[i]*10);
            else:
                py.draw.circle(self.screen, (200,10,10), (x+215,y+48*i+24), abs(self.brain.bias2[i]*10));
            
            for j in range(2):
                if(self.brain.weights3[j][i] > 0):
                    py.draw.line(self.screen, (10,200,10), (x+215,y+48*i+24), (x+315,y+120*j+60), width=round(self.brain.weights3[j][i]*3))
                else:
                    py.draw.line(self.screen, (200,10,10), (x+215,y+48*i+24), (x+315,y+120*j+60), width=abs(round(self.brain.weights3[j][i]*3)))

        #output layer
        for i in range(2):
            if(self.brain.bias3[i]>0):
                py.draw.circle(self.screen, (10,200,10), (x+315,y+120*i+60), self.brain.bias2[i]*10)
            else:
                py.draw.circle(self.screen, (200,10,10), (x+315,y+120*i+60), abs(self.brain.bias2[i]*10))
            
            if(self.outputs[i]>0):
                img = font.render(str(round(self.tabInput[i],2)), True, (10,200,10))
            else:
                img = font.render(str(round(self.tabInput[i],2)), True, (200,10,10))
            
            self.screen.blit(img, (x+330,y+120*i+56))


                        



