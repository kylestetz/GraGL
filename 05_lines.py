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

    def setup(self):
        self.lines = GImage("lines.png")

    def draw(self):
        # lines.png has been loaded onto the GPU as a texture, which means
        # we can call it as many times as we want with very little overhead
        self.lines.draw(0,0)
        self.lines.draw(100, 0, 200, 200)
        self.lines.draw(300, 0, 400, 400)
        self.lines.draw(300, 200, -50, 50)
        self.lines.draw(300, 400, 200, 100)
        self.lines.draw(700, 200, 100, 100)
        self.lines.draw(700, 400, 100, -100)
        self.lines.draw(300, 400, -300, 300)
        for i in range(5): self.lines.draw(300 + i*100, 700)

    def mousePressed(self, x, y, b):
        glColor4f(random.random(), random.random(), random.random(), 1)
    
    def mouseDragged(self, x, y, b):
        if 0 < x < 100 and 0 < y < 100:
            self.lines.pixels[x + y*100] = (255, 255, 255, 255)
            self.lines.updatePixels()

runApp(Lines())