from graphics import *
import math

class Car:
    def __init__(self, dna, speed, width, height, color, track, win, rotationSpeed):
        self.rotationSpeed = rotationSpeed

        #Data given from constructor
        self.dna = dna
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
        self.track = track
        self.win = win

        #initial movement data
        self.position = track.midPointList[0]
        self.direction = Point(0, -1)
        
        #initial rays
        self.rayDirections = [Point(-1, 0), Point(-math.sqrt(2)/2, -math.sqrt(2)/2), Point(0, -1), Point(math.sqrt(2)/2, -math.sqrt(2)/2), Point(1, 0)]
        self.rays = []
        self.rayData = []
        for i in range(self.rayDirections.__len__()):
            self.rays.append(Line(self.position, Point(self.position.x + self.rayDirections[i].x * 200, self.position.y + self.rayDirections[i].y * 200)))
            
        #initial body daya
        self.carCorners = [
                Point(-width/2, -height/2), 
                Point(-width/2, height/2),
                Point(width/2, height/2),
                Point(width/2, -height/2)
        ]
        self.carBody = Polygon()

        #initial neural network data
        self.generateNeuralNetork()

        #initial genetic algorithm data
        self.lastClosestTrackSegment = 0
        self.loopsCompleted = 0
        self.fitnessScore = 0
        

    #generates the neural network that controls the car direction
    def generateNeuralNetork(self):
        #self.nn = NeuralNetwork(self.dna)
        return

    #obtain current fitness score
    def getFitnessScore(self):
        closestSegDistance = float('inf')
        tempClosestSeg = 0
        for i in range(self.track.numOfSegments):
            tempDist = math.sqrt(math.pow(self.track.midPointList[i].x - self.position.x, 2) + math.pow(self.track.midPointList[i].y - self.position.y, 2))
            if (tempDist < closestSegDistance):
                closestSegDistance = tempDist
                tempClosestSeg = i

        if (self.lastClosestTrackSegment == self.track.numOfSegments - 1 and tempClosestSeg == 0):
            self.loopsCompleted += 1
        if (self.lastClosestTrackSegment == 0 and tempClosestSeg == self.track.numOfSegments - 1):
            self.loopsCompleted -= 1

        self.lastClosestTrackSegment = tempClosestSeg

        self.fitnessScore = self.loopsCompleted * self.track.numOfSegments + self.lastClosestTrackSegment

    #update direction and move car
    def update(self):
        lastPosition = self.position

        self.rayData = self.getRayData() #cast rays and get distance info

        self.updateDirection() #Rotate body data and determine how much to turn using neural network
        self.position = Point(self.position.x + self.direction.x * self.speed, self.position.y + self.direction.y * self.speed) #move in the relative forward direction

        if (self.checkCollision()): #if the car collides with the wall
            self.position = lastPosition
        
        self.getFitnessScore() #get the current fitness score

    
    def draw(self):
        #update graphics with new data
        self.carBody.undraw()
        tempCorners = []
        for p in self.carCorners:
            tempCorners.append(Point(p.x + self.position.x, p.y + self.position.y))
        self.carBody = Polygon(tempCorners)
        self.carBody.setWidth(0)
        self.carBody.setFill(self.color)
        self.carBody.draw(self.win)

        for i in range(self.rayDirections.__len__()):
            self.rays[i].undraw()
            self.rays[i] = Line(self.position, Point(self.position.x + self.rayDirections[i].x * self.rayData[i], self.position.y + self.rayDirections[i].y * self.rayData[i]))
            self.rays[i].setWidth(1)  
            self.rays[i].setFill(color_rgb(255, 0, 0))
            self.rays[i].draw(self.win)   

    #get the distances from the rays to the walls
    def getRayData(self):
        rayData = []

        segStartIndex = (self.fitnessScore % self.track.numOfSegments - self.track.numOfSegments / 4)
        if (segStartIndex < 0): 
            segStartIndex = self.track.numOfSegments + segStartIndex
            
        segEndIndex = (self.fitnessScore % self.track.numOfSegments + self.track.numOfSegments / 4)
        if (segEndIndex > self.track.numOfSegments - 1): 
            segEndIndex = self.track.numOfSegments - 1 - segEndIndex

        if (segStartIndex < segEndIndex):
            buffer = segEndIndex
            segEndIndex = segStartIndex
            segStartIndex = buffer

        for r in range(self.rayDirections.__len__()): #check all rays
            closestWallDist = float('inf')
            for i in range(int(segStartIndex)): #for each ray check all wall segments
                insideHitDist = self.rayLineIntersection(self.position, self.rayDirections[r], self.track.insidePointList[i], self.track.insidePointList[(i + 1) % self.track.numOfSegments])
                outsideHitDist = self.rayLineIntersection(self.position, self.rayDirections[r], self.track.outsidePointList[i], self.track.outsidePointList[(i + 1) % self.track.numOfSegments])
                if (insideHitDist != -1 and insideHitDist < closestWallDist):
                    closestWallDist = insideHitDist
                if (outsideHitDist != -1 and outsideHitDist < closestWallDist):
                    closestWallDist = outsideHitDist

            for i in range(int(segEndIndex), self.track.numOfSegments): #for each ray check all wall segments
                insideHitDist = self.rayLineIntersection(self.position, self.rayDirections[r], self.track.insidePointList[i], self.track.insidePointList[(i + 1) % self.track.numOfSegments])
                outsideHitDist = self.rayLineIntersection(self.position, self.rayDirections[r], self.track.outsidePointList[i], self.track.outsidePointList[(i + 1) % self.track.numOfSegments])
                if (insideHitDist != -1 and insideHitDist < closestWallDist):
                    closestWallDist = insideHitDist
                if (outsideHitDist != -1 and outsideHitDist < closestWallDist):
                    closestWallDist = outsideHitDist

            rayData.append(closestWallDist)

        return rayData

    #input ray data into nn, get new direction data, turn the car accordingly
    def updateDirection(self):
        #newDirectionData = self.nn.GetNextDirectionData(self.getRayData())
        angle = self.rotationSpeed / 60 #this will later be calculated from newDirectionData
        
        #rotate direction
        self.direction = self.rotateVector(self.direction, angle)

        #rotate car body
        newCorners = []
        for p in self.carCorners:
            newCorners.append(self.rotateVector(p, angle))
        self.carCorners = newCorners

        #rotate rays
        newRayDirections = []
        for p in self.rayDirections:
            newRayDirections.append(self.rotateVector(p, angle))
        self.rayDirections = newRayDirections

    def rotateVector(self, vecAsPoint, angle):
        newX = math.cos(angle) * vecAsPoint.x - math.sin(angle) * vecAsPoint.y
        newY = math.sin(angle) * vecAsPoint.x + math.cos(angle) * vecAsPoint.y
        return Point(newX, newY)

    def rayLineIntersection(self, rayOrigin, rayDirection, linep1, linep2):
        vector1 = Point(rayOrigin.x - linep1.x, rayOrigin.y - linep1.y) #rayOrigin - p1
        vector2 = Point(linep2.x - linep1.x, linep2.y - linep1.y) #p2 - p1
        vector3 = Point(-rayDirection.y, rayDirection.x)

        #vector2 * vector3
        dot = (vector2.x * vector3.x) + (vector2.y * vector3.y)

        #if parallel
        if (abs(dot) < 0.000001):
            return -1
        
        #(vector2 x vector1) / dot
        test1 = ((vector2.x * vector1.y) - (vector2.y * vector1.x)) / dot
        test2 = ((vector1.x * vector3.x) + (vector1.y * vector3.y)) / dot

        if (test1 > 0.0 and (test2 >= 0.0 and test2 <= 1.0)):
            return test1
        
        return -1

    def checkCollision(self):
        if (self.carBody.getPoints().__len__() == 0): #is only true first frame but is need so it doesn't break
            return False
        
        topLeft = self.carBody.getPoints()[0]
        bottomLeft = self.carBody.getPoints()[1]
        topRight = self.carBody.getPoints()[3]
        bottomRight = self.carBody.getPoints()[2]

        topLeftToBottomLeftDir = Point((bottomLeft.x - topLeft.x) / self.height, (bottomLeft.y - topLeft.y) / self.height)
        topLeftToTopRightDir = Point((topRight.x - topLeft.x) / self.width, (topRight.y - topLeft.y) / self.width)
        topRightToBottomRightDir = Point((bottomRight.x - topRight.x) / self.height, (bottomRight.y - topRight.y) / self.height)

        for i in range(self.track.numOfSegments):
            topLeftToBottomLeftOutsideDist = self.rayLineIntersection(topLeft, topLeftToBottomLeftDir, self.track.outsidePointList[i], self.track.outsidePointList[(i + 1) % self.track.numOfSegments])
            topLeftToBottomLeftInsideDist = self.rayLineIntersection(topLeft, topLeftToBottomLeftDir, self.track.insidePointList[i], self.track.insidePointList[(i + 1) % self.track.numOfSegments])
            if ((topLeftToBottomLeftOutsideDist != -1 and topLeftToBottomLeftOutsideDist <= 4) or (topLeftToBottomLeftInsideDist != -1 and topLeftToBottomLeftInsideDist <= 4)):
                return True

            topLeftToTopRightOutsideDist = self.rayLineIntersection(topLeft, topLeftToTopRightDir, self.track.outsidePointList[i], self.track.outsidePointList[(i + 1) % self.track.numOfSegments])
            topLeftToTopRightInsideDist = self.rayLineIntersection(topLeft, topLeftToTopRightDir, self.track.insidePointList[i], self.track.insidePointList[(i + 1) % self.track.numOfSegments])
            if ((topLeftToTopRightOutsideDist != -1 and topLeftToTopRightOutsideDist <= self.width) or (topLeftToTopRightInsideDist != -1 and topLeftToTopRightInsideDist <= self.width)):
                return True

            topRightToBottomRightOutsideDist = self.rayLineIntersection(topRight, topRightToBottomRightDir, self.track.outsidePointList[i], self.track.outsidePointList[(i + 1) % self.track.numOfSegments])
            topRightToBottomRightInsideDist = self.rayLineIntersection(topRight, topRightToBottomRightDir, self.track.insidePointList[i], self.track.insidePointList[(i + 1) % self.track.numOfSegments])
            if ((topRightToBottomRightOutsideDist != -1 and topRightToBottomRightOutsideDist <= 4) or (topRightToBottomRightInsideDist != -1 and topRightToBottomRightInsideDist <= self.height / 4)):
                return True
        
        return False