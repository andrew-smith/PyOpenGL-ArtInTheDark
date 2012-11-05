
#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from MovingBlob import *
from ConnectionManager import *
import sys
import random
import math


# A manager class to manage all the blobs

class BlobManager:

    def __init__(self):
        self.blobs = [] # an array to store all MovingBlobs
        # start listening for a client
        self.client = ClientConnection() 
        self.client.startServer()
        
        
        
    def update(self):
        """
        Updates all the blobs.
        """
        
        # grab the latest blob centroids and update
        for p in self.client.points:
            # get 2D coordinates
            x = ((p[0] / 640.0) * 6.0) - 3.0
            y = (((480.0 - p[1]) / 480.0) * 6.0) - 3.0
            
            
            print str(p)
        
        
        # loop through blobs
        for blob in self.blobs:
            print str(blob)
                
    
    
    
    def draw(self):
        """
        Draws all the blobs
        """
        glTranslatef(0.0, 0.0, 0.01);
        
        """
        for blob in self.blobs:
            blob.drawTrails()
        
         # draw interaction afterwards so it appears behind base blobs
        # although transparency is a slight issue here
        glTranslatef(0.0, 0.0, 0.01);
        for blob in self.blobs:
            blob.drawNeighbourInteraction()
            
        glTranslatef(0.0, 0.0,0.01);
        for blob in self.blobs:
            blob.draw()
        """
            
        
        

