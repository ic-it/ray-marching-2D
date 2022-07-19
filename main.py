from functools import cache
import math
import pygame
from map_lib import Circle, Line, Map, Polygon
from math import sqrt, atan, tan, sin, cos, fabs, pi, acos, asin

#Const
SPEED = 50
WIN_X = 1200
WIN_Y = 1000
CENTER = (WIN_X//2, WIN_Y//2)

    

def min_distance(obj_ts: list, player_pos: list):
    return round(min(ob_ct.get_distance(player_pos) for ob_ct in obj_ts))


pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)

win = pygame.display.set_mode((WIN_X, WIN_Y))   # отображение окна
clock = pygame.time.Clock()
pygame.display.set_caption("ray marching")      # заголовок окна



map_     = Map(WIN_X, WIN_Y)
map_.figures.append(Circle((300, 200), 50))
map_.figures.append(Polygon([(0, 0), (WIN_X, 0), (WIN_X, WIN_Y), (0, WIN_Y), (0, 1), (1, 2), (2, 3), (3, 0)], hidden=True))
map_.figures.append(Polygon([(200, 100), (100, 300), (100, 100), (200, 300)]))


map_.figures.append(Polygon([(500, 500), (400, 700), (200, 500), (400, 600)], color=(255, 0, 0)))

figures_ = map_._figures
player_pos = list(CENTER)


run = True
while run:
    win.fill((0, 0, 0))

    cursor = pygame.mouse.get_pos()

    c_distance = ((cursor[0]-player_pos[0])**2 + (cursor[1]-player_pos[1])**2)**0.5
    c_direction = ((cursor[0]-player_pos[0])/c_distance, (cursor[1]-player_pos[1])/c_distance)

    ## DRAW FIGURES
    for figure in figures_:
        figure.draw(win)



    for direction in ((cos(r/10), sin(r/10)) for r in range(0, 63, SPEED//3)):
        light_pos = player_pos[:]
        for i in range(10):
            min_radius = min_distance(figures_, light_pos)
            pygame.draw.circle(win, (50, 0, 50), light_pos, min_radius, 1)
            if min_radius < 5:
                pygame.draw.circle(win, (0, 255, 0), light_pos, 3)
                break
            
            p1 = light_pos[:]
            light_pos[0] += direction[0]*min_radius
            light_pos[1] += direction[1]*min_radius
            pygame.draw.line(win, (50, 50, 50), p1, light_pos, 2)
            pygame.draw.circle(win, (0, 50, 0), light_pos, 3)
        
    light_pos = player_pos[:]

    for i in range(50):
        min_radius = min_distance(figures_, light_pos)
        pygame.draw.circle(win, (255, 0, 255), light_pos, min_radius, 1)
        if min_radius < 5:
            pygame.draw.circle(win, (0, 255, 0), light_pos, 3)
            break
        p1 = light_pos[:]
        light_pos[0] += c_direction[0]*min_radius
        light_pos[1] += c_direction[1]*min_radius
        pygame.draw.line(win, (255, 255, 255), p1, light_pos, 1)
        pygame.draw.circle(win, (0, 255, 0), light_pos, 2)
    
    pygame.draw.circle(win, (225, 225, 0), player_pos, 10)       


    win.blit(my_font.render(f'{clock.get_fps()}', False, (255, 255, 255)), (10, 10))

    pygame.display.update()
    pygame.time.delay(int(SPEED))
    for event in pygame.event.get():    #quit
        if event.type == pygame.QUIT:   #quit
            run = False                 #quit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    key = pygame.key.get_pressed()

    if key[pygame.K_DOWN] or key[pygame.K_s]:
        player_pos[1] += 1
    if key[pygame.K_UP] or key[pygame.K_w]:
        player_pos[1] -= 1
    if key[pygame.K_LEFT] or key[pygame.K_a]:
        player_pos[0] -= 1
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        player_pos[0] += 1
    
    elapsed = clock.tick(60)
    SPEED = elapsed//100 or 10