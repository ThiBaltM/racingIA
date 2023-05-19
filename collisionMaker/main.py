import pygame as py

#initialisation valeurs plateau
largeurEcran, hauteurEcran = (1280, 720)
#paramétrage de l'affichage
screen = py.display.set_mode((largeurEcran,hauteurEcran))

clock = py.time.Clock()

road = py.transform.scale(py.image.load(f"../assets/circuit.png"),(largeurEcran, hauteurEcran));
unit=4
x =0
y = 0
isRunning = True
res = []

while isRunning:
    py.draw.rect(screen, "white", py.Rect(0,0,largeurEcran, hauteurEcran));

    screen.blit(road, (0,0));

    py.draw.rect(screen, 'red', py.Rect(x*unit,y*unit,unit,unit))
    x+= 1
    if(x*unit>=largeurEcran):
        x=0
        y+=1
        if(y*unit>=hauteurEcran):
            pass

    
    py.display.flip()

