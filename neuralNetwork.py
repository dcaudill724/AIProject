import numpy as np
from neuralLayers import *

class NeuralNetwork():

    def __init__(self, i, w):
        self.inputs = i
        self.weights = w
        
        self.iLayer = inputLayer(self.inputs)
        self.hLayer = hiddenLayer(self.iLayer.output(), self.weights)
        self.oLayer = outputLayer(self.hLayer.output())
    
    def output(self):
        return self.oLayer.output()

    