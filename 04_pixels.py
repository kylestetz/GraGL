from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_image import *

class PixelSketch(GraGL):

    def __init__(self):
        GraGL.__init__(self)

    def setup(self):
        self.empty = GImage()
        self.empty.createEmpty(800, 800)

    def draw(self):
        self.empty.draw(0,0)


runApp(PixelSketch())