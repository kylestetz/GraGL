from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import time
import GraGL_tools


"""
ABOUT.

This is a first pass at a 2d library for prototyping interactions/interfaces.
Full of charming little mistakes and oddities.
Some algorithms are borrowed; credit is given where that happens.
Yes, this is based on deprecated python, deprecated OpenGL, etc. etc.
Works for now!
Established and maintained by Kyle Stetz. kylestetz@gmail.com.

TODO.

Figure out frame rate math issue- is it an error in the calculation or a
fundamental limitation of time.sleep()? Or something else?

DEPENDENCIES.

The number of dependencies for this library is regrettably high.

the only truly necessary piece:
    ~PyOpenGL           http://pypi.python.org/pypi/PyOpenGL

for images:
    ~PIL                http://www.pythonware.com/products/pil/
    ~numpy              http://sourceforge.net/projects/numpy/files/

for fonts:
    ~PIL                http://www.pythonware.com/products/pil/
    ~FreeType           (a C library, which can't be packaged with a python build)
                        > http://freetype.sourceforge.net/download.html#stable
                        > or in macports: "sudo port install freetype"
    ~freetype-py        http://code.google.com/p/freetype-py/downloads/list

for midi:
    ~rtmidi-python      https://github.com/superquadratic/rtmidi-python/

"""

# GraGL is the class that the app inherits. All of the app's functions,
# e.g. update, draw, mousePressed, etc., are wrapped in parent functions
# (all of which end in GraGL) which take care of some OpenGL stuff and
# make it super easy to get an app going.

