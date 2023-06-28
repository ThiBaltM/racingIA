import pygame  


class Menu:

    def __init__(self, screen):
        self.screen = screen 
        self.pressed = {}
        self.cliquerJouer = False 
        self.cliquerQuitter = False 
        self.jeuLance = False
        self.menuLance = True
   
        # importer l'arrière plan de notre jeu
        self.background = pygame.transform.scale(pygame.image.load('assets/menu.png'), (self.screen.get_width(), self.screen.get_height()))
      
        # importer les images des boutons
        self.img = {}

        self.img["Jouer"] = pygame.transform.scale(pygame.image.load('assets/play.xcf'), (250,100))
        self.rectJouer = self.img["Jouer"].get_rect()
        self.rectJouer.x = self.screen.get_width() /2.5
        self.rectJouer.y = self.screen.get_height() /3
        
        self.img["JouerCliquer"] = pygame.transform.scale(pygame.image.load('assets/playPress.xcf'), (250,100))
        self.rectJouerCliquer = self.img["JouerCliquer"].get_rect()
        self.rectJouerCliquer.x = self.screen.get_width() /2.5
        self.rectJouerCliquer.y = self.screen.get_height() /3

        self.img["Quitter"] = pygame.transform.scale(pygame.image.load('assets/quit.xcf'), (250, 100))
        self.rectQuitter = self.img ["Quitter"].get_rect()
        self.rectQuitter.x = self.screen.get_width() /2.5
        self.rectQuitter.y = self.screen.get_height() /2

        self.img["QuitterCliquer"] = pygame.transform.scale(pygame.image.load('assets/quitPress.xcf'), (250, 100))
        self.rectQuitterCliquer = self.img ["Quitter"].get_rect()
        self.rectQuitterCliquer.x = self.screen.get_width() /2.5
        self.rectQuitterCliquer.y = self.screen.get_height() /2


    def update(self):
        if self.menuLance:
            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.img["Jouer"], (self.rectJouer.x, self.rectJouer.y))
            self.screen.blit(self.img["Quitter"], (self.rectQuitter.x, self.rectQuitter.y))
        
            # affichage boutons sélection
            if self.cliquerJouer:
                self.screen.blit(self.img["JouerCliquer"], (self.rectJouerCliquer.x, self.rectJouerCliquer.y))
            if self.cliquerQuitter:    
                self.screen.blit(self.img["QuitterCliquer"], (self.rectQuitterCliquer.x, self.rectQuitterCliquer.y))
            

     

            
