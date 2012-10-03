
#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from MovingBlob import *
import sys
import random


# A manager class to manage all the blobs

class BlobManager:

    def __init__(self):
        self.blobs = [] # an array to store all MovingBlobs
        
        # DEBUG CODE TO GENERATE RANDOM BLOBS
        for i in range(0,10):
            blob = self.spawnBlob(random.random() *6 -3, random.random() *6 -3)
            blob.setRandomGoTo()
        
        
        
    def spawnBlob(self,x,y):
        """
        Spawns a new blob, adds it to the list, and returns it
        """
        blob = MovingBlob(x,y)
        self.blobs.append(blob)
        return blob
        
        
        
    def update(self):
        """
        Updates all the blobs.
        TODO: will check blob positions to see if blobs are close to each other
        """
        for blob in self.blobs:
            blob.update()
        
    
    
    
    
    def draw(self):
        """
        Draws all the blobs
        """
        for blob in self.blobs:
            blob.draw()
        