class GraGL:
    def __init__(self):
        # register the app with GraGL_tools
        # so that tools can modify app parameters
        # without having to pass 'self' references
        GraGL_tools.setApp(self)

        # window title, which can be changed with setWindowTitle()
        # from within app.__init__()
        self.WINDOW_TITLE = "GraGL"

        # size (updates with window resizing!)
        self.WIDTH, self.HEIGHT = 800, 800

        # this is a workaround for glutMotionFunc's lack of a
        # mouse button parameter.
        self.MOUSE_BUTTON_GraGL = None

        # mouse vitals
        self.MOUSE_X, self.MOUSE_Y = 0, 0

        # framerate timing! default = 60fps
        self.DELTA_TIME = 1/60.0
        self.PRE_CALC_TIME = 0
        self.POST_CALC_TIME = 0
        self.CALC_TIME = 0

        # a useful feature
        self.FRAMECOUNT = 0

        # this is given to glClearColor every frame
        self.backgroundColor = (0.2, 0.2, 0.2, 0)

        # fill & stroke with corresponding booleans
        self.FILL_GraGL = True
        self.STROKE_GraGL = True
        self.FILL_COLOR_GraGL = (0.3, 0.3, 0.6, 1)
        self.STROKE_COLOR_GraGL = (1, 1, 1, 1)
        self.LINE_WIDTH_GraGL = 1

        # fill/stroke stack
        self.styleStack = []

    def setup(self):
        pass

    def onAppExit(self):
        pass

    # -------------------------------------------------------
    # UPDATING
    # -------------------------------------------------------

    def update(self):
        pass

    def updateGraGL(self):
        self.FRAMECOUNT += 1
        self.update()

    # -------------------------------------------------------
    # DRAWING
    # -------------------------------------------------------

    def draw(self):
        pass

    # THIS PART IS WONKY. please help.
    def drawGraGL(self):
        # finish measuring the time it takes to compute a frame.
        self.postMeasureCalcTime()
        # sleep the thread for the difference of the ideal frame time
        # and the actual frame time
        self.normalizeFPS()
        # start measuring the time it takes to compute a frame.
        self.preMeasureCalcTime()

        # ----
        # Here's where the app's stuff actually happens.
        # ----

        # call the parent update function
        self.updateGraGL()
        # set up the OpenGL frame
        self.setupSceneGraGL()
        # the actual draw call.
        self.draw()
        # this is necessary for OpenGL.
        glutSwapBuffers()

        self.endOfFrame()

    def endOfFrame(self):
        pass

    def setupSceneGraGL(self):
        # select + load the projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # set projection matrix to orthographic @ window width and height
        glOrtho(0, self.WIDTH, self.HEIGHT, 0, 0, 1)
        # change the viewport to reflect window width/height
        glViewport(0, 0, self.WIDTH, self.HEIGHT)
        glDisable(GL_DEPTH_TEST)
        # select + load the model matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # a lil pixel magic
        glTranslatef(0.375, 0.375, 0)
        # clear the background with the bg color
        apply(glClearColor, self.backgroundColor)
        glClear(GL_COLOR_BUFFER_BIT)

    # ------------------------------------------------------
    # BACK END HANDLERS
    # ------------------------------------------------------

    def windowResizeHandler(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

    def mousePressHandler(self, button, state, x, y):
        self.setMouseCoordsGraGL(x, y)
        self.MOUSE_BUTTON_GraGL = button
        if state == GLUT_DOWN:
            self.mousePressed(x, y, button)
        elif state == GLUT_UP:
            self.mouseReleased(x, y, button)

    def mouseMoveHandler(self, x, y):
        self.setMouseCoordsGraGL(x, y)
        self.mouseMoved(x, y)

    def mouseDragHandler(self, x, y):
        self.setMouseCoordsGraGL(x, y)
        self.mouseDragged(x, y, self.MOUSE_BUTTON_GraGL)

    def keyPressHandler(self, *args):
        if args[0] == '\x1b':
            self.onAppExit()
            sys.exit()
        numkey = ord(args[0])
        self.keyPressed(numkey)

    def setMouseCoordsGraGL(self, x, y):
        self.MOUSE_X, self.MOUSE_Y = x, y

    # ------------------------------------------------------
    # FRONT END HANDLERS
    # ------------------------------------------------------

    # These are the handlers that a GraGLer will actually be exposing.

    def mouseMoved(self, x, y):
        pass

    def mousePressed(self, x, y, b):
        pass

    def mouseReleased(self, x, y, b):
        pass

    def mouseDragged(self, x, y, b):
        pass

    def keyPressed(self, key):
        pass

    # ------------------------------------------------------
    # FRAME RATE NORMALIZATION
    # ------------------------------------------------------

    def setFrameRate(self, framerate):
        # the ideal amount of time a given frame would take
        # at the framerate passed in.
        self.DELTA_TIME = 1/float(framerate)

    def normalizeFPS(self):
        time_to_sleep = self.DELTA_TIME - self.CALC_TIME
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    def preMeasureCalcTime(self):
        self.PRE_CALC_TIME = time.time()

    def postMeasureCalcTime(self):
        self.POST_CALC_TIME = time.time()
        self.CALC_TIME = self.POST_CALC_TIME - self.PRE_CALC_TIME

def runApp(app):
    # the app is instantiated as it is passed into runApp, which
    # means we have access to all of its variables and functions.
    glutInit()
    # use the app's size to define the GL window
    glutInitWindowSize(app.WIDTH, app.HEIGHT)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    # use the app's title to name the window
    glutCreateWindow(app.WINDOW_TITLE)
    
    # Here we register all of the app's functions with our OpenGL environment.

    # the draw call:
    glutDisplayFunc(app.drawGraGL)
    # the idle call, which is the draw call:
    glutIdleFunc(app.drawGraGL)
    # an event handler for window resizing

    glutReshapeFunc(app.windowResizeHandler)
    # the keyboard event handler
    glutKeyboardFunc(app.keyPressHandler)
    # mouse click event handler
    glutMouseFunc(app.mousePressHandler)
    # mouse move event handler
    glutPassiveMotionFunc(app.mouseMoveHandler)
    # mouse drag event handler
    glutMotionFunc(app.mouseDragHandler)

    # I don't know too much about these.
    # Better anti-aliasing would be nice.
    glShadeModel(GL_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glBlendFunc(GL_SRC_ALPHA, GL_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    # last thing to do is call setup.
    app.setup()

    # this should always be the last thing, as it is the main loop.
    glutMainLoop()