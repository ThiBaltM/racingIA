import pygame as py
from math import sqrt, inf

class Road:
    def __init__(self, game):
        self.game = game;
        self.screen = game.screen;
        self.listPts = [(107, 647), (129, 649), (156, 650), (175, 650), (197, 648), (220, 642), (246, 637), (271, 635), (294, 633), (324, 630), (350, 629), (379, 626), (403, 625), (432, 623), (456, 624), (488, 626), (530, 626), (555, 626), (582, 628), (607, 625), (632, 627), (659, 627), (686, 627), (711, 626), (732, 626), (751, 627), (775, 630), (795, 630), (819, 631), (845, 631), (861, 629), (878, 625), (893, 613), (904, 600), (910, 581), (920, 553), (923, 528), (930, 504), (931, 466), (941, 415), (945, 370), (951, 326), (960, 284), (976, 253), (996, 238), (1015, 232), (1032, 232), (1053, 236), (1070, 247), (1083, 261), (1090, 280), (1094, 301), (1096, 316), (1099, 340), (1101, 372), (1102, 398), (1106, 421), (1107, 449), (1115, 478), (1125, 495), (1141, 502), (1164, 502), (1186, 489), (1201, 470), (1214, 451), (1215, 417), (1217, 386), (1215, 349), (1217, 318), (1214, 275), (1207, 228), (1205, 195), (1197, 160), (1167, 131), (1133, 100), (1094, 88), (1057, 84), (1022, 84), (972, 89), (953, 98), (926, 103), (906, 106), (880, 107), (862, 100), (848, 90), (834, 81), (818, 71), (802, 74), (793, 89), (785, 112), (781, 136), (767, 156), (749, 164), (729, 150), (722, 128), (712, 104), (698, 83), (682, 69), (666, 66), (658, 77), (655, 94), (652, 113), (651, 129), (651, 143), (648, 157), (642, 171), (631, 187), (613, 180), (605, 154), (597, 133), (583, 109), (565, 90), (550, 71), (536, 56), (524, 61), (524, 81), (524, 107), (524, 130), (524, 148), (525, 173), (526, 198), (526, 223), (530, 250), (528, 278), (527, 315), (522, 340), (508, 367), (491, 391), (474, 398), (464, 405), (452, 417), (445, 435), (438, 451), (434, 464), (424, 478), (417, 487), (399, 495), (383, 499), (367, 501), (346, 502), (327, 491), (308, 476), (288, 452), (283, 415), (269, 376), (260, 348), (250, 310), (241, 265), (228, 218), (219, 166), (205, 141), (181, 131), (164, 131), (149, 140), (141, 156), (135, 176), (123, 200), (116, 229), (106, 257), (99, 284), (93, 309), (90, 338), (81, 372), (75, 404), (66, 437), (64, 465), (57, 494), (53, 522), (51, 545), (55, 568), (62, 592), (72, 612), (87, 628)]
        self.list = [];
    
    def draw(self):
        self.list.append(py.mouse.get_pos())  

    def advance(self, car, time, current):
        x, y = (int(car.x), int(car.y));
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


