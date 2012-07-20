from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
import numpy
from PIL import Image

# This is a class for passing PIL-loaded images into OpenGL.
# It only supports PNGs at the moment.

class GImage:
    def __init__(self, name=None):
        self.filename = name
        self.ID = None
        self.w, self.h = None, None
        self.z = 0
        self.force_color = None
        if name:
            self.loadImage(name)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        # glEnable(GL_ALPHA_TEST)
        # glAlphaFunc(GL_GREATER, 0.1)

    def loadImage(self, filename):
        self.filename = filename
        img = Image.open(self.filename)
        img_list = list(img.getdata())
        img_data = numpy.array(list(img.getdata()), numpy.uint8)

        # pixel_data = []
        # for i in range(len(img_list)):
        #     pixel_data.append((200, 0, 0, 255))
        # img_data = numpy.array(pixel_data, numpy.uint8)

        self.ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        if img.mode == "RGBA":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        elif img.mode == "RGB":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        self.w, self.h = img.size[0], img.size[1]

    def createEmpty(self, w, h):
        pixel_data = []
        for i in range(w*h):
            pixel_data.append((0, 0, 0, 255))
        print pixel_data[:10]
        
        img_data = numpy.array(pixel_data, numpy.uint8)
        print img_data[0]

        self.ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        # if len(pixel_data[0]) == 4:
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        # elif len(pixel_data[0]) == 3:
        #     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        self.w, self.h = w, h

    def draw(self, x, y, w=None, h=None):
        if w == None:
            w, h = self.w, self.h

        if self.force_color:
            apply(glColor4f, self.force_color)
        
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glBindTexture(GL_TEXTURE_2D, self.ID)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex(x, y, self.z)
        glTexCoord2f(1, 0)
        glVertex(x + w, y, self.z)
        glTexCoord2f(1, 1)
        glVertex(x + w, y + h, self.z)
        glTexCoord2f(0, 1)
        glVertex(x, y + h, self.z)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def setColor(self, r, g, b, a=1):
        self.force_color = (r, g, b, a)

    #---------------------------------
    # Getters
    #---------------------------------

    def width(self):
        return self.w

    def height(self):
        return self.h