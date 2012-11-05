#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import random

from GLCircles import *


# helper function to reverse negative numbers
def ensurePositiveNum(value):
    if value < 0:
        value *= -1
    return value


# Defines a moving blob in a 2D world

class MovingBlob:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.disposed = False
        self.rotation = 0
        
        self.oldPoints = []
        
        # used to keep track of blob being updated
        # if this is false after an update has occured - this blob will be discarded
        self.updated = True
        
    
    def isActive(self):
        """
        If this blob is still active in the world
        """    
        return not self.disposed
        
    def dispose(self):
        """
        Disposes this blob - should no longer be updated
        """
        self.disposed = True
       
       
    def move(self,x,y):
        """
        Moves this blob and retains it's old positions
        """
        # save original position before setting new one
        self.oldPoints.append( (self.x, self.y) )
        # set new position
        self.x = x
        self.y = y
        
        
    
    def update(self):
        """
        Updates the blob (rotation, colours, effects, etc...)
        """
        if self.isActive():
            # only hold the last 280 points
            if len(self.oldPoints) > 280 :
                self.oldPoints.pop(0)
                
            # add some rotation
            self.rotation += 4
            if self.rotation > 360:
                self.rotation = 0
            

    def draw(self):
    
        if self.isActive():
            glPushMatrix()
            
            glTranslatef(self.x, self.y, 0.0)
            
            glColor3f(1.0, 0.0, 0.0) # Red
            
            # draw center circle
            glDrawTransparentCircle(0.1, 1.0, 0.0, 0.0)
            
            # draw 3 circles circling it
            glRotatef(self.rotation, 0, 0, 1)
            circleRotations = [0, 120, 240]
            
            for rotation in circleRotations:
                glPushMatrix()
                glRotatef(rotation, 0, 0, 1)
                glTranslatef(0.0, 0.2, 0.0)
                glColor3f(0.0, 0.0, 1.0) # Blue
                glDrawTransparentCircle(0.05, 0.0, 0.0, 1.0)
                glPopMatrix()
            
            glPopMatrix()


