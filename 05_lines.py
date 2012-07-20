from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_image import *

class Lines(GraGL):

    def __init__(self):
        GraGL.__init__(self)
        self.backgroundColor = (0.9, 0.9, 0.9, 1)

    def setup(self):
        self.lines = GImage("lines.png")

        self.genlines = GImage()
        self.genlines.createEmpty(100, 100)
        for i in range(0, len(self.genlines.pixels), 13):
            self.genlines.pixels[i] = (255, 255, 255, 255)
        self.genlines.updatePixels()

    def draw(self):
        glColor3f(1, 0, 0)
        self.genlines.draw(0, 0, 300, 300)
        glColor3f(0, 1, 0)
        self.genlines.draw(3, 0, 300, 300)
        glColor3f(0, 0, 1)
        self.genlines.draw(mouseX(), mouseY(), 300, 300)

runApp(Lines())