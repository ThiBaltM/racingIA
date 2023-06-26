import pygame  


class Menu:

    def __init__(self, screen):
        self.screen = screen 
        self.pressed = {}
   
        # importer l'arrière plan de notre jeu
        self.background = pygame.transform.scale(pygame.image.load('assets/menu.png'), (self.screen.get_width(), self.screen.get_height()))
      
        # importer les images des boutons
        self.img = {}


    def update(self):
        self.screen.blit(self.background,(0,0))
        

     

            
