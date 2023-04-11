import pygame as py
from math import sqrt, inf

class Road:
    def __init__(self, game):
        self.game = game;
        self.screen = game.screen;
        self.listPts = [(128, 380), (123, 430), (139, 481), (157, 512), (184, 538), (217, 556), (268, 572), (319, 590), (392, 601), (437, 604), (506, 618), (557, 624), (604, 631), (665, 630), (696, 630), (749, 628), (799, 616), (840, 594), (887, 580), (953, 565), (1002, 561), (1046, 565), (1070, 579), (1109, 605), (1146, 620), (1193, 605), (1199, 564), (1204, 523), (1189, 469), (1172, 431), (1171, 388), (1158, 347), (1150, 297), (1148, 253), (1152, 187), (1151, 140), (1149, 99), (1119, 72), (1064, 52), (1010, 50), (957, 80), (864, 134), (812, 150), (711, 145), (668, 121), (590, 110), (526, 107), (487, 127), (476, 170), (501, 209), (566, 226), (635, 236), (689, 261), (736, 292), (760, 331), (744, 362), (685, 370), (636, 370), (559, 363), (493, 353), (450, 343), (403, 321), (374, 288), (317, 230), (265, 212), (228, 214), (192, 236), (164, 275)];
        #self.list = [];
    
    def draw(self):
        self.list.append(py.mouse.get_pos())  

    def advance(self, car):
        x, y = (int(car.x-car.img.get_width()/2), int(car.y-car.img.get_height()/2));
        c = 0;
        listeDistance = [];
        dictDistance = {};
        for coords in self.listPts:
            l = sqrt((x-coords[0])**2+(y-coords[1])**2);
            listeDistance.append(l)
            dictDistance[l] = c;
            py.draw.circle(self.screen,'red',coords,5,5);

            c+=1;
        if(listeDistance != []):
            r = dictDistance[min(listeDistance)];
            py.draw.circle(self.screen,'green',self.listPts[r],10,10);
            return r;
        return 0;


