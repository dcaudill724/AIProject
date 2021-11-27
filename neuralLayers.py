import numpy as np


def main():
    a = inputLayer([0.4, 0.5, 0.6, 0.7, 0.8])
    b = hiddenLayer(a.output(), [[0.1, 0.2, 0.3, 0.9, 0.6], [0.4, 0.1, 0.9, 0.9, 0.5], [0.9, 0.4, 0.6, 0.9, 0.4], [0.1, 0.9, 0.8, 0.7, 0.6]])
    c = outputLayer(b.output(), [[0.4, 0.9, 0.3, 0.1,], [0.8, 0.1, 0.2, 0.1,], [0.8, 0.6, 0.2, 0.5,]])
    print(c.output())

# Takes a matrix of size 5 x 1
class inputLayer():
    def __init__(self, i):
        self.tmp = []
        for x in i:
            self.tmp.append(self.sigmoid(x))
        self.inputs = []
        for i in range(4):
            self.inputs.append(self.tmp)

    def sigmoid(self, x):
        return 1.0 / (1.0+ np.exp(-x))

    def output(self):
        return self.inputs


# Takes a matrix of size 5 x 4
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

    def addInputWeights(self, i, w, x):
        if len(self.addedInputs) <= x:
            self.addedInputs.append(0)
        for c in range(len(w)):
            self.addedInputs[x] += (i[c] * w[c])

    def sigmoid(self, x):
        return 1.0 / (1.0+ np.exp(-x))

    def output(self):
        tmp = []
        for i in range(3):
            tmp.append(self.addedInputs)
        return tmp

# Takes a matrix of size 4 x 3
class outputLayer():
    addedInputs = []

    def __init__(self, i, w):
        for x in range(len(i)):
            self.addInputWeights(i[x], w[x], x)
        
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


main()