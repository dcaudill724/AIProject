import numpy as np
from neuralLayers import *

class NeuralNetwork():

    def __init__(self, i, w):
        
        self.seperateWeights(w)
        self.nextInputs(i)

    def nextInputs(self, i):
        #print(i)
        self.iLayer = inputLayer(i)
        self.hLayer = hiddenLayer(self.iLayer.output(), self.hWeights)
        self.oLayer = outputLayer(self.hLayer.output(), self.oWeights)

    def seperateWeights(self, w):
        self.hWeights = [w[0:5], w[5:10], w[10:15], w[15:20]]
        self.oWeights = [w[20:24], w[24:28]]
    
    def output(self):
        return self.oLayer.output()

    