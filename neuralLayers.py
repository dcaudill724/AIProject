import numpy as np


def main():
    a = inputLayer([0.4, 0.5, 0.6, 0.7, 0.8])
    b = hiddenLayer(a.output(), [0.6, 0.7, 0.8, 0.9])
    c = outputLayer(b.output())
    print(c.output())

class inputLayer():

    def __init__(self, i):
        self.inputs = []
        for x in i:
            self.inputs.append(self.sigmoid(x))

    def sigmoid(self, x):
        return 1.0 / (1.0+ np.exp(-x))

    def output(self):
        return self.inputs


# Takes an array of arrays...  [ [1, 2, 3], [4, 5, 6], [7, 8, 9], .... ]
class hiddenLayer():

    addedInputs = []

    def __init__(self, i, w):
        #print("addIW: ")
        for x in range(len(w)):
            self.addInputWeights(i[x], w[x], x)
            #print(self.addedInputs[x])
                
        #print("sigmoid:")
        for x in range(len(self.addedInputs)):
            self.addedInputs[x] = self.sigmoid(self.addedInputs[x])
            #print(self.addedInputs[x])

    def addInputWeights(self, i, w, x):
        if len(self.addedInputs) <= x:
            self.addedInputs.append(0)
        self.addedInputs[x] = np.sum(np.dot(i, w))

    def sigmoid(self, x):
        return 1.0 / (1.0+ np.exp(-x))

    def output(self):
        return self.addedInputs

class outputLayer():

    addedInputs = []

    def __init__(self, i):
        for x in range(len(i)):
            self.addInputWeights(i[x], x)
            self.addedInputs[x] = self.sigmoid(self.addedInputs[x])

    def addInputWeights(self, i, x):
        if len(self.addedInputs) <= x:
            self.addedInputs.append(0)
        self.addedInputs[x] = np.sum(i)

    def sigmoid(self, x):
        return 1.0 / (1.0+ np.exp(-x))

    def output(self):
        return self.addedInputs




main()