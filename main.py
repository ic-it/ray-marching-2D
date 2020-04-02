import pygame
from map_lib import Map
from math import sqrt, atan, tan, sin, cos, fabs, pi, acos, asin

#Const
SPEED = 10
WIN_X = 1200
WIN_Y = 1000
CENTER = (WIN_X//2, WIN_Y//2)



def line_distance(line_, pos_now):
    if line_.get('end')[0] >= line_.get('start')[0] and line_.get('end')[1] >= line_.get('start')[1]: 
        x1_, y1_ = line_.get('end')     # Координаты начала
        x2_, y2_ = line_.get('start')   # Координаты конца
    else:
        x1_, y1_ = line_.get('start')   # Координаты начала
        x2_, y2_ = line_.get('end')     # Координаты конца
    Mx_, My_ = pos_now                  # Координаты курсора
    
    l1_ = sqrt((x1_ - Mx_)**2 + (y1_ - My_)**2)
    l2_ = sqrt((x2_ - Mx_)**2 + (y2_ - My_)**2)
    l3_ = sqrt((x2_ - x1_)**2 + (y2_ - y1_)**2)
    AC_ = max(l1_, l2_)
    A_ = y2_ - y1_
    B_ = x1_- x2_
    C_ = y1_*(x2_ - x1_) - x1_*(y2_ - y1_)
    if sqrt(A_**2 + B_**2) == 0:
        d_ = abs(A_*Mx_ + B_*My_ + C_) / 0.000001
    else:
        d_ = abs(A_*Mx_ + B_*My_ + C_) / sqrt(A_**2 + B_**2)
    AD_ = sqrt(AC_**2 - d_**2)
    if AD_ > l3_:
        return min(l1_, l2_)
    else:
        return d_

def min_distance(obj_ts: list, pos_now: list):
    distances = []
    for ob_ct in obj_ts:
        if ob_ct.get('type') == 'circle':
            distances.append(sqrt( 
                                    (pos_now[0] - ob_ct.get('center')[0])**2 + (pos_now[1] - ob_ct.get('center')[1])**2
                                    ) - ob_ct.get('radius')
                            )
        if ob_ct.get('type') == 'line':
            distances.append(line_distance(ob_ct, pos_now))
        elif ob_ct.get('type') == 'hide_box' or ob_ct.get('type') == 'figure':
            for line_ in ob_ct.get('connects'):
                points_ = { 'start': ob_ct.get('points')[line_[0]], 
                            'end': ob_ct.get('points')[line_[1]]}
                distances.append(line_distance(points_ ,pos_now))
    return round(min(distances))

pygame.init()
win = pygame.display.set_mode((WIN_X, WIN_Y))   # отображение окна
pygame.display.set_caption("ray marching")      # заголовок окна

run = True
#######
map_     = Map(WIN_X, WIN_Y)
map_.add().circle((300, 200), 50)
map_.add().line((300, 400), (300, 350))
map_.add().line((700, 350), (300, 350))
map_.add().line((400, 700), (700, 350))
map_.add().line((400, 700), (300, 400))
map_.add().hide_box(
    [(0, 0), (WIN_X, 0), (WIN_X, WIN_Y), (0, WIN_Y)], 
    [(0, 1), (1, 2), (2, 3), (3, 0)])
map_.add().figure(
    [(200, 100), (100, 300), (100, 100), (200, 300)],
    [(0, 1), (1, 2), (2, 3), (3, 0)])

figures_ = map_.figures
points_to_draw = []
pos_now = list(CENTER[:]) # Позиция начала луча
while run:
    pos_now_d = pos_now[:] # Позиция начала луча, которая будет уменьшатся со временем
    win.fill((0, 0, 0))

    #Get mouse pos
    cursor = list(pygame.mouse.get_pos())

    # Получить угол наклона между курсором и позицией в данный момент
    if (pos_now[0] - cursor[0]) == 0:
        alfa = atan((pos_now[1] - cursor[1]) / 0.0000001)
    else:
        alfa = atan((pos_now[1] - cursor[1]) / (pos_now[0] - cursor[0]))
    if cursor[0] <= pos_now[0]:
        alfa = pi+alfa

    ## DRAW FIGURES
    for figure in figures_:
        if figure.get('type') == 'circle':
            pygame.draw.circle(win, figure['color'], figure['center'], figure['radius'], 1)
        elif figure.get('type') == 'line':
            pygame.draw.line(win, figure['color'], figure['start'], figure['end'], 1)
        elif figure.get('type') == 'figure':
            pygame.draw.polygon(win, figure['color'], figure.get('points'))

    ## Get Ray 
    for i in range(50):
        pygame.draw.circle(win, (0, 225, 225), pos_now_d, 4)
        min_radius = min_distance(figures_, pos_now_d)
        if min_radius > 5:
            pygame.draw.circle(win, (225, 225, 0), pos_now_d, min_radius, 1)
        else:
            break
        pos_now_d[0] = round(pos_now_d[0] + cos(alfa)*min_radius)
        pos_now_d[1] = round(pos_now_d[1] + sin(alfa)*min_radius)

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
        pos_now[1] += 1
        points_to_draw = []
    if key[pygame.K_UP] or key[pygame.K_w]:
        pos_now[1] -= 1
        points_to_draw = []
    if key[pygame.K_LEFT] or key[pygame.K_a]:
        pos_now[0] -= 1
        points_to_draw = []
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        pos_now[0] += 1
        points_to_draw = []