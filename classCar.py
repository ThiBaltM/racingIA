import pygame as py
from math import pi, atan2, degrees, sqrt, cos, sin;

class Car:
    def __init__(self, game, brain):
        self.game = game;
        self.screen = game.screen;
        self.angle = 0.5*pi;
        self.maxTurn = pi/4;
        self.speed = 3;
        self.maxSpeed = 10
        self.x = 120;
        self.y = 300;
        self.imgOrigin = py.transform.scale(py.image.load(f"assets/car.png"),(50, 50));
        self.img = self.imgOrigin;
        self.turn = 0;
        self.turning = False;
        self.ko = False;
        self.score=0;
        self.scoreFinal =0;
        self.lenRay = 300;
        self.demo = False;
        self.brain = brain;
    
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

            """
            #collide
            carMask = py.mask.from_surface(self.img);
            offset = (int((self.x-self.img.get_width()/2)- self.game.x), int((self.y-self.img.get_height()/2) - self.game.y));
            poi = self.game.trackBorder.overlap(carMask, offset);
            
            if(poi != None):
                self.ko = True;
                self.scoreFinal = self.calculScore();
            """
            self.turning = False;
        
            self.score = self.game.roadAdvance.advance(self, self.game.compteur, self.score);
           
            #calcul des lasers
            xStart, yStart = (self.x, self.y)
            tabRes = []
            tabInput = []

            test = py.Surface((self.game.screenWidth, self.game.screenHeight), py.SRCALPHA)
            for angle in [self.angle+3*pi/8, self.angle+pi/4, self.angle+pi/8, self.angle, self.angle-pi/8, self.angle - pi/4, self.angle - 3*pi/8]:
                test.fill((0,0,0,0));
                for k in range(60, self.lenRay+1, 60):
                    # Création d'une surface temporaire pour tracer la ligne
                    py.draw.line(test, (255, 255, 255), (xStart, yStart), (xStart - k * cos(angle), yStart + k * sin(angle)), 2)

                    # Création du masque à partir de la surface temporaire
                    line_mask = py.mask.from_surface(test);

                    # Test de collision entre le masque de la ligne et le masque de la piste
                    collision_offset = (0,0);
                    overlap_mask = self.game.trackBorder.overlap(line_mask, collision_offset);
                    if(overlap_mask != None):
                        # Ajout du résultat de la collision à la liste des résultats
                        break;
                tabRes.append(overlap_mask);

                # Affichage de la ligne sur l'écran
                if(self.demo):
                    if overlap_mask is None:
                        py.draw.line(self.screen, (0, 255, 255), (xStart, yStart), (xStart - self.lenRay * cos(angle), yStart + self.lenRay * sin(angle)), 2)
                    else:
                        collision_coords = overlap_mask;
                        py.draw.line(self.screen, (30, 100, 100), (xStart, yStart), collision_coords, 2)
            for coords in tabRes:
                if(coords!=None):
                    v = sqrt((xStart - coords[0])**2+(yStart - coords[1])**2);
                    lenght = v/self.lenRay;
                    if(v<15):
                        self.ko = True;
                        self.scoreFinal = self.calculScore();
                    
                    tabInput.append(lenght*2-1);
                else:
                    tabInput.append(1);
            
            #ajout moteur et volant aux données
            tabInput.append(self.speed/self.maxSpeed*2-1);
            tabInput.append(self.turn/self.maxTurn);

            print(tabInput)
            self.acting(tabInput);



            if self.score == len(self.game.roadAdvance.listPts):
                self.ko = True;
                self.score = self.calculScore();
                self.score += 500;

        self.screen.blit(self.img, (self.x-self.img.get_width()/2, self.y-self.img.get_height()/2));

    def acting(self, inputs):
        act = self.brain.forward(inputs);
        for k in range(4):
            if(act[k]>0.5 and k ==0):
                self.accelerate();
            if(act[k]>0.5 and k==1):
                self.brake();
            if(act[k]>0.5 and k==2):
                self.left();
            if(act[k]>0.5 and k==3):
                self.right();

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
            self.speed -=0.4;

    def calculScore(self):
        return self.score*300 - self.game.compteur;