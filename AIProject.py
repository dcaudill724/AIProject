from tkinter.constants import TRUE
from graphics import *
from car import *
from track import *
import time

#track variables
trackSegments = 20
trackRadius = 300
trackVariance = 300
trackMidpoint = Point(400, 400)
trackWidth = 100

#car variables
cars = []
carsPerGeneration = 1

carSpeed = 1 #pixels per frame
carColor = color_rgb(0, 255, 0)
carWidth = 10
carHeight = 16


def main():
    
    win = GraphWin("AIProject", 800, 800, False) #initialize window
    win.setBackground(color_rgb(0, 150, 50))
    

    track = Track(trackSegments, trackRadius, trackVariance, trackMidpoint, trackWidth, win) #instantiane track
    for i in range(carsPerGeneration):
        cars.append(Car([2.5], carSpeed, carWidth, carHeight, carColor, track, win, i / 10))

    

    win.updateRoot()

    #gameloop data
    training = False
    fps = 10000
    lastSecond = 0
    lastFrameTime = 0
    frameCount = 0



    #game loop
    while(True):
        currentFrameTime = time.perf_counter()

        if (currentFrameTime - lastSecond >= 1.0):
            print("fps: " + str(frameCount))
            frameCount = 0
            lastSecond = currentFrameTime - (currentFrameTime % (1.0))
            
        if (currentFrameTime - lastFrameTime >= 1.0 / fps):
            #print("here")
            #Perform game update functions in this region
            #~~~~~~~~~~~~~~~~~~~~~~~
            for i in range(carsPerGeneration):
                cars[i].update() #update car position and rotation

            if (not training):
                for i in range(carsPerGeneration):
                    cars[i].draw() #draw it all to canvas
                
                win.updateRoot()
            #~~~~~~~~~~~~~~~~~~~~~~~
            lastFrameTime = currentFrameTime - (currentFrameTime % (1.0 / fps))
            frameCount += 1
            
        
            
        
            


        
        
        
        
        
    
    


main()
