from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_image import *
import random


class Begin(GraGL):

    def __init__(self):
        GraGL.__init__(self)
    
    def setup(self):
        self.logo = GImage("GraGL.png")
        self.logo.setColor(1, 1, 1)

        self.corner_colors = [(0.2, 0.2, 0.2), (0.2, 0.2, 0.2), (0.2, 0.2, 0.2), (0.2, 0.2, 0.2)]
        self.backgroundColor = (0.9, 0.9, 0.9, 0.9)

    def draw(self):
        lx = width()/2 - self.logo.width()/2
        ly = height()/2 - self.logo.height()/2

        beginShape()
        apply(vFill, self.corner_colors[0])
        vertex(lx + 10, ly + 10)
        apply(vFill, self.corner_colors[1])
        vertex(lx + self.logo.width() - 10, ly + 10)
        apply(vFill, self.corner_colors[2])
        vertex(lx + self.logo.width() - 10, ly + self.logo.height() - 10)
        apply(vFill, self.corner_colors[3])
        vertex(lx + 10, ly + self.logo.height() - 10)
        endShape()

        self.logo.draw(width()/2 - self.logo.width()/2, height()/2 - self.logo.height()/2)

        self.logo.shiftRed(-1)
        self.logo.shiftBlue(1)
        self.logo.updatePixels()

    def mousePressed(self, x, y, b):
        for i in range(4):
            self.corner_colors[i] = (random.random(), random.random(), random.random())


runApp(Begin())