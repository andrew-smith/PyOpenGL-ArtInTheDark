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
        self.neighbours = []
        self.rotation = random.random() * 360
    
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
        
    def addNeighbour(self, neighbour):
        self.neighbours.append(neighbour)
        
    def clearNeighbours(self):
        self.neighbours = [] # reset the list
    
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
            
        #add some rotation
        self.rotation += 4
        if self.rotation > 360:
            self.rotation = 0
            

    def draw(self):
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
            glColor3f(0.0, 1.0, 0.0) # Green
            glDrawTransparentCircle(0.05, 0.0, 1.0, 0.0)
            glPopMatrix()
        
        glPopMatrix()
        
        
            
            
            
            
    def drawNeighbourInteraction(self):
        thing = self.x
        
        for neighbour in self.neighbours:
            
            origDist = math.hypot(neighbour.getX() - self.getX(), neighbour.getY() - self.getY())
            dist = ensurePositiveNum(origDist)
                    
            if dist <= 0.8: # the maximum distance to start interacting with another blob


                #find distance to each coordinate 
                boundsX = self.getX() - neighbour.getX()
                boundsY = self.getY() - neighbour.getY()
                
                
                randomX = self.getX() - boundsX/2 + ((random.random() * 0.3)-0.15)
                randomY = self.getY() - boundsY/2 + ((random.random() * 0.3)-0.15)

                glColor4f(1.0, 1.0, 0.0, 0.7) # Transparent Yellow
                
                glBegin(GL_LINE_STRIP)
                
                glVertex2f(self.x, self.y)
                #random inbetween position
                glVertex2f(randomX, randomY)
                glVertex2f(neighbour.getX(), neighbour.getY())
                
                glEnd()
    
            

