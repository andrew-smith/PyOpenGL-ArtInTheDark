#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys


# amount of degrees to step circles 
CIRCLE_ANGLE_INC = 45


# Methods for drawing circles in OpenGL
def glDrawCircle(radius):

    glBegin(GL_TRIANGLE_FAN)
    
    # first point is center
    glVertex2f(0.0, 0.0)
    
    angle = 0
    while True:
        rads = math.radians(angle)
        glVertex2f(math.cos(rads) * radius, math.sin(rads) * radius)
        angle += CIRCLE_ANGLE_INC # smoothness of circle (increase for rough circles)
        if angle > 360:
            break
    
    glEnd()
    
    
    
def glDrawTransparentCircle(radius, colourR, colourG, colourB):
    """
    Inside colour should have been set before this function
    """
    
    glBegin(GL_TRIANGLE_FAN)
    
    # first point is center
    glVertex2f(0.0, 0.0)
    
    #set outside transparent colour
    glColor4f(colourR, colourG, colourB, 0.0)
    
    angle = 0
    while True:
        rads = math.radians(angle)
        glVertex2f(math.cos(rads) * radius, math.sin(rads) * radius)
        angle += CIRCLE_ANGLE_INC # smoothness of circle (increase for rough circles)
        if angle > 360:
            break
    
    glEnd()

def glDrawInvertedTransparentCircle(radius, colourR, colourG, colourB, alpha):
    """
    No colour should have been set before this function
    """
    
    glBegin(GL_TRIANGLE_FAN)
    
    #set inside transparent colour
    glColor4f(colourR, colourG, colourB, 0.0)
    # first point is center
    glVertex2f(0.0, 0.0)
    
    
    #set outside non-transparent colour
    glColor4f(colourR, colourG, colourB, alpha)
    angle = 0
    while True:
        rads = math.radians(angle)
        glVertex2f(math.cos(rads) * radius, math.sin(rads) * radius)
        angle += CIRCLE_ANGLE_INC # smoothness of circle (increase for rough circles)
        if angle > 360:
            break
    
    glEnd()
    
    
