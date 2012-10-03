#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys

# Methods for drawing circles in OpenGL


def glDrawCircle(radius):

    glBegin(GL_TRIANGLE_FAN)
    
    # first point is center
    glVertex2f(0.0, 0.0)
    
    angle = 0
    while True:
        rads = math.radians(angle)
        glVertex2f(math.cos(rads) * radius, math.sin(rads) * radius)
        angle += 0.5 # smoothness of circle (increase for rough circles)
        if angle > 360:
            break
    
    glEnd()


