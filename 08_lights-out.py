from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_image import *

import random

class LightsOut(GraGL):

    def __init__(self):
        GraGL.__init__(self)
        self.backgroundColor = (0.8, 0.8, 0.8, 1)
        size(500, 500)

    def setup(self):
        self.lines = GImage("lines.png")
        self.blips = []
        for x in range(5):
            for y in range(5):
                self.blips.append(Blip(self.lines, x*100, y*100))
        stroke(0.7, 0, 0)
        self.size = 5
        self.levels = \
        [(0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),\
        (1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1)]
        self.current = 0
        self.loadLevel(self.current)

    def loadLevel(self, new):
        self.current = new
        for i in range(len(self.blips)):
            self.blips[i].on = self.levels[new][i]
    
    def draw(self):
        for i in range(1, self.size):
            line(i * 100, 0, i * 100, height())
            line(0, i * 100, width(), i * 100)
        for b in self.blips:
            b.draw()

    def mousePressed(self, x, y, b):
        hit = 0
        for i in range(len(self.blips)):
            if self.blips[i].mouseOver(x, y):
                hit = i
                break
        self.flip(hit)
        if self.checkSolution() == 0:
            self.loadLevel(self.current + 1)

    def flip(self, hit):
        x = hit%self.size
        y = int(hit/self.size)
        print x, y
        self.blips[hit].flip()
        # above
        if y > 0:
            self.blips[ x + (y - 1) * self.size ].flip()
        # below
        if y < self.size - 1:
            self.blips[ x + (y + 1) * self.size ].flip()
        # left
        if x > 0:
            self.blips[ (x - 1) + y * self.size ].flip()
        # right
        if x < self.size - 1:
            self.blips[ (x + 1) + y * self.size ].flip()

    def checkSolution(self):
        for b in self.blips:
            if b.on:
                return 1
        return 0



class Blip:
    def __init__(self, img, x, y):
        self.img = img
        self.x, self.y = x, y
        self.w, self.h = 100, 100
        self.on = 0

    def draw(self):
        if self.on:
            self.img.draw(self.x, self.y)

    def mouseOver(self, x, y):
        if self.x < x < self.x+self.w and self.y < y < self.y+self.h:
            return True
        return False

    def flip(self):
        self.on = 1 - self.on


runApp(LightsOut())