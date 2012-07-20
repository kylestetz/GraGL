from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

"""
WHAT THIS IS ALL ABOUT.

The tools section of GraGL stores a reference to the App you are developing.
Whenever the tool functions are called they grab this reference in order to read
and write variables within the App.

"""

# ----------------------------------------------------
# EVNIRONMENT
# ----------------------------------------------------

# store a ref to the app so that we can
# modify its parameters if we need to,
# e.g. for fill/stroke, style stacks, etc
app = None

# this is called from the parent GraGL class __init__()
def setApp(a):
    global app
    app = a

def width():
    global app
    return app.WIDTH

def height():
    global app
    return app.HEIGHT

def frameCount():
    global app
    return app.FRAMECOUNT

def mouseX():
    global app
    return app.MOUSE_X

def mouseY():
    global app
    return app.MOUSE_Y

# these can only be called from within the app's __init__()
def setWindowTitle(t):
    global app
    app.WINDOW_TITLE = t

def size(w, h):
    global app
    app.WIDTH, app.HEIGHT = w, h

# ----------------------------------------------------
# FILL / STROKE STYLES
# ----------------------------------------------------

# the fill & stroke colors are actually stored in the app
def fill(r, g, b, a=1):
    global app
    app.FILL_GraGL = True
    app.FILL_COLOR_GraGL = (r, g, b, a)
    apply(glColor4f, app.FILL_COLOR_GraGL)

def stroke(r, g, b, a=1):
    global app
    app.STROKE_GraGL = True
    app.STROKE_COLOR_GraGL = (r, g, b, a)

def noFill():
    global app
    app.FILL_GraGL = False

def noStroke():
    global app
    app.STROKE_GraGL = False

def strokeWidth(w):
    global app
    app.LINE_WIDTH_GraGL = w
    glLineWidth(w)

def background(r, g, b):
    global app
    app.backgroundColor = (r, g, b, 0)

# accessing/modifying the style stack
def pushStyle():
    global app
    app.styleStack.append( (app.FILL_GraGL, app.FILL_COLOR_GraGL, app.STROKE_GraGL, app.STROKE_COLOR_GraGL, app.LINE_WIDTH_GraGL) )

def popStyle():
    global app
    last = app.styleStack.pop()
    restoreStyles(last)
    glLineWidth(app.LINE_WIDTH_GraGL)

def restoreStyles(items):
    global app
    app.FILL_GraGL, app.FILL_COLOR_GraGL, app.STROKE_GraGL, app.STROKE_COLOR_GraGL, app.LINE_WIDTH_GraGL = items

# -----------------------------------------------------
# SHAPES & LINES
# -----------------------------------------------------

def rectangle(x, y, w, h):
    global app
    if app.FILL_GraGL:
        apply(glColor4f, app.FILL_COLOR_GraGL)
        _rectangle(x,y,w,h)
    if app.STROKE_GraGL:
        apply(glColor4f, app.STROKE_COLOR_GraGL)
        _strokeRectangle(x,y,w,h)

def _rectangle(x, y, w, h):
    glBegin(GL_POLYGON)
    glVertex3f(x, y, 0)
    glVertex3f(x + w, y, 0)
    glVertex3f(x + w, y + h, 0)
    glVertex3f(x, y + h, 0)
    glEnd()

def _strokeRectangle(x, y, w, h):
    glBegin(GL_LINE_LOOP)
    glVertex3f(x, y, 0)
    glVertex3f(x + w, y, 0)
    glVertex3f(x + w, y + h, 0)
    glVertex3f(x, y + h, 0)
    glEnd()

#

def circle(x, y, r, pts = 40):
    global app
    if app.FILL_GraGL:
        apply(glColor4f, app.FILL_COLOR_GraGL)
        _circle(x, y, r, pts)
    if app.STROKE_GraGL:
        apply(glColor4f, app.STROKE_COLOR_GraGL)
        _strokeCircle(x, y, r, pts)

def _circle(x, y, r, pts):
    glBegin(GL_POLYGON)
    for i in range(pts):
        xv = x + math.cos(i * math.pi/(pts/2.0)) * r
        yv = y + math.sin(i * math.pi/(pts/2.0)) * r
        glVertex3f(xv, yv, 0)
    glEnd()

def _strokeCircle(x, y, r, pts):
    glBegin(GL_LINE_LOOP)
    for i in range(pts):
        xv = x + math.cos(i * math.pi/(pts/2.0)) * r
        yv = y + math.sin(i * math.pi/(pts/2.0)) * r
        glVertex3f(xv, yv, 0)
    glEnd()

#

def line(x1, y1, x2, y2):
    global app
    if app.STROKE_GraGL:
        apply(glColor4f, app.STROKE_COLOR_GraGL)
        glBegin(GL_LINES)
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)
        glEnd()


# ----------------------------------------------------
# VERTICES & CUSTOM SHAPES
# ----------------------------------------------------

# styles
OPEN_LINE = GL_LINE_STRIP
CLOSED_LINE = GL_LINE_LOOP
TRIANGLES = GL_TRIANGLES
QUADS = GL_QUADS

