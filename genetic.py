import random 


class Genetic:
    
    def __init__(self, cars):
        self.carsList = cars
        self.generationNum = 0
        self.DNAlength = 10
        
        self.firstGen()
        
        
    #initial generation of random DNA for every car
    def firstGen(self):
        #self.carsList = [[]for _ in range(self.carsAmount)]
        for car in self.carsList:
            DNA = []
            for i in range(self.DNAlength):
                DNA = round(random.uniform(-1,1), 4)
                car.dna.append(DNA)
                 
            
    #find the top cars with the best fitness score and add them to a pool
    #fitnessScores is a list and the index should match its respective car in the carsList
    def selection(self, topCarsAmount, fitnessScores):
        #sorts the fitness score from lowest to highest and keeps track of its original index
        li= []
        for i in range(len(fitnessScores)):
            li.append([fitnessScores[i],i])
        li.sort()
        topCarsIndex = []
        for i in range(topCarsAmount):
          topCarsIndex.append(li[i][1])
          
        #add the cars with the best fitness scores to a pool
        topCarsList = [None for _ in range(topCarsAmount)]
        for i,val in enumerate(topCarsIndex):
            topCarsList[i] = self.carsList[val]
        
        return topCarsList
        
    
    def crossover(self, topCarsList):
        tempcarsList = []
        topCarsAmount = len(topCarsList)
        halfcars = int(topCarsAmount/2) 
        child1,child2 = [],[]
        
        for i in range(0, topCarsAmount, 2):
            parent1 = topCarsList[i].dna.copy()
            parent2 = topCarsList[i+1].dna.copy()
            
            child1 = parent1[:halfcars] + parent2[halfcars:]
            child2 = parent2[:halfcars] + parent1[halfcars:]
            
            tempcarsList.append(child1)
            tempcarsList.append(child2)
            
        return tempcarsList
    
    
    #randomly select one gene in each cars DNA and change it
    def mutation(self, topCarsList):
        for car in topCarsList:
            r = random.randint(0, self.DNAlength-1)#random gene from DNA
            gene = round(random.uniform(-1,1), 4)#new random gene
            car[r] = gene
            
        return topCarsList
          
          
    #generate new dna for each car based off of the fittest cars pool
    def newGen(self, topCarsList):
        for car in self.carsList:
              r = random.randint(0, len(topCarsList)-1)#random DNA fron top Cars pool
              car.dna = topCarsList[r]
        

  
            


