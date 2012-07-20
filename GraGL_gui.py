from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from GraGL import *
from GraGL_tools import *
from GraGL_font import *

# a first pass at an abstract GUI class.
class GuiElement:
    def __init__(self, x, y):
        # position/size
        self.x = x
        self.y = y
        self.w = 100
        self.h = 20
        # mouse states
        self.hover = False
        self.clicking = False
        # a font
        self.font = BitmapFont(BLOCK_8x13)
        self.font.setColor(0, 0, 0)

    # ---------------------------------------------------------------
    # this is the standard interface for using the gui elements.
    # they can be called directly from the main app's mouse callbacks,
    # however it could be useful to wrap them in a GUI controller class.
    # examples will materialize eventually.
    # ---------------------------------------------------------------

    def mouseOver(self, x, y):
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            self.hover = True
            self.hoverOnCallback()
            return 1
        else:
            if self.hover:
                self.hover = False
                self.hoverOffCallback()
            return 0

    def mousePressed(self, x, y):
        if self.hover:
            self.clicking = True
            self.pressedCallback()
            return 1
        return 0

    def mouseReleased(self, x, y):
        self.clicking = False
        if self.hover:
            self.doCallback()
            return 1
        return 0

    def mouseDragged(self, x, y):
        pass

    def hoverOnCallback(self):
        pass

    def setHoverOnCallback(self, c):
        self.hoverOnCallback = c

    def hoverOffCallback(self):
        pass

    def setHoverOffCallback(self, c):
        self.hoverOffCallback = c

    def pressedCallback(self):
        pass

    def setPressedCallback(self, c):
        self.pressedCallback = c

    def doCallback(self):
        self.callback()

    def callback(self):
        print "this gui element has no callback!"

    def setCallback(self, c):
        self.callback = c

    def draw(self):
        pass


# ------------------------------------------------------------------------------------------
# BUTTON
# ------------------------------------------------------------------------------------------


class Button(GuiElement):
    def __init__(self, label, x, y):
        GuiElement.__init__(self, x, y)
        self.font.align(CENTER)
        self.w = self.font.width(label) + 20
        self.label = label
        #
        self.color = (0.4, 0.4, 0.4)
        self.hoverColor = (0.5, 0.5, 0.5)
        self.pressedColor = (0.35, 0.35, 0.35)
        self.active = True

    def doCallback(self):
        if self.active:
            self.callback()

    def draw(self):
        pushStyle()
        self.drawShadow()
        if self.active:
            if self.hover:
                if self.clicking:
                    apply(fill, self.pressedColor)
                else:
                    apply(fill, self.hoverColor)
            else:
                apply(fill, self.color)
            stroke(0, 0, 0)
            if self.clicking:
                rectangle(self.x + 2, self.y + 2, self.w, self.h)
                self.font.text(self.label, self.x + self.w/2.0 + 2, self.y + self.h - 7 + 2)
            else:
                rectangle(self.x, self.y, self.w, self.h)
                self.font.text(self.label, self.x + self.w/2.0, self.y + self.h - 7)
        else:
            apply(fill, self.pressedColor)
            stroke(0,0,0)
            rectangle(self.x, self.y, self.w, self.h)
            self.font.text(self.label, self.x + self.w/2.0, self.y + self.h - 7)
            noStroke()
            fill(1, 1, 1, 0.3)
            rectangle(self.x + 1, self.y + 1, self.w - 1, self.h - 1)
        popStyle()

    def drawShadow(self):
        self._drawShadow()

    def _drawShadow(self):
        noStroke()
        fill(0, 0, 0, 0.3)
        rectangle(self.x + 5, self.y + 5, self.w, self.h)

    def disableShadow(self):
        self.drawShadow = None

    def enableShadow(self):
        self.drawShadow = self._drawShadow()

    def setActive(self):
        self.active = not self.active


# ------------------------------------------------------------------------------------------
# CHECKBOX
# ------------------------------------------------------------------------------------------

class CheckBox(GuiElement):
    def __init__(self, label, x, y):
        GuiElement.__init__(self, x, y)
        self.w = 20
        self.label = label
        self.value = False
        #
        self.color = (0.4, 0.4, 0.4)
        self.hoverColor = (0.5, 0.5, 0.5)
        self.pressedColor = (0.35, 0.35, 0.35)

    def draw(self):
        pushStyle()
        self.drawShadow()
        if self.hover:
            if self.clicking:
                apply(fill, self.pressedColor)
            else:
                apply(fill, self.hoverColor)
        else:
            apply(fill, self.color)
        stroke(0, 0, 0)
        if self.clicking:
            rectangle(self.x + 2, self.y + 2, self.w, self.h)
        else:
            rectangle(self.x, self.y, self.w, self.h)
        if self.value == True:
            # draw the X if we're checked
            if self.clicking:
                x, y = self.x + 2, self.y + 2
            else:
                x, y = self.x, self.y
            beginShape(OPEN_LINE)
            vertex(x, y)
            vertex(x + self.w, y + self.h)
            endShape()
            beginShape(OPEN_LINE)
            vertex(x + self.w, y)
            vertex(x, y + self.h)
            endShape()
        self.font.text(self.label, self.x + self.w + 7, self.y + self.h - 7)
        popStyle()

    def doCallback(self):
        self.value = not self.value
        self.callback()

    def drawShadow(self):
        self._drawShadow()

    def _drawShadow(self):
        noStroke()
        fill(0, 0, 0, 0.3)
        rectangle(self.x + 5, self.y + 5, self.w, self.h)

    def disableShadow(self):
        self.drawShadow = None

    def enableShadow(self):
        self.drawShadow = self._drawShadow()


