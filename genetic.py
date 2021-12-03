import random 
from car import *


class Genetic:
    
    def __init__(self, carsPerGeneration, mutationChance, carSpeed, carWidth, carHeight, carColor, track, win):
        self.carsPerGeneration = carsPerGeneration
        self.generationNum = 0
        self.DNAlength = 28
        self.mutationChance = mutationChance
        
        self.firstGen(carsPerGeneration, carSpeed, carWidth, carHeight, carColor, track, win)
        
        
    #initial generation of random DNA for every car
    def firstGen(self, carsPerGeneration, carSpeed, carWidth, carHeight, carColor, track, win):
        print("Generation 1")
        self.generationNum += 1

        self.carList = []

        for i in range(carsPerGeneration):
            DNA = []
            for j in range(self.DNAlength):
                tempDNA = round(random.uniform(-1,1), 4)
                DNA.append(tempDNA)

            self.carList.append(Car(DNA, carSpeed, carWidth, carHeight, carColor, track, win))

                 
            
    #find the top cars with the best fitness score and add them to a pool
    def selection(self, topCarsAmount):
        li = []

        for i in range(topCarsAmount):
            bestCarIndex = 0
            bestCarFitnessScore = float('-inf')

            for j in range(len(self.carList)):
                if (self.carList[j].fitnessScore > bestCarFitnessScore):
                    if (not self.carList[j] in li):
                        bestCarIndex = j
                        bestCarFitnessScore = self.carList[j].fitnessScore
            
            li.append(self.carList[bestCarIndex])

        return li
        
    
    def crossover(self, topCarsList):
        tempCarlistDna = [0] * self.DNAlength
        randTopCar1 = topCarsList[random.randrange(0, len(topCarsList))]

        differentParents = False
        randTopCar2 = topCarsList[random.randrange(0, len(topCarsList))]
        while(not differentParents):
            if (not (randTopCar1 is randTopCar2)):
                differentParents = True
            else: 
                randTopCar2 = topCarsList[random.randrange(0, len(topCarsList))]
        

        for j in range(self.carsPerGeneration):
            tempDna = [0] * self.DNAlength
            for i in range(self.DNAlength):
                breedRand = random.uniform(-1, 1)
                if (breedRand > 0):
                    tempDna[i] = randTopCar1.dna[i]
                else:
                    tempDna[i] = randTopCar2.dna[i]
                

                tempDna[i] = self.mutation(tempDna[i])
            tempCarlistDna[j] = tempDna

        for j in range(self.carsPerGeneration):

            self.carList[j].dna = tempCarlistDna[j]

    
    
    #randomly select one gene in each cars DNA and change it
    def mutation(self, dna):
        mutationRand = random.uniform(0, 1)
        if (mutationRand <= self.mutationChance):
            mutation = round(random.uniform(-1,1), 4)#new random gene
            dna = mutation
        else:
            mutation = 0

        return dna
          
          
    #generate new dna for each car based off of the fittest cars pool
    def newGen(self, topCarsAmount):
        self.generationNum += 1
        print("Generation " + str(self.generationNum))

        topCars = self.selection(topCarsAmount)
        self.crossover(topCars)
        
        for i in range(len(self.carList)):
            self.carList[i].reset()

        
        

  
            


