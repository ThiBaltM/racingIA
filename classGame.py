import pygame as py
from classCar import Car
from classRoad import Road
from classNeuron import NeuralNetwork
from functionShortCar import shortingScore;
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
        self.actionCamera = True;

        self.road = [py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth, self.screenHeight)),py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth*2, self.screenHeight*2))];
        self.trackBorder = json.load(open("roadCollides.json"))
        self.x = 0;
        self.y=0;
        self.roadAdvance = Road(self);
        self.listCar = [];
        self.layer = [11,14,18,15,2]

        try:
            file = open("genSave.json", 'r')
            data = json.load(file)
            self.gen = data["gen"]
            for k in range (self.pop):
                self.listCar.append(Car(self, NeuralNetwork(data = data["listCar"][k])));
            print("fichier sauvegarde lu")

        except IOError:
            print("pas de sauvegarde trouvée, lancement d'une nouvelle simulation")
            self.listCar = []
            for _ in range (self.pop):
                self.listCar.append(Car(self, NeuralNetwork(self.layer[0],self.layer[1],self.layer[2],self.layer[3], self.layer[4])));
            self.gen = 0;

        self.lives = self.batchTry;
        self.currentListCar = self.listCar[:self.batchTry];
        self.clock = py.time.Clock();
        self.fps = 30;


          
    def update(self):
        """Cette fonction met a jour les evenement divers pouvant avoir lieux"""
        self.clock.tick(self.fps);
        py.draw.rect(self.screen, (22,73,0), py.Rect(0,0,self.screen.get_width(), self.screen.get_height()));
        if(self.lives<=0):
            self.lives = self.batchTry;
            if((self.numBatch+1)*self.batchTry>=self.pop):
                


                self.gen +=1;
                self.numBatch = 0;
                self.listCar.sort(key=lambda x:x.scoreFinal, reverse=True);

                nListCar =[];
                for k in range (25):
                    nListCar.append(Car(self, self.listCar[k].brain));
                for k in range (25, 450):
                    
                    r1 = random.choices(population=[i for i in range(150)], weights=[(151-i)*(151-i) for i in range(150)], k=1)
                    tmp = [i for i in range(150)]
                    tmp.remove(r1[0])
                    tmp2 = [(151-i)*(151-i) for i in range(150)]
                    tmp2.remove((151-r1[0])*(151-r1[0]))
                    r2 = random.choices(population=tmp, weights=tmp2, k=1)

                    p1 = self.listCar[r1[0]]
                    p2 = self.listCar[r2[0]]
                    nListCar.append(Car(self, NeuralNetwork(data=p1.brain.export(), data2=p2.brain.export())));
                for k in range(450,500):
                    nListCar.append(Car(self,NeuralNetwork(self.layer[0],self.layer[1],self.layer[2],self.layer[3])))
                
                self.listCar = nListCar;

                #sauvegarde de la génération
                if(self.gen%2==0):
                    print(f"sauvegarde gen {self.gen}...")
                    with open('genSave.json', 'w') as outfile:
                        outfile.write(json.dumps(
                            {
                                "listCar":[car.brain.export() for car in self.listCar],
                                "gen":self.gen
                            }
                        ))
                    print("sauvegarde terminée")

                random.shuffle(self.listCar);
                self.currentListCar = self.listCar[:self.batchTry]
            else:
                self.numBatch +=1;
                self.currentListCar = self.listCar[self.numBatch*self.batchTry: (self.numBatch+1)*self.batchTry]
                


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
        self.currentListCar.sort(key=shortingScore);   
        firstCar = self.currentListCar[-1]

        if(self.actionCamera):
            x,y = firstCar.x, firstCar.y;
            x,y = (-2*x+self.screenWidth/2,-2*y+self.screenHeight/2)
            self.screen.blit(self.road[int(self.actionCamera)], (x,y));
            firstCar.showData();
            for car in self.currentListCar:
                car.disp(x,y);
        else:
            self.screen.blit(self.road[int(self.actionCamera)], (0,0));
            firstCar.showData();
            for car in self.currentListCar:
                car.disp(0,0);

        
        
        #afficher génération
        font = py.font.SysFont(None, 20)
        img = font.render('gen : '+str(self.gen), True, (0,0,0))
        self.screen.blit(img, (100, 10))
        img = font.render('remain : '+str(self.lives), True, (0,0,0))
        self.screen.blit(img, (260, 10))
        img = font.render('batch : '+str(self.numBatch), True, (0,0,0))
        self.screen.blit(img, (180, 10))

        img = font.render('FPS : '+str(round(self.clock.get_fps())), True, (0,0,0))
        self.screen.blit(img, (5, 10))
        
        self.compteur += 1;
