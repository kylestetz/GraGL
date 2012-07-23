from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_image import *

import random

class Lines(GraGL): 

    def __init__(self):
        GraGL.__init__(self)
        self.backgroundColor = (0.9, 0.9, 0.9, 1)
        size(1000, 1000)

    def setup(self):
        self.lines = GImage("lines.png")
        self.grid = []
        for x in range(5):
            for y in range(5):
                self.grid.append(LineImage(self.lines, x*200, y*200))
        glColor3f(0, 0, 0.5)

    def draw(self):
        for l in self.grid:
            l.draw()
            l.drawSmall(0, 0)
            l.drawSmall(500, 0)
            l.drawSmall(500, 500)
            l.drawSmall(0, 500)

    def mousePressed(self, x, y, b):
        for l in self.grid:
            if l.mouseOver(x, y):
                l.flipped = not l.flipped
                break
    
    def mouseDragged(self, x, y, b):
        if 0 < x < 100 and 0 < y < 100:
            self.lines.pixels[x + y*100] = (255, 255, 255, 255)
            self.lines.updatePixels()


class LineImage:
    def __init__(self, img, x, y):
        self.img = img
        self.x, self.y = x, y
        self.w, self.h = 200, 200
        self.flipped = False

    def draw(self):
        if self.flipped:
            # glColor3f(0.6, 0.3, 0.3)
            glColor3f(0, 0.7, 0.7)
            self.img.draw(self.x + self.w, self.y, -self.w, self.h)
        else:
            # glColor3f(0.3, 0.3, 0.1)
            glColor3f(0.3, 0.4, 0.6)
            self.img.draw(self.x, self.y, self.w, self.h)

    def drawSmall(self, xoff, yoff):
        if self.flipped:
            # glColor3f(0.6, 0.3, 0.3)
            glColor3f(0, 0.7, 0.7)
            self.img.draw(self.x/2 + 100 + xoff, self.y/2 + yoff, -100, 100)
        else:
            # glColor3f(0.3, 0.3, 0.1)
            glColor3f(0.3, 0.4, 0.6)
            self.img.draw(self.x/2 + xoff, self.y/2 + yoff, 100, 100)

    def mouseOver(self, x, y):
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        return False

runApp(Lines())