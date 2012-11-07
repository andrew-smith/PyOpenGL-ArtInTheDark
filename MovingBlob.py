#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import random

from GLCircles import *

# how many old points to keep track of
AMT_OLD_POINTS = 250

COLOUR_MAIN = (0.388, 0.721, 1.0)

# class/enum to set drawing mode
class DrawMode:
    RotatingBlobs=1 # circle with circles rotating around
    BlobPhatTrails=2 # bloby trails that disappear (show where the blob has been)
    BlobTrails=3 #thin trailing lines (show where the blob has been)
  
    

CURRENT_DRAW_MODE = DrawMode.BlobTrails

# helper function to reverse negative numbers
def ensurePositiveNum(value):
    if value < 0:
        value *= -1
    return value


# Defines a moving blob in a 2D world

class MovingBlob:

    def __init__(self,x,y,emitter):
        self.x = x
        self.y = y
        self.disposed = False
        self.rotation = 0
        self.drawmode = CURRENT_DRAW_MODE
        
        # if the draw mode has an effect to emit - do it now
        # effect emitter (has the function emit_effect)
        if CURRENT_DRAW_MODE is DrawMode.BlobTrails:
            emitter.emit_effect(BlobTrailEffect(self))
        
        # list of old points (Trail)
        self.oldPoints = []
        
        # used to keep track of blob being updated
        # 0  = no blobs referenced this - remove it as blob has disappeared
        # 1  = a single blob referenced this - good
        # >1 = more than one blob thinks this blob is it. This happens when 
        #      two or more blobs collide/come close to each other.
        #      A special effect should be started!
        self.updateReferenceCount = 1
        
    
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
            # only hold the last AMT_OLD_POINTS points
            while len(self.oldPoints) > AMT_OLD_POINTS :
                self.oldPoints.pop(0)
                
            # add some rotation
            self.rotation += 4
            if self.rotation > 360:
                self.rotation = 0
            

    def draw(self):
    
        if self.isActive():
            if self.drawmode is DrawMode.BlobPhatTrails:
                draw_blob_phat_trails(self)
            #elif self.drawmode is DrawMode.BlobTrails:
            #    draw_blob_trails(self)
            #else: 
            #    draw_rotating_blobs(self)







def draw_rotating_blobs(blob):
    glPushMatrix()
    
    glTranslatef(blob.x, blob.y, 0.0)
    
    glColor3f(1.0, 0.0, 0.0) # Red
    
    # draw center circle
    glDrawTransparentCircle(0.1, 1.0, 0.0, 0.0)
    
    # draw 3 circles circling it
    glRotatef(blob.rotation, 0, 0, 1)
    circleRotations = [0, 120, 240]
    
    for rotation in circleRotations:
        glPushMatrix()
        glRotatef(rotation, 0, 0, 1)
        glTranslatef(0.0, 0.2, 0.0)
        glColor3f(0.0, 0.0, 1.0) # Blue
        glDrawTransparentCircle(0.05, 0.0, 0.0, 1.0)
        glPopMatrix()
    
    glPopMatrix()


def draw_blob_phat_trails(blob):
    
    current_point_index = AMT_OLD_POINTS
    for p in reversed(blob.oldPoints):
        glPushMatrix()
        x = p[0]
        y = p[1]
        
        glTranslatef(x, y, 0.0)
        
        radius = math.sin((math.pi / AMT_OLD_POINTS) * current_point_index) * 0.2
        
        glColor3f(1.0, 1.0, 0.0) # Green/Yellow
        glDrawCircle(radius)
        
        
        current_point_index = current_point_index - 1
        glPopMatrix()
        
        
        
        
class BlobTrailEffect:


    def __init__(self,blob):
        self.blob = blob
        self.points = []
        self.finished = False
        
        # this tells the effect to dispose
        # when this reaches zero
        self.ttl = AMT_OLD_POINTS
        
        
    def update(self):
    
        self.points.append( (self.blob.x, self.blob.y))
        
        # only hold the last AMT_OLD_POINTS points
        while len(self.points) > AMT_OLD_POINTS :
            self.points.pop(0)
        
        # start killing the life of this effect    
        if not self.blob.isActive():
            self.ttl = self.ttl - 1
        if self.ttl < 0:
            self.finished = True
            
    def draw(self):
        glLineWidth(5.0)
        
        glTranslatef(0.0, 0.0, 0.01)
    
        glPushMatrix()
        glColor4f(COLOUR_MAIN[0], COLOUR_MAIN[1], COLOUR_MAIN[2], 0.35) # Green/Yellow
        
        glBegin(GL_LINE_STRIP)
        
        for p in reversed(self.points):
            x = p[0]
            y = p[1]
            
            glVertex2f(x, y)
            
            
        glEnd()
        glPopMatrix()
    

def draw_bubbles(blob):
    thing=None
    



