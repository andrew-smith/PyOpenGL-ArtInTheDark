#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random

from GLCircles import *


# Defines a moving blob in a 2D world

class MovingBlob:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.disposed = False
        self.neighbour = None
    
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
        
    def setNeighbour(self, neighbour):
        self.neighbour = neighbour
    
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
        
    def setRandomGoTo(self):
        """
        Creates a random 2D position (debug blobs)
        """
        self.randomX = random.random() *6 -3
        self.randomY = random.random() *6 -3

    def update(self):
        """
        Moves randomly based on the position generated from setRandomGoTo()
        """
        BLOB_MOVEMENT = 0.01
        
        #move x
        if self.randomX > self.x:
            self.x += BLOB_MOVEMENT
        elif self.randomX < self.x:
            self.x -= BLOB_MOVEMENT
            
        #move y
        if self.randomY > self.y:
            self.y += BLOB_MOVEMENT
        elif self.randomY < self.y:
            self.y -= BLOB_MOVEMENT
            
        #check if position reached (stops them vibrating when they reach the position)
        if self.y > self.randomY - BLOB_MOVEMENT and self.y < self.randomY + BLOB_MOVEMENT:
            self.randomY = self.y
        if self.x > self.randomX - BLOB_MOVEMENT and self.x < self.randomX + BLOB_MOVEMENT:
            self.randomX = self.x
            
        if self.y == self.randomY and self.x == self.randomX:
            self.setRandomGoTo()
            

    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y, 0.0)
        
        glColor3f(1.0, 0.0, 0.0) # Red
        
        glDrawCircle(0.1)
        
        glPopMatrix()
        
        # draw line to neighbour
        if self.neighbour != None:
            glColor3f(0.0, 0.0, 1.0) # Blue
            
            glBegin(GL_LINES)
            
            glVertex2f(self.x, self.y)
            glVertex2f(self.neighbour.getX(), self.neighbour.getY())
            
            glEnd()

