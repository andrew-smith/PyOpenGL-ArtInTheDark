#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


# Defines a moving blob in a 2D world

class MovingBlob:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        self.y += 0.01

    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y, 0.0)
        
        glBegin(GL_POLYGON)                 # Start drawing a polygon
        glColor3f(1.0, 0.0, 0.0)            # Red
        glVertex3f(0.0, 1.0, 0.0)           # Top
        glColor3f(0.0, 1.0, 0.0)            # Green
        glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
        glColor3f(0.0, 0.0, 1.0)            # Blue
        glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
        glEnd()    
        
        glPopMatrix()

