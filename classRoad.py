import pygame as py
from math import sqrt, inf

class Road:
    def __init__(self, game):
        self.game = game;
        self.screen = game.screen;
        self.listPts = [(120, 334), (120, 363), (119, 391), (120, 414), (125, 435), (130, 459), (143, 477), (158, 494), (171, 507), (186, 527), (202, 539), (221, 551), (245, 566), (272, 576), (300, 582), (330, 589), (358, 595), (392, 600), (431, 604), (476, 611), (529, 616), (606, 624), (678, 624), (733, 619), (783, 610), (816, 601), (838, 595), (858, 589), (889, 584), (923, 577), (947, 573), (970, 568), (997, 560), (1025, 560), (1049, 564), (1067, 578), (1083, 594), (1108, 610), (1144, 615), (1169, 608), (1193, 595), (1200, 574), (1200, 540), (1192, 512), (1184, 484), (1179, 469), (1173, 450), (1170, 432), (1166, 411), (1164, 390), (1157, 371), (1157, 349), (1155, 322), (1155, 300), (1156, 275), (1155, 249), (1158, 213), (1162, 171), (1156, 120), (1134, 85), (1090, 65), (1046, 64), (1003, 74), (965, 91), (938, 104), (904, 129), (860, 144), (824, 153), (784, 140), (746, 133), (708, 126), (682, 118), (640, 116), (593, 106), (553, 110), (525, 123), (501, 135), (493, 153), (497, 175), (510, 194), (531, 207), (556, 215), (584, 224), (616, 234), (649, 247), (677, 258), (707, 269), (730, 282), (740, 299), (745, 319), (735, 335), (714, 352), (688, 359), (659, 363), (626, 361), (572, 357), (538, 349), (497, 348), (456, 335), (408, 331), (373, 308), (347, 283), (324, 251), (303, 225), (264, 210), (218, 207), (181, 215), (143, 239), (130, 267)];
        #self.list = [];
    
    def draw(self):
        self.list.append(py.mouse.get_pos())  

    def advance(self, car, time, current):
        x, y = (int(car.x-car.img.get_width()/2), int(car.y-car.img.get_height()/2));
        c = 0;
        listeDistance = [];
        dictDistance = {};
        for coords in self.listPts[current:current+5]:
            l = sqrt((x-coords[0])**2+(y-coords[1])**2);
            listeDistance.append(l)
            dictDistance[l] = c;
            #py.draw.circle(self.screen,'red',coords,5,5);

            c+=1;
        if(listeDistance != []):
            r = dictDistance[min(listeDistance)]+current;
            #py.draw.circle(self.screen,'green',self.listPts[r],10,10);
            return r;
        return 0;


