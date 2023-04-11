import pygame as py
from classCar import Car
from classRoad import Road

class Game:
    def __init__(self, screen):
        self.screen = screen;
        self.pressed = {py.K_e : False,1: False, py.K_z:False, py.K_s:False, py.K_q:False, py.K_d:False};
        self.compteur = 0;
        self.screenHeight, self.screenWidth = (self.screen.get_height(),self.screen.get_width());
        self.score = 0;
        self.car = Car(self);
        self.road = py.transform.scale(py.image.load(f"assets/circuit.png"),(self.screenWidth, self.screenHeight));
        self.trackBorder = py.mask.from_surface(self.road);
        self.x = 0;
        self.y=0;
        self.roadAdvance = Road(self)


          
    def update(self):
        """Cette fonction met a jour les evenement divers pouvant avoir lieux"""

        #myfont = pygame.font.SysFont('Impact', self.screen.get_width() // 74)
        #textScoreSurface = myfont.render(f"your score :{self.score}", False, (255, 255, 255))
        #self.screen.blit(textScoreSurface,(self.joueur.pixel[0] * 340, 9 * self.joueur.pixel[1]))

        #gestion joueur
        if self.pressed[py.K_z]:
            self.car.accelerate()
        elif self.pressed[py.K_s]:
            self.car.brake()
        elif self.pressed[py.K_q]:
            self.car.left()
        elif self.pressed[py.K_d]:
            self.car.right()
        
        py.draw.rect(self.screen, "white", py.Rect(0,0,self.screen.get_width(), self.screen.get_height()));

        
            
        self.screen.blit(self.road, (0,0));
        self.car.disp();
        
        self.compteur += 1;
