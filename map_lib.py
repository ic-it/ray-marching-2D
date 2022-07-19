import numpy as np
import pygame

from math import sqrt
from typing import Union
from dataclasses import dataclass



@dataclass
class Circle:
    center: tuple
    radius: int
    color: tuple = (0, 255, 255)
    hidden: bool = False

    def __post_init__(self):
        if self.hidden:
            self.draw = lambda win: None

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.center, self.radius)
    
    def get_distance(self, point: tuple) -> int:
        return sqrt((self.center[0] - point[0])**2 + (self.center[1] - point[1])**2) - self.radius


@dataclass
class Line:
    start: tuple
    end: tuple
    color: tuple = (255, 0, 255)
    hidden: bool = False

    def __post_init__(self):
        if self.hidden:
            self.draw = lambda win: None

    def draw(self, win):
        pygame.draw.line(win, self.color, self.start, self.end)
    
    def get_distance(self, point: tuple) -> int:
        return Line._get_distance(self.start, self.end, point)

    @staticmethod
    def _get_distance(start: tuple, end: tuple, point: tuple) -> int:
        if end[0] >= start[0] and end[1] >= start[1]: 
            x1_, y1_ = end     # Координаты начала
            x2_, y2_ = start   # Координаты конца
        else:
            x1_, y1_ = start   # Координаты начала
            x2_, y2_ = end     # Координаты конца
        px_, py_ = point                  # Координаты курсора
        
        l1_ = sqrt((x1_ - px_)**2 + (y1_ - py_)**2)
        l2_ = sqrt((x2_ - px_)**2 + (y2_ - py_)**2)
        l3_ = sqrt((x2_ - x1_)**2 + (y2_ - y1_)**2)
        AC_ = max(l1_, l2_)
        A_ = y2_ - y1_
        B_ = x1_- x2_
        C_ = y1_*(x2_ - x1_) - x1_*(y2_ - y1_)
        if sqrt(A_**2 + B_**2) == 0:
            d_ = abs(A_*px_ + B_*py_ + C_) / 0.000001
        else:
            d_ = abs(A_*px_ + B_*py_ + C_) / sqrt(A_**2 + B_**2)
        AD_ = sqrt(AC_**2 - d_**2)
        if AD_ > l3_:
            return min(l1_, l2_)
        else:
            return d_

@dataclass
class Polygon:
    points: list
    color: tuple = (255, 255, 0)
    hidden: bool = False

    def __post_init__(self):
        if self.hidden:
            self.draw = lambda win: None

    def draw(self, win):
        pygame.draw.polygon(win, self.color, self.points)

    def get_distance(self, point: tuple) -> int:
        dists = []
        for i in range(len(self.points)):
            dists.append(Line._get_distance(self.points[i], self.points[(i+1)%len(self.points)], point))
        return min(dists)


class Map:
    _figures: list[Union[Circle, Line, Polygon]]

    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth

        self._figures = []

    @property
    def figures(self):
        return self._figures

