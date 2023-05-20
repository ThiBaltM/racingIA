import pygame as py
import json

def showRes():
    #afficher l'état actuel
    for y in range(len(res)):
        for x in range(len(res[0])):
            if(res[y][x]):
                py.draw.rect(screen, "green", py.Rect(x*unit,y*unit,unit, unit));
            else:
                py.draw.rect(screen, "blue", py.Rect(x*unit,y*unit,unit, unit));

        print(f"next row {y}")
        py.display.flip()
    print("end")
    py.display.flip()

#initialisation valeurs plateau
largeurEcran, hauteurEcran = (1280, 720)
#paramétrage de l'affichage
screen = py.display.set_mode((largeurEcran,hauteurEcran))

clock = py.time.Clock()

road = py.transform.scale(py.image.load(f"assets/circuit.png"),(largeurEcran, hauteurEcran));
road_mask = py.mask.from_surface(road)
unit=4
x =0
y = 0
isRunning = True
res = [[ False for _ in range(0,largeurEcran,unit)] for k in range(0,hauteurEcran,unit)] 
tmpSurface = py.Surface((largeurEcran, hauteurEcran), py.SRCALPHA)
end = False

while isRunning:
    for event in py.event.get():
        if event.type == py.QUIT: #fermeture de la page
            isRunning = False
    if(not end):
        tmpSurface.fill((0,0,0,0));





        py.draw.rect(screen, "white", py.Rect(0,0,largeurEcran, hauteurEcran));

        screen.blit(road, (0,0));

        py.draw.rect(tmpSurface, 'red', py.Rect(x*unit,y*unit,unit,unit))
        screen.blit(tmpSurface,(0,0))

        # Création du masque à partir de la surface temporaire
        rect_mask = py.mask.from_surface(tmpSurface);

        # Test de collision entre le masque de la ligne et le masque de la piste
        overlap_mask = road_mask.overlap(rect_mask, (0,0));
        if(overlap_mask == None):
            res[y][x] = False
        else:
            res[y][x] = True
        x+= 1
        if(x*unit>=largeurEcran):
            x=0
            y+=1
            if(y*unit>=hauteurEcran):
                with open('roadCollides.json', 'w') as outfile:
                    outfile.write(json.dumps(res))
                showRes()
                end=True;

        
        py.display.flip()