# ------------------------------------------------------------------------------------------
# SLIDER
# ------------------------------------------------------------------------------------------

class Slider(GuiElement):
    def __init__(self, x, y):
        GuiElement.__init__(self, x, y)
        self.position = 0.5
        self.color = (0.4, 0.4, 0.4)
        self.locked = False
        self.xoffset = 0
    
    def p(self):
        return self.x + self.w*self.position
    
    def mouseOver(self, x, y):
        if self.x+self.w*self.position-5 < x < self.x+self.w*self.position+5 and self.y < y < self.y + self.h:
            self.hover = True
            self.hoverOnCallback()
            return 1
        else:
            if self.hover:
                self.hover = False
                self.hoverOffCallback()
            return 0
    
    def mouseDragged(self, x, y):
        if self.hover and not self.locked:
            self.locked = True
            self.xoffset = (self.x + self.w*self.position) - x
        elif self.hover and self.locked:
            self.position = (x + self.xoffset - self.x) / float(self.w)
            self.position = constrain(self.position, 0, 1)
            self.callback(self.position)
    
    def draw(self):
        pushStyle()
        self.drawShadow()
        stroke(0, 0, 0)
        line(self.x, self.y + self.h/2.0, self.x + self.w, self.y + self.h/2.0)
        line(self.x, self.y + 5, self.x, self.y + self.h - 5)
        line(self.x + self.w, self.y + 5, self.x + self.w, self.y + self.h - 5)
        apply(fill, self.color)
        rectangle(self.p() - 5, self.y, 10, 20)
        if self.hover:
            if self.clicking:
                fill(0, 0, 0, 0.2)
                noStroke()
                rectangle(self.p() - 4, self.y + 1, 9, 19)
            else:
                fill(1, 1, 1, 0.2)
                noStroke()
                rectangle(self.p() - 4, self.y + 1, 9, 19)
    
    def doCallback(self):
        self.locked = False
        self.callback(self.position)
    
    def drawShadow(self):
        self._drawShadow()

    def _drawShadow(self):
        noStroke()
        fill(0, 0, 0, 0.3)
        rectangle(self.p(), self.y + 5, 10, 20)

    def disableShadow(self):
        self.drawShadow = None

    def enableShadow(self):
        self.drawShadow = self._drawShadow()
    
    def setWidth(self, w):
        self.w = w


class VSlider(GuiElement):
    def __init__(self, x, y, h=100):
        GuiElement.__init__(self, x, y)
        self.w, self.h = 20, h
        self.position = 0.5
        self.color = (0.4, 0.4, 0.4)
        self.locked = False
        self.yoffset = 0
    
    def p(self):
        return self.y + self.h*self.position
    
    def mouseOver(self, x, y):
        if self.p()-5 < y < self.p()+5 and self.x-10 < x < self.x + self.w-10:
            self.hover = True
            self.hoverOnCallback()
            return 1
        else:
            if self.hover:
                self.hover = False
                self.hoverOffCallback()
            return 0
    
    def mouseDragged(self, x, y):
        if self.hover and not self.locked:
            self.locked = True
            self.yoffset = (self.y + self.h*self.position) - y
        elif self.hover and self.locked:
            self.position = (y + self.yoffset - self.y) / float(self.h)
            self.position = constrain(self.position, 0, 1)
            self.callback(self.position)
    
    def draw(self):
        pushStyle()
        self.drawShadow()
        stroke(0, 0, 0)
        # line(self.x, self.y + self.h/2.0, self.x + self.w, self.y + self.h/2.0)
        line(self.x, self.y, self.x, self.y+self.h)
        # line(self.x, self.y + 5, self.x, self.y + self.h - 5)
        # line(self.x + self.w, self.y + 5, self.x + self.w, self.y + self.h - 5)
        apply(fill, self.color)
        rectangle(self.x-10, self.p()-5, 20, 10)
        if self.hover:
            if self.clicking:
                fill(0, 0, 0, 0.2)
                noStroke()
                rectangle(self.x-10, self.p()-5, 19, 9)
            else:
                fill(1, 1, 1, 0.2)
                noStroke()
                rectangle(self.x-10, self.p()-5, 19, 9)
    
    def doCallback(self):
        self.locked = False
        self.callback(self.position)

    def callback(self, p):
        pass
    
    def drawShadow(self):
        self._drawShadow()

    def _drawShadow(self):
        noStroke()
        fill(0, 0, 0, 0.3)
        rectangle(self.x-5, self.p(), 20, 10)

    def disableShadow(self):
        self.drawShadow = None

    def enableShadow(self):
        self.drawShadow = self._drawShadow()
    
    def setHeight(self, h):
        self.h = h


