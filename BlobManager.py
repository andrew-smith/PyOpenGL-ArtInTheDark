
#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from MovingBlob import *
from ConnectionManager import *
import sys
import random
import math


# limit amount of effects there can be
MAX_EFFECTS_COUNT = 300


# A manager class to manage all the blobs

class BlobManager:

    def __init__(self):
        self.blobs = [] # an array to store all MovingBlobs
        # start listening for a client
        self.client = ClientConnection() 
        self.client.startServer()
        
        # list of effects that aren't attached to blobs 
        self.effects = []
        self.cvApp = None
        
        
        
    # called from a blob to emit an effect that shouldn't disappear when the blob does
    def emit_effect(self, effect):
        self.effects.append(effect)
        
    def update(self):
        global COLOUR_MAIN
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
        
        interaction_value = 0.25
        
        if self.client.hasNewData:
        
            glEnable(GL_TEXTURE_2D)
            glTexImage2D(GL_TEXTURE_2D, 
                0, 
                GL_RGB, 
                640, 
                480, 
                0,
                GL_RGB, 
                GL_UNSIGNED_BYTE, 
                self.cvApp.display_image)
            glDisable(GL_TEXTURE_2D)
        
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
                    if lastBlobfound is None and blob.x > x - interaction_value and blob.x < x + interaction_value:
                        if blob.y > y - interaction_value and blob.y < y + interaction_value:
                            lastBlobfound = blob
                            blob.updateReferenceCount = blob.updateReferenceCount + 1
                            blob.move(x,y)
                    
                # if blob was not found then create a new one    
                if lastBlobfound is None:
                    self.blobs.append(MovingBlob(x,y,self))
                
                
            
            
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
                
                
            # update all the effects
            effectsToRemove = []
            for effect in self.effects:
                effect.update()
                # if it is finished - remove it
                if effect.finished:
                    effectsToRemove.append(effect)
                
            # remove all finished effects
            for effect in effectsToRemove:
                self.effects.remove(effect)
                
            # limit on how many effects are displayed
            while len(self.effects) > MAX_EFFECTS_COUNT:
                self.effects.pop(0)
            
    
    
    
    def draw(self):
        """
        Draws all the blobs
        """
        glTranslatef(0.0, 0.0, 0.01)
        
        for blob in self.blobs:
            blob.draw()
           
        glTranslatef(0.0, 0.0, 0.01)
        for effect in self.effects:
            glTranslatef(0.0, 0.0, 0.001) # make effects appear on top of each other (for blending)
            effect.draw()
        
        

