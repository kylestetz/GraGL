from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import GraGL_tools

# BROKEN: StrokeFont.width() isn't quite right.

# ---------------------------------------------------
# BITMAP FONT & FONTTYPES
# ---------------------------------------------------

# aligns
LEFT = 0
CENTER = 1
RIGHT = 2

# our simplified globals for the available fonts.
# the numbers correspond to the types[] tuple below
BLOCK_8x13 = 0
BLOCK_9x15 = 1
TIMES_10 = 2
TIMES_24 = 3
HELVETICA_10 = 4
HELVETICA_12 = 5
HELVETICA_18 = 6

# the actual types, accessed using the indices above
types = [ \
GLUT_BITMAP_8_BY_13,
GLUT_BITMAP_9_BY_15,
GLUT_BITMAP_TIMES_ROMAN_10,
GLUT_BITMAP_TIMES_ROMAN_24,
GLUT_BITMAP_HELVETICA_10,
GLUT_BITMAP_HELVETICA_12,
GLUT_BITMAP_HELVETICA_18
]

# the class. defaults to 8x13 block font.
class BitmapFont:
    def __init__(self, ftype = BLOCK_8x13):
        # convert our type to the actual glut font type
        self.ftype = types[ftype]
        self.hasColor = False
        self.color = None
        self.alignment = 0
    
    # display the text.
    def text(self, string, x, y):
        # in case there is a font color we need
        # to create this temporary reference.
        # when I think about this it confuses me
        # but it seems to work?
        lastColor = None
        
        if self.hasColor:
            lastColor = glGetFloatv(GL_CURRENT_COLOR)
            apply(glColor3f, self.color)
        
        xoffset = 0

        if self.alignment == 1:
            xoffset = -self.width(string)/2.0
        elif self.alignment == 2:
            xoffset = -self.width(string)

        for c in string:
            # note: glRasterPos is NOT cumulative. it takes absolute positions.
            glRasterPos2f(x + xoffset, y)
            glutBitmapCharacter(self.ftype, ord(c))
            xoffset += glutBitmapWidth(self.ftype, ord(c))
        
        # apply the previous color again if necessary
        if self.hasColor:
            apply(glColor4f, lastColor)
    
    # this grabs the width of the string. Tried to use
    # glBitmapLength() but there was a string-to-ctype mismatch.
    def width(self, string):
        total = 0
        for c in string:
            total += glutBitmapWidth(self.ftype, ord(c))
        return total
    
    # sets an internal color
    def setColor(self, r, g, b):
        self.hasColor = True
        self.color = (r, g, b)

    def align(self, a):
        self.alignment = a

# ---------------------------------------------------
# A STROKE FONT!
# ---------------------------------------------------

class StrokeFont:
    def __init__(self, size, tracking = 20):
        self.scale = size/119.05
        self.hasColor = False
        self.color = None
        self.tracking = tracking
        self.alignment = 0 # LEFT by default

    def setSize(self, s):
        self.scale = s/119.05
    
    def text(self, string, x, y):
        if self.hasColor:
            self._textWithColor(string, x, y)
        else:
            self._text(string, x, y)

    def _textWithColor(self, string, x, y):
        lastColor = glGetFloatv(GL_CURRENT_COLOR)
        apply(glColor4f, self.color)
        self._text(string, x, y)
        apply(glColor4f, lastColor)

    def _text(self, string, x, y):
        linewidth = GraGL_tools.app.LINE_WIDTH_GraGL
        glLineWidth(1)
        
        glPushMatrix()
        
        # how to get rid of this verbosity?
        if self.alignment == 0:
            glTranslatef(x, y, 0)
        elif self.alignment == 1:
            glTranslatef(x - self.width(string)/2.0, y, 0)
        elif self.alignment == 2:
            glTranslatef(x - self.width(string), y, 0)
        
        # apparently the letters are upside-down by default,
        # hence the -y translation...
        glScale(self.scale, -self.scale, 1)
        for c in string:
            # this automatically translates over the width of the character...
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
            # but we can give it a little nudge anyway.
            # sorry, this makes things a little more complicated, but the
            # result looks way better.
            if c != ' ':
                # track if the character isn't a space
                glTranslatef(self.tracking, 0, 0)
            else:
                # backtrack if it is a space.
                glTranslatef(-self.tracking, 0, 0)
        glPopMatrix()
        
        glLineWidth(linewidth)

    
    def width(self, string):
        total = 0
        for c in string:
            # for some reason glutStrokeWidthf isn't working.
            # the following is technically depricated but it returns an integer just fine.
            total += glutStrokeWidth(GLUT_STROKE_ROMAN, ord(c)) * self.scale
            # factor in the space adjustments happening in the text display.
            # this is sort of broken at the moment.
            if c != ' ':
                total += self.tracking*self.scale
            else:
                total -= self.tracking*self.scale
        return total
    
    def setColor(self, r, g, b, a=1):
        self.hasColor = True
        self.color = (r, g, b, a)
    
    def setTracking(self, t):
        self.tracking = t
    
    def align(self, a):
        self.alignment = a