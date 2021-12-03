from tkinter.constants import TRUE

from numpy import generic
from graphics import *
from car import *
from neuralNetwork import NeuralNetwork
from track import *
from genetic import Genetic
import time
import random


#track variables
trackSegments = 40
trackRadius = 300
trackVariance = 100
trackMidpoint = Point(400, 400)
trackWidth = 100

#car variables
cars = []
carsPerGeneration = 10

carSpeed = 1 #pixels per frame
carColor = color_rgb(0, 255, 0)
carWidth = 10
carHeight = 16

#Genetic algorithm variables
framesPerGeneration = 1200
carsPerGeneration = 10
topCarsToBreed = 2
mutationChance = 0.03

def main():
    
    win = GraphWin("AIProject", 800, 800, False) #initialize window
    win.setBackground(color_rgb(0, 150, 50))
    
    track = Track(trackSegments, trackRadius, trackVariance, trackMidpoint, trackWidth, win) #instantiane track
    genetic = Genetic(carsPerGeneration, mutationChance, carSpeed, carWidth, carHeight, carColor, track, win)
    

    win.updateRoot()

    #gameloop data
    training = False
    fps = 10000
    lastFrameTime = 0
    frameCount = 0
    lastGenerationFrame = 0

    #game loop
    while(True):
        currentFrameTime = time.perf_counter()

        if (frameCount - lastGenerationFrame == framesPerGeneration):
            genetic.newGen(topCarsToBreed)
            lastGenerationFrame = frameCount

        if (currentFrameTime - lastFrameTime >= 1.0 / fps):

            #Perform game update functions in this region
            #~~~~~~~~~~~~~~~~~~~~~~~
            for i in range(carsPerGeneration):
                genetic.carList[i].update() #update car position and rotation
                

            if (not training):
                for i in range(carsPerGeneration):
                    genetic.carList[i].draw() #draw it all to canvas
                win.updateRoot()

            #~~~~~~~~~~~~~~~~~~~~~~~

            #Time tracking
            lastFrameTime = currentFrameTime - (currentFrameTime % (1.0 / fps))
            frameCount += 1

        
            
        
            
        
            


        
        
        
        
        
    
    


main()
