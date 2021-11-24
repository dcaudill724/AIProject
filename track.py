from graphics import Point
import math
import random
from graphics import *
from perlin_noise import PerlinNoise

class Track:
    def __init__(self, numOfSegments, radius, variance, midPoint, width, win):
        self.numOfSegments = numOfSegments
        self.midPointList = []
        self.insidePointList = []
        self.outsidePointList = []
        radiansPerSegment = (math.pi * 2) / numOfSegments


        noise = PerlinNoise()
        for i in range(0, numOfSegments):
            angle = i * radiansPerSegment + math.pi

            xoff = math.cos(angle) + 1
            yoff = math.sin(angle) + 1

            noiseRadius = noise([xoff, yoff]) * variance
            noiseRadius += radius

            tempMidRadius = noiseRadius 
            midx = tempMidRadius * math.cos(angle) + midPoint.x
            midy = tempMidRadius * math.sin(angle) + midPoint.y
            self.midPointList.append(Point(midx, midy))

            tempInsideRadius = noiseRadius - width / 2
            insidex = tempInsideRadius * math.cos(angle) + midPoint.x
            insidey = tempInsideRadius * math.sin(angle) + midPoint.y
            self.insidePointList.append(Point(insidex, insidey))

            tempOutsideRadius = noiseRadius + width / 2
            outsidex = tempOutsideRadius * math.cos(angle) + midPoint.x
            outsidey = tempOutsideRadius * math.sin(angle) + midPoint.y
            self.outsidePointList.append(Point(outsidex, outsidey))

        self.draw(win)


    def draw(self, win):
        for i in range(self.numOfSegments):
            insideP1 = self.insidePointList[i]
            insideP2 = self.insidePointList[(i + 1) % self.numOfSegments]
            insideLine = Line(insideP1, insideP2)
            insideLine.setWidth(3)
            insideLine.draw(win)

            outsideP1 = self.outsidePointList[i]
            outsideP2 = self.outsidePointList[(i + 1) % self.numOfSegments]
            outsideLine = Line(outsideP1, outsideP2)
            outsideLine.setWidth(3)
            outsideLine.draw(win)

            roadPolygon = Polygon(outsideP1, insideP1, insideP2, outsideP2)
            roadPolygon.setFill(color_rgb(75, 75, 75))
            roadPolygon.setOutline(color_rgb(75, 75, 75))
            roadPolygon.setWidth(0)
            roadPolygon.draw(win)

        startline = Line(self.insidePointList[0], self.outsidePointList[0])
        startline.setFill(color_rgb(255, 0, 0))
        startline.setWidth(5)
        startline.draw(win)

        
        

    


    

    

