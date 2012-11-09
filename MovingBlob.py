#!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import random

from GLCircles import *

# how many old points to keep track of
AMT_OLD_POINTS = 125

COLOUR_MAIN = (0.388, 0.721, 1.0)

# class/enum to set drawing mode
class DrawMode:
    RotatingBlobs=1 # circle with circles rotating around
    BlobPhatTrails=2 # bloby trails that disappear (show where the blob has been)
    BlobTrails=3 #thin trailing lines (show where the blob has been)
    BubblesBubblesBubbles=4
  
    

CURRENT_DRAW_MODE = DrawMode.BlobTrails

# helper function to reverse negative numbers
def ensurePositiveNum(value):
    if value < 0:
        value *= -1
    return value


def randomBrightColour():

    # generate high random float value
    r = randomHighFloatValue()
    g = randomHighFloatValue()
    b = randomHighFloatValue()
    
    colour = [r,g,b]

    # pick either r,g,b to be zero
    randZero = random.randint(0,2)
    colour[randZero] = 0
    
    return colour

# helper method for the randomBrightColour
def randomHighFloatValue():
    # get a random number between 0 and 55
    randNum = random.random() * 55.0
    # move it to 200 to 255
    randNum += 200
    # move it to 0.0 to 1.0
    return randNum/255.0


# 0.03 = 3% chance of bubble popping off
RAND_BUBBLE_RATE = 0.1 # number between 0 and 1 to randomly generate a bubble


# Defines a moving blob in a 2D world

class MovingBlob:

    def __init__(self,x,y,emitter):
        self.x = x
        self.y = y
        self.disposed = False
        self.rotation = 0
        self.drawmode = CURRENT_DRAW_MODE
        self.emitter = emitter
        
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
        
        # randomly display a bubble popping off
        if random.random() < RAND_BUBBLE_RATE:
            self.emitter.emit_effect(BubbleParticleEffect(x,y))
        
        
    
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
                
            if self.drawmode is DrawMode.BubblesBubblesBubbles:
                handle_bubbles(self)
            

    def draw(self):
    
        if self.isActive():
            if self.drawmode is DrawMode.BlobPhatTrails:
                draw_blob_phat_trails(self)
            #elif self.drawmode is DrawMode.BubblesBubblesBubbles:
            #    handle_bubbles(self)
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
        
        
        
TRAILING_LINE_TRANSPARENCY = 0.7
    
# thin trailing line that folows blobs
# 3D enabled and alpha transparency so that lines overlap each other and get brighter
class BlobTrailEffect:


    def __init__(self,blob):
        self.blob = blob
        self.points = []
        self.finished = False
        self.colour = randomBrightColour()
        
        # this tells the effect to dispose
        # when this reaches zero
        self.ttl = AMT_OLD_POINTS
        
        
    def update(self):
    
        self.points.append( [self.blob.x, self.blob.y])
        
        # only hold the last AMT_OLD_POINTS points
        while len(self.points) > AMT_OLD_POINTS :
            p1 = self.points.pop(0)
            p2 = self.points.pop(0)
            
            if p1 is not None and p2 is not None:
                self.blob.emitter.emit_effect(DroppingLine(p1,p2,self.colour))
            
        # start killing the life of this effect    
        if not self.blob.isActive():
            self.ttl = self.ttl - 1
        if self.ttl < 0:
            self.finished = True
            
    def draw(self):
        glLineWidth(5.0)
    
        glPushMatrix()
        glColor4f(self.colour[0], self.colour[1], self.colour[2], TRAILING_LINE_TRANSPARENCY) 
        
        glBegin(GL_LINE_STRIP)
        
        for p in reversed(self.points):
            x = p[0]
            y = p[1]
            
            glVertex2f(x, y)
            
            
        glEnd()
        glPopMatrix()
    


# handles creating bubbles from blobs
def handle_bubbles(blob):
    blob.emitter.emit_effect(BubbleParticleEffect(blob.x,blob.y))
    
    
# set to true to darken the colour every update
REDUCE_COLOUR = False

def reduceColour(array, index):
    array[index] -= 0.05
    if array[index] < 0:
        array[index] = 0

class BubbleParticleEffect:
    
    def __init__(self,x,y):
    
        self.x = x
        self.y = y
        self.vectorX = (random.random() * 0.15) - 0.075
        self.vectorY = (random.random() * 0.3) - 0.15
        self.finished = False
        self.colour = randomBrightColour()
        self.ttl = 25
        
    
    
    
    def update(self):
        if not self.finished:
            # darken colour for every update
            if REDUCE_COLOUR:
                reduceColour(self.colour, 0)
                reduceColour(self.colour, 1)
                reduceColour(self.colour, 2)
            
            # move blob based on vec
            self.x += self.vectorX
            self.y += self.vectorY
            
            # apply gravity
            self.vectorY -= 0.025
            
            self.ttl -= 1
            
            if self.y < -10 or self.ttl < 1:
                self.finished = True
        
        
        
    def draw(self):
        if not self.finished:
            glPushMatrix()
            
            glTranslatef(self.x, self.y, 0.0)
            
            glColor3f(self.colour[0], self.colour[1], self.colour[2])
            glDrawCircle(0.05)
            
            glPopMatrix()
    
    
    
LINE_DROP_RATE = 0.15    

# a line that drops off a blob trail
class DroppingLine:

    def __init__(self, p1, p2, colour):
        self.p1 = p1
        self.p2 = p2
        self.colour = colour
        self.ttl = 25
        self.finished = False
        
        
        
    def update(self):
        self.p1[1] -= LINE_DROP_RATE
        self.p2[1] -= LINE_DROP_RATE
    
        self.ttl -= 1
        if self.ttl < 0:
            self.finished = True
    
    def draw(self):
        glColor4f(self.colour[0], self.colour[1], self.colour[2], TRAILING_LINE_TRANSPARENCY) 
        glBegin(GL_LINE_STRIP)
        glVertex2f(self.p1[0], self.p1[1])
        glVertex2f(self.p2[0], self.p2[1])
        glEnd()
    
