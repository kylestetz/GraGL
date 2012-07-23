from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from GraGL import *
from GraGL_tools import *
from GraGL_image import *


class Fun(GraGL):

    def __init__(self):
        GraGL.__init__(self)
        size(984, 1000)

    def setup(self):
        background(0.8, 0.8, 0.8)
        self.img = GImage("spiral-galaxy.png")
    
    def draw(self):
        if frameCount() % 2 == 0:
            self.img.shiftBlue(5)
            self.img.shiftGreen(-7)
        # self.img.shiftColors(1, -1, 2, 1)
        self.img.updatePixels()

        self.img.draw(0, 0)
        

runApp(Fun())