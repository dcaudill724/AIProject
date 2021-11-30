import numpy as np
from numpy.lib.shape_base import split
from neuralLayers import *

class NeuralNetwork():

    def __init__(self, i, w):
        self.seperateWeights(w)
        self.nextInputs(i)
        
    def nextInputs(self, i):
        self.iLayer = inputLayer(i)
        self.hLayer = hiddenLayer(self.iLayer.output(), self.hWeights)
        self.oLayer = outputLayer(self.hLayer.output(), self.oWeights)

    def seperateWeights(self, w):
        self.hWeights = w[0:20]
        self.oWeights = w[21:28]
    
    def output(self):
        return self.oLayer.output()

    