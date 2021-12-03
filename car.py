from graphics import *
import math
from neuralNetwork import *
import random

class Car:
    def __init__(self, dna, speed, width, height, color, track, win):
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
        
    def reset(self):
        self.carBody.undraw()
        for i in range(self.rayDirections.__len__()):
            self.rays[i].undraw()   

        #initial movement data
        self.position = self.track.midPointList[0]
        self.direction = Point(0, -1)
        
        #initial rays
        self.rayDirections = [Point(-1, 0), Point(-math.sqrt(2)/2, -math.sqrt(2)/2), Point(0, -1), Point(math.sqrt(2)/2, -math.sqrt(2)/2), Point(1, 0)]
        self.rays = []
        self.rayData = []
        for i in range(self.rayDirections.__len__()):
            self.rays.append(Line(self.position, Point(self.position.x + self.rayDirections[i].x * 200, self.position.y + self.rayDirections[i].y * 200)))
            
        #initial body daya
        self.carCorners = [
                Point(-self.width/2, -self.height/2), 
                Point(-self.width/2, self.height/2),
                Point(self.width/2, self.height/2),
                Point(self.width/2, -self.height/2)
        ]
        self.carBody = Polygon()

        #initial neural network data
        self.generateNeuralNetork()

        #initial genetic algorithm data
        self.lastClosestTrackSegment = 0
        self.loopsCompleted = 0
        self.fitnessScore = 0

        #self.draw()

    #generates the neural network that controls the car direction
    def generateNeuralNetork(self):
        self.nn = NeuralNetwork([0, 0, 0, 0, 0], self.dna)

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

        self.updateDirection() #Rotate body data and determine how much to turn using neural network
        self.position = Point(self.position.x + self.direction.x * self.speed, self.position.y + self.direction.y * self.speed) #move in the relative forward direction
        
        #st = time.perf_counter()
        self.rayData = self.getRayData() #cast rays and get distance info
        #et = time.perf_counter()

        if (self.checkCollision()): #if the car collides with the wall
            self.position = lastPosition
        
        
        
        self.getFitnessScore() #get the current fitness score
        
        #print(et - st)

    
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
            self.rays[i].setFill(color_rgb(0, 0, 255))
            self.rays[i].draw(self.win)   


    #get the distances from the rays to the walls
    def getRayData(self):
        rayData = [0, 0, 0, 0, 0]
        
        
        currentSeg = int(self.fitnessScore % self.track.numOfSegments)
        checkRange = int(self.track.numOfSegments / 2)

        relativePosX = self.position.x - 400
        relativePosY = 400 - self.position.y

        
        quadrant = ""
        if (relativePosX < 0): #left side
            if (relativePosY >= 0): #top side
                quadrant = "top left"
            else: #bottom side
                quadrant = "bottom left"
        else: #right side
            if (relativePosY >= 0): #top side
                quadrant = "top right"
            else: #bottom side
               quadrant = "bottom right"
        
        
        for rd in range(self.rayDirections.__len__()):
            if (quadrant == "top left"):
                
                if(self.rayDirections[rd].y <= 0):
                    rayData[rd] = self.rayCheckForwardBackward(rd, currentSeg, checkRange)
                else:
                    rayData[rd] = self.rayCheckBackwardForward(rd, currentSeg, checkRange)
                
            elif (quadrant == "top right"):
                if(self.rayDirections[rd].x >= 0):
                    rayData[rd] = self.rayCheckForwardBackward(rd, currentSeg, checkRange)
                else:
                    rayData[rd] = self.rayCheckBackwardForward(rd, currentSeg, checkRange)

            elif (quadrant == "bottom left"):
                if(self.rayDirections[rd].x <= 0):
                    rayData[rd] = self.rayCheckForwardBackward(rd, currentSeg, checkRange)
                else:
                    rayData[rd] = self.rayCheckBackwardForward(rd, currentSeg, checkRange)

            elif (quadrant == "bottom right"):
                if(self.rayDirections[rd].y >= 0):
                    rayData[rd] = self.rayCheckForwardBackward(rd, currentSeg, checkRange)
                else:
                    rayData[rd] = self.rayCheckBackwardForward(rd, currentSeg, checkRange)

        
        
        return rayData

    def rayCheckForwardBackward(self, rd, currentSeg, checkRange):
        closestDist = float('inf')
        closestDist = self.rayCheckForward(rd, currentSeg, checkRange)

        if (closestDist != float('inf')):
            return closestDist

        closestDist = self.rayCheckBackward(rd, currentSeg, checkRange)
        return closestDist

    def rayCheckBackwardForward(self, rd, currentSeg, checkRange):
        closestDist = float('inf')
        closestDist = self.rayCheckBackward(rd, currentSeg, checkRange)
        
        if (closestDist != float('inf')):
            return closestDist

        closestDist = self.rayCheckForward(rd, currentSeg, checkRange)
        
        return closestDist

    def rayCheckForward(self, rd, currentSeg, checkRange):
        closestDist = float('inf')
        
        for i in range(currentSeg, currentSeg + checkRange):
            outsideHitDist = self.rayLineIntersection(self.position, self.rayDirections[rd], self.track.outsidePointList[i % self.track.numOfSegments], self.track.outsidePointList[(i - 1) % self.track.numOfSegments])
            if (outsideHitDist != -1):
                closestDist = outsideHitDist

            insideHitDist = self.rayLineIntersection(self.position, self.rayDirections[rd], self.track.insidePointList[i % self.track.numOfSegments], self.track.insidePointList[(i - 1) % self.track.numOfSegments])
            if (insideHitDist != -1):
                if (outsideHitDist == -1 or (outsideHitDist != -1 and insideHitDist < outsideHitDist)):
                    closestDist = insideHitDist
                
            if (closestDist != float('inf')):
                break
        
        return closestDist

    def rayCheckBackward(self, rd, currentSeg, checkRange):
        closestDist = float('inf')

        for i in range(currentSeg, currentSeg - checkRange, -1):
            outsideHitDist = self.rayLineIntersection(self.position, self.rayDirections[rd], self.track.outsidePointList[i % self.track.numOfSegments], self.track.outsidePointList[(i + 1) % self.track.numOfSegments])
            if (outsideHitDist != -1):
                closestDist = outsideHitDist

            insideHitDist = self.rayLineIntersection(self.position, self.rayDirections[rd], self.track.insidePointList[i % self.track.numOfSegments], self.track.insidePointList[(i + 1) % self.track.numOfSegments])
            if (insideHitDist != -1):
                if (outsideHitDist == -1 or (outsideHitDist != -1 and insideHitDist < outsideHitDist)):
                    closestDist = insideHitDist
                
            if (closestDist != float('inf')):
                break

        return closestDist

    #input ray data into nn, get new direction data, turn the car accordingly
    def updateDirection(self):
        angle = 0#this will later be calculated from newDirectionData
        

        if (len(self.rayData) != 0):
            mappedRayData = self.rayData.copy()
            for i in range(len(self.rayData)):
                mappedRayData[i] /= 400

            self.nn.nextInputs(mappedRayData)
            directionData = self.nn.output()
            turnRight = directionData[1]
            turnLeft = directionData[0]
            turnTotal = turnRight - turnLeft
            angle = turnTotal
            #print(mappedRayData)
        
        
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

        for r in range(1, self.rayData.__len__() - 1):
            if (self.rayData[r] < 5):
                return True

        return False