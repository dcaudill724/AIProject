from graphics import *
from car import *
from track import *
import math

trackSegments = 100
trackRadius = 300
trackVariance = 200
trackMidpoint = Point(400, 400)
trackWidth = 100

def main():
    win = GraphWin("AIProject", 800, 800) #initialize window
    win.setBackground(color_rgb(0, 150, 50))
    track = Track(trackSegments, trackRadius, trackVariance, trackMidpoint, trackWidth, win)

    while(True) :
        win.getMouse()
    
    


main()
