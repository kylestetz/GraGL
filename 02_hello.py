from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_font import *


class Hello(GraGL):

    def __init__(self):
        # we need this to get everything started behind the scenes.
        GraGL.__init__(self)
    
    def setup(self):
        # let's create a simple bitmap font
        self.font = BitmapFont(0)
        # and give it a color
        self.font.setColor(0, 0, 0)
        # and set the align to center
        self.font.align(CENTER)

    def draw(self):
        # we are drawing a rectangle and giving each vertex a different color (neat!)
        beginShape()
        vFill(0, 0.5, 0.7)
        vertex(0, 0)
        vFill(1, 1, 0.3)
        vertex(width(), 0)
        vFill(0, 1, 0)
        vertex(width(), height())
        vFill(1, 0, 0)
        vertex(0, height())
        endShape()
        # and now we are drawing a string
        self.font.text("Hello from GraGL.", width()/2.0, height()/2.0)


# This is what actually creates and runs the app.
runApp(Hello())