class VBlockSlider(GuiElement):
    def __init__(self, x, y, h=100):
        GuiElement.__init__(self, x, y)
        self.w, self.h = 20, h
        self.position = 0.5
        self.color = (0.4, 0.4, 0.4)
        self.locked = False
        self.yoffset = 0
    
    def p(self):
        return self.y + self.h*self.position
    
    def mouseOver(self, x, y):
        if self.p()-5 < y < self.p()+5 and self.x-10 < x < self.x + self.w-10:
            self.hover = True
            self.hoverOnCallback()
            return 1
        else:
            if self.hover:
                self.hover = False
                self.hoverOffCallback()
            return 0
    
    def mouseDragged(self, x, y):
        if self.hover and not self.locked:
            self.locked = True
            self.yoffset = (self.y + self.h*self.position) - y
        elif self.hover and self.locked:
            self.position = (y + self.yoffset - self.y) / float(self.h)
            self.position = constrain(self.position, 0, 1)
            self.callback(self.position)
    
    def draw(self):
        pushStyle()
        self.drawShadow()
        stroke(0, 0, 0)
        # line(self.x, self.y + self.h/2.0, self.x + self.w, self.y + self.h/2.0)
        line(self.x, self.y, self.x, self.y+self.h)
        # line(self.x, self.y + 5, self.x, self.y + self.h - 5)
        # line(self.x + self.w, self.y + 5, self.x + self.w, self.y + self.h - 5)
        apply(fill, self.color)
        rectangle(self.x-10, self.p()-5, 20, 10)
        if self.hover:
            if self.clicking:
                fill(0, 0, 0, 0.2)
                noStroke()
                rectangle(self.x-10, self.p()-5, 19, 9)
            else:
                fill(1, 1, 1, 0.2)
                noStroke()
                rectangle(self.x-10, self.p()-5, 19, 9)
    
    def doCallback(self):
        self.locked = False
        self.callback(self.position)

    def callback(self, p):
        pass
    
    def drawShadow(self):
        self._drawShadow()

    def _drawShadow(self):
        noStroke()
        fill(0, 0, 0, 0.3)
        rectangle(self.x-5, self.p(), 20, 10)

    def disableShadow(self):
        self.drawShadow = None

    def enableShadow(self):
        self.drawShadow = self._drawShadow()
    
    def setHeight(self, h):
        self.h = h

# -------------------------------------------------------------

class EvolverSlider(GuiElement):
    def __init__(self, x, y, label):
        GuiElement.__init__(self, x, y)
        self.label = label
        self.position = 0
        self.color = (0.4, 0.4, 0.4)
        self.locked = Falses
        self.xoffset = 0
    
    def p(self):
        return self.x + self.w*self.position
    
    def mouseOver(self, x, y):
        if self.x+self.w*self.position-5 < x < self.x+self.w*self.position+5 and self.y < y < self.y + self.h:
            self.hover = True
            self.hoverOnCallback()
            return 1
        else:
            if self.hover:
                self.hover = False
                self.hoverOffCallback()
            return 0
    
    def mouseDragged(self, x, y):
        if self.hover and not self.locked:
            self.locked = True
            self.xoffset = (self.x + self.w*self.position) - x
        elif self.hover and self.locked:
            self.position = (x + self.xoffset - self.x) / float(self.w)
            self.position = constrain(self.position, 0, 1)
            self.callback(self, self.position)
    
    def draw(self):
        pushStyle()
        self.drawShadow()
        stroke(0, 0, 0)
        line(self.x, self.y + self.h/2.0, self.x + self.w, self.y + self.h/2.0)
        line(self.x, self.y + 5, self.x, self.y + self.h - 5)
        line(self.x + self.w, self.y + 5, self.x + self.w, self.y + self.h - 5)
        apply(fill, self.color)
        rectangle(self.p() - 5, self.y, 10, 20)
        if self.hover:
            if self.clicking:
                fill(0, 0, 0, 0.2)
                noStroke()
                rectangle(self.p() - 4, self.y + 1, 9, 19)
            else:
                fill(1, 1, 1, 0.2)
                noStroke()
                rectangle(self.p() - 4, self.y + 1, 9, 19)
        self.font.text(str(int(self.position*127))+" "+self.label, self.x + self.w + 20, self.y + 14)
    
    def doCallback(self):
        self.locked = False
        self.callback(self, self.position)

    def callback(self, c, p):
        pass
    
    def drawShadow(self):
        self._drawShadow()

    def _drawShadow(self):
        noStroke()
        fill(0, 0, 0, 0.3)
        rectangle(self.p(), self.y + 5, 10, 20)

    def disableShadow(self):
        self.drawShadow = None

    def enableShadow(self):
        self.drawShadow = self._drawShadow()
    
    def setWidth(self, w):
        self.w = w