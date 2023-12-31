#! /usr/bin/env python

import pygame
import time

"""
# Notactión

## Mapa

En mapa original:

* 0: libre
* 1: ocupado (muro/obstáculo)

Vía código incorporamos:

* 2: visitado
* 3: start
* 4: goal

## Nodo

Nós
* -2: parentId del nodo start
* -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Específico de implementación Python

* Índices empiezan en 0
* charMap
"""

# # Initial values are hard-coded (A nivel mapa)

#FILE_NAME = "/usr/local/share/master-ipr/map1/map1.csv" # Linux-style absolute path
#FILE_NAME = "C:\\Users\\USER_NAME\\Downloads\\master-ipr\\map1\\map1.csv" # Windows-style absolute path, note the `\\` and edit `USER_NAME`
#FILE_NAME = "../../../../map1/map1.csv" # Linux-style relative path
FILE_NAME = "../map7/map7.csv" # Linux-style relative path
START_X = 3
START_Y = 9
END_X = 3
END_Y = 15

# # Define Node class (A nivel grafo/nodo)

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

# # Mapa

# ## Creamos estructura de datos para mapa

charMap = []

# ## Creamos función para volcar estructura de datos para mapa

def dumpMap():
    for line in charMap:
        print(line)

# ## De fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

# ## A nivel mapa, integramos la info que teníamos de start & end

charMap[START_X][START_Y] = '3' # 3: start
charMap[END_X][END_Y] = '4' # 4: goal

# ## Volcamos mapa por consola

dumpMap()

# # Grafo búsqueda

# ## Creamos el primer nodo
init = Node(START_X, START_Y, 0, -2)
# init.dump() # comprobar que primer nodo bien

# ## `nodes` contendrá los nodos del grafo

nodes = []

# ## Añadimos el primer nodo a `nodes`

nodes.append(init)

# ## Empieza algoritmo

done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

start_time = time.time()

while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    for node in nodes:
        node.dump()

        # up
        tmpX = node.x - 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("up: GOALLLL!!!")
            goalParentId = node.myId  # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("up: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # down
        tmpX = node.x + 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("down: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("down: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # right
        tmpX = node.x
        tmpY = node.y + 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("right: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("right    : mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # left
        tmpX = node.x
        tmpY = node.y - 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("left: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("left: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        dumpMap()

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")



########################################################
################### VISUALIZATION ######################
########################################################


# initialize the pygame module
pygame.init()

pygame.display.set_caption("BREADTH FIRST SEARCH")

# create a surface on screen that has the size of 240 x 180
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
    
# define a variable to control the main loop
running = True

# Int Map

map_rows = len(charMap)
map_cols = len(charMap[0])

intMap = []

for i in range(map_rows):
    temp_row =[]
    for j in range(map_cols):
        temp_row.append(int(charMap[i][j]))
    intMap.append(temp_row)


cell_width = screen_width/map_cols
cell_height = screen_height/map_rows

size_coef = min(cell_height, cell_height)/60

# Rectangles
rectangles = []
occupied = []
color_ocuppied = (16, 25, 155)
color_free = (255, 255, 255)
color_border = (164, 169, 247)


for i in range(map_rows):
    for j in range(map_cols):
        rectangles.append(pygame.Rect(j*cell_width, i*cell_height, cell_width, cell_height))
        occupied.append(intMap[i][j])


start_color = (0, 0, 255)
start_center = (cell_width*(START_Y+0.5), cell_height*(START_X+0.5))
start_radius = (cell_width*0.2)

end_color = (251, 103, 0)
end_center = (cell_width*(END_Y+0.5), cell_height*(END_X+0.5))
end_radius = (cell_width*0.2)

# Drawing crosses

font = pygame.font.Font(None, round(60*size_coef))
cross = font.render("x", True, (104, 139, 240))

# Draw lines

prev_coor = ((END_Y+0.5)*cell_width, (END_X+0.5)*cell_height)
coordinates = [prev_coor]

ok = False
    
# main loop
while running:
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False
    
    screen.fill((0, 0, 0))
    

    for i in range(len(rectangles)):
        
        if occupied[i] == 1: color = color_ocuppied
        else: color = color_free

        pygame.draw.rect(screen, color, rectangles[i])
        pygame.draw.rect(screen, color_border, rectangles[i], round(2*size_coef))

    for i in range(map_rows):
        for j in range(map_cols):
            if intMap[i][j] == 2:
                
                cross_x, cross_y = (j+0.5)*cell_width, (i+0.5)*cell_height

                text_rect = cross.get_rect()
                text_rect.center = (cross_x, cross_y)
                
                screen.blit(cross, text_rect)     
    

    # Start point drawing
    pygame.draw.circle(screen, start_color, start_center, start_radius)

    # Goal point drawing
    pygame.draw.circle(screen, end_color, end_center, end_radius)

    # Display solución hallada

    while not ok:
        for node in nodes:
            if node.myId == goalParentId:
                node.dump()
                coordinates.append(((node.y+0.5)*cell_width, (node.x+0.5)*cell_height))
                goalParentId = node.parentId
                if( goalParentId == -2):
                    ok = True

    for i in range(len(coordinates)):
        if i>0:
            pygame.draw.line(screen, end_color, coordinates[i], coordinates[i-1], round(4*size_coef))

    pygame.display.flip()