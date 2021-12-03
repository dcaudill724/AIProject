import numpy as np

# Takes a matrix of size 1 x 5
class inputLayer():
    def __init__(self, i):
        self.newInputs(i)

    def newInputs(self, i):
        self.tmp = []
        for x in i:
            self.tmp.append(self.sigmoid(x))
        
        self.inputs = []
        for i in range(4):
            self.inputs.append(self.tmp)

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def output(self):
        return self.inputs


# Takes a matrix of size 4 x 5
class hiddenLayer():

    def __init__(self, i, w):
        self.weights = w
        self.nextInput(i)
        
    def nextInput(self, i):
        self.addedInputs = []
        for x in range(len(self.weights)):
            self.addInputWeights(i[x], self.weights[x], x)

        for x in range(len(self.addedInputs)):
            self.addedInputs[x] = self.sigmoid(self.addedInputs[x])

    def addInputWeights(self, i, w, x):
        if len(self.addedInputs) <= x:
            self.addedInputs.append(0)
        for c in range(len(w)):
            self.addedInputs[x] += (i[c] * w[c])

    def sigmoid(self, x):
        return 1.0 / (1.0+ np.exp(-x))

    def output(self):
        tmp = []
        for i in range(2):
            tmp.append(self.addedInputs)
        return tmp

# Takes a matrix of size 4 x 3
class outputLayer():

    def __init__(self, i, w):
        self.weights = w
        self.nextInput(i)

    def nextInput(self, i):
        self.addedInputs = []
        for x in range(len(i)):
            self.addInputWeights(i[x], self.weights[x], x)
        
        for x in range(len(self.addedInputs)):
            self.addedInputs[x] = self.sigmoid(self.addedInputs[x])

    def addInputWeights(self, i, w, x):
        if len(self.addedInputs) <= x:
            self.addedInputs.append(0)
        for c in range(len(w)):
            self.addedInputs[x] += (i[c] * w[c])

    def sigmoid(self, x):
        return 1.0 / (1.0+ np.exp(-x))

    def output(self):
        return self.addedInputs