def beginShape(style=None):
    if style:
        glBegin(style)
    else:
        glBegin(GL_POLYGON)

def endShape():
    glEnd()

def vertex(x, y):
    glVertex3f(x, y, 0)

def vFill(r, g, b, a=1):
    glColor4f(r, g, b, a)


# ----------------------------------------------------
# TRANSFORMATIONS
# ----------------------------------------------------

# a thinly veiled reference to glTranslate & glRotate.
# keeping it 2d by default for now.

def translate(x, y, z=0):
    glTranslatef(x, y, z)

def rotate(a, x=0, y=0, z=1):
    # glRotate takes degrees!
    glRotatef(a, x, y, z)

def degrees(r):
    # turn radians to degrees
    return math.degrees(r)

def radians(d):
    # degrees to radians
    return math.radians(d)

# gonna use these because they are way more
# efficient than whatever I can dream up

def pushMatrix():
    glPushMatrix()

def popMatrix():
    glPopMatrix()


# ----------------------------------------------------
# MATH, NUMBERS, ETC
# ----------------------------------------------------

def constrain(num, minimum, maximum):
    if min(num, minimum) == num:
        num = minimum
    elif max(num, maximum) == num:
        num = maximum
    return num

def dist2(x1, y1, x2, y2):
    return (x2 - x1)**2 + (y2 - y1)**2

def bounds(x, y, x1, y1, x2, y2):
    return x1 < x < x2 and y1 < y < y2

# ----------------------------------------------------
# INTERPOLATION
# ----------------------------------------------------


# this code is borrowed from Ben Fry's excellent Visualizing Data book.
# It's a simple 1D physics attractor that can be tweaked to move
# linearly or bounce around towards a target.
class Integrator:
    def __init__(self, value, damp=0.5, attr=0.2):
        self.value = value
        self.damping = damp
        self.attraction = attr
        self.targeting = False
        self.target = None
        self.vel, self.accel, self.force, self.mass = 0, 0, 0, 1
    
    def set(self, v):
        self.value = v
    
    def update(self):
        if self.targeting:
            self.force += self.attraction * (self.target - self.value)
        self.accel = self.force / float(self.mass)
        self.vel = (self.vel + self.accel) * self.damping
        self.value += self.vel
        self.force = 0

    def setTarget(self, t):
        self.targeting = True
        self.target = t
    
    def noTarget(self):
        self.targeting = False

# these correspond to the different options in the following Interpolator class.
LINEAR = 0
EASE_SINE = 1
EASE_IN_SINE = 2
EASE_OUT_SINE = 3
EASE_CUBIC = 4
EASE_IN_CUBIC = 5
EASE_OUT_CUBIC = 6

# the equations in this class are adapted from Robert Penner's easing equations.
# I didn't use them all. Feel free to add more if you so choose!
# referenced from http://gizma.com/easing/
class Interpolator:
    def __init__(self, value, easing = None):
        self.easingFunctions = [self.linear, self.easeSine, self.easeSineIn, self.easeSineOut, self.easeCubic, self.easeCubicIn, self.easeCubicOut]
        self.value = value
        self.previousValue = 0
        self.target = 0
        self.targeting = False
        self.time = 1
        self.previousTime = 0
        
        if easing != None:
            self._update = self.easingFunctions[easing]
    
    def setTarget(self, target, t):
        self.targeting = True
        self.target = target
        self.time = t
        self.previousTime = time.time()
        self.previousValue = self.value

    def changeEasingType(self, newType):
        try:
            self._update = self.easingFunctions[newType]
        except:
            print "Interpolator.changeEasingType recieved an invalid type"
    
    def update(self):
        # linear movement by default.
        if self.targeting:
            pos = (time.time() - self.previousTime) / float(self.time)
            if pos <= 1.0:
                self.value = self._update(pos, self.time, self.previousValue, self.target - self.previousValue)
            else:
                self.value = self.target

    def _update(self, pos, dur, prev, change):
        return change * pos + prev

    # Penner equations for easing:
    
    def linear(self, pos, dur, prev, change):
        return change * pos + prev

    def easeSine(self, pos, dur, prev, change):
        return -change/2.0 * (math.cos(math.pi*pos) - 1) + prev

    def easeSineIn(self, pos, dur, prev, change):
        return -change * math.cos(pos * (math.pi/2.0)) + change + prev

    def easeSineOut(self, pos, dur, prev, change):
        return change * math.sin(pos * (math.pi/2.0)) + prev

    def easeCubic(self, pos, dur, prev, change):
        t = pos * dur
        if t > 0:
            t /= dur/2.0
        if t < 1:
            return change / 2.0 * t**3 + prev
        t -= 2
        return change / 2.0 * (t**3 + 2) + prev

    def easeCubicIn(self, pos, dur, prev, change):
        return change * pos**3 + prev

    def easeCubicOut(self, pos, dur, prev, change):
        pos -= 1
        return change * (pos**3 + 1) + prev
