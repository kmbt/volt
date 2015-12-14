from pyglet.gl import *
import pyglet.gl as gl

def draw_rectangle(window, x, y, dx, dy, fill=None, border=None):
    glColor3f(*fill)

    glBegin(GL_QUADS)
    glVertex2f(x, window.height-y)
    glVertex2f(x, window.height-y-dy)
    glVertex2f(x+dx, window.height-y-dy)
    glVertex2f(x+dx, window.height-y)
    glEnd()

    if border:
        glColor3f(*border)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, window.height-y)
        glVertex2f(x, window.height-y-dy)
        glVertex2f(x+dx, window.height-y-dy)
        glVertex2f(x+dx, window.height-y)
        glEnd()
