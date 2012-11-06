
#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from MovingBlob import *
from ConnectionManager import *
import sys
import random
import math


# helper function to remove blobs from lists who aren't updated




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
        
        """
        Each point sent from the client searches an area around it
        to see if this point is from an existing point (from the last update).
        
        This area is also the same size as points that interact with each other.
        If two blobs come together as one then an effect needs to be displayed.
        This will have to be configured on site when tweaking the camera position.
        
        This interaction_value is how many OpenGL units radius to search for the 
        last position
        TODO tweak this value to suit site
        """
        
        interaction_value = 0.5
        
        if self.client.hasNewData:
            # alert blobs that a new update is coming
            for blob in self.blobs:
                blob.updateReferenceCount = 0
            
            # grab the latest blob centroids from client
            latestPoints = self.client.get_new_points()
            for p in latestPoints:
                # get 2D coordinates
                x = ((p[0] / 640.0) * 6.0) - 3.0
                y = (((480.0 - p[1]) / 480.0) * 6.0) - 3.0
                
                
                # loop through current blobs to try and find this blob
                lastBlobfound = None
                for blob in self.blobs:
                    if blob.x > x - interaction_value and blob.x < x + interaction_value:
                        lastBlobfound = blob
                        blob.updateReferenceCount = blob.updateReferenceCount + 1
                        blob.move(x,y)
                    
                # if blob was not found then create a new one    
                if lastBlobfound is None:
                    self.blobs.append(MovingBlob(x,y))
                
                
            
            
            # now remove all blobs that weren't updated
            blobsToRemove = []
            
            for blob in self.blobs:
                if blob.updateReferenceCount is 0:
                    blobsToRemove.append(blob)
            for blob in blobsToRemove:
                blob.dispose()
                self.blobs.remove(blob)
            
            # update all blobs
            for blob in self.blobs:
                blob.update()
                
    
    
    
    def draw(self):
        """
        Draws all the blobs
        """
        glTranslatef(0.0, 0.0, 0.01)
        
        for blob in self.blobs:
            blob.draw()
            
        
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
            
        
        

