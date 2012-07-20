from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_gui import *

class ColorMixer(GraGL):
    def __init__(self):
        GraGL.__init__(self)

    def setup(self):
        # create an instance of our handy GUI manager
        self.guiManager = GuiManager()
        # here we are creating Sliders, adding them to the manager, and giving them callbacks, all in one line
        self.guiManager.addElement( Slider(width()/2.0 - 50, height()/2.0 - 50), self.mixRed )
        self.guiManager.addElement( Slider(width()/2.0 - 50, height()/2.0), self.mixGreen )
        self.guiManager.addElement( Slider(width()/2.0 - 50, height()/2.0 + 50), self.mixBlue )
        # some variables to keep track of the color
        self.red = 0.5
        self.green = 0.5
        self.blue = 0.5

    def draw(self):
        background(self.red, self.green, self.blue)
        self.guiManager.draw()

    # here we direct all of the mouse events to the GUI manager
    def mouseMoved(self, x, y):
        self.guiManager.mouseMoved(x, y)
    
    def mousePressed(self, x, y, b):
        self.guiManager.mousePressed(x, y)
    
    def mouseDragged(self, x, y, b):
        self.guiManager.mouseDragged(x, y)
        
    def mouseReleased(self, x, y, b):
        self.guiManager.mouseReleased(x, y)

    # these are our Slider callbacks.
    # Whenever a slider moves, it sends its new value to the callback.
    def mixRed(self, r):
        self.red = r

    def mixGreen(self, g):
        self.green = g

    def mixBlue(self, b):
        self.blue = b


# This is a simple class to keep track of all the GUI elements.
# It can be extended to keep track of names or IDs, which would allow
# you to reference the elements individually from the main sketch.

# It takes advantage of the fact that GUI elements return a 1 if they've
# consumed the mouse input, thereby preventing overlapping elements from
# reacting to the mouse during the same frame.

class GuiManager:
    def __init__(self):
        self.elements = []

    def addElement(self, e, c):
        e.setCallback(c)
        self.elements.append(e)

    def draw(self):
        for e in self.elements:
            e.draw()

    def mouseMoved(self, x, y):
        for e in self.elements:
            if e.mouseOver(x, y):
                return
    
    def mousePressed(self, x, y):
        for e in self.elements:
            if e.mousePressed(x, y):
                return
    
    def mouseDragged(self, x, y):
        for e in self.elements:
            if e.mouseDragged(x, y):
                return
        
    def mouseReleased(self, x, y):
        for e in self.elements:
            if e.mouseReleased(x, y):
                return


runApp(ColorMixer())