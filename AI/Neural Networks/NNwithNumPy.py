# ****************** Tom Rietjens ******************************************
# implementing a fully connected neural netwoerk from scratch in python using NumPy
# this code is yet to be debugged and can be optimised. it was made just for learning purposes

import numpy as np
from Activations import *
from copy import deepcopy
# np.random.seed(0)


class NeuralNetworkDense:
    # initalise network like this NeuralNetworkDense(2,4,5,2) where the arguments are however many nodes you wany per layer.
    def __init__(self, *args) -> None:
        self.layers = []
        self.activations = []
        for i in range(len(args)-1):
            self.layers.append(LayerDense(args[i], args[i+1]))
            if i+2 == len(args):
                if args[i+1] == 1:
                    self.activations.append(ActivationReLU())
                else:
                    self.activations.append(ActivationSoftmax())
            else:
                self.activations.append(ActivationReLU())
                
    def forward(self, NextLayerInputs):
        for layer, activation in zip(self.layers, self.activations):
            layer.forward(NextLayerInputs)
            activation.forward(layer.output)
            NextLayerInputs = activation.output
        self.output = NextLayerInputs
            
            
class LayerDense:
    def __init__(self, nInputs, nNeurons) -> None:
        self.weights = 1 * np.random.randn(nInputs, nNeurons)
        self.biases = np.random.rand(1, nNeurons)
        
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
        
        
        
class NeuralNetworkGentic(NeuralNetworkDense):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.fitness = 0
      
    @staticmethod    
    def crossover(ParentA, ParentB):
        allWeightsA = np.array(NeuralNetworkGentic.getAllWeights(ParentA))
        print(allWeightsA)
        print(np.shape(allWeightsA))
        # unfinished
        
    @staticmethod
    def getAllWeights(nn):
        weights = []
        for layer in nn.layers:
            weights.append(layer.weights)
        return weights
            
        
    def mutate(self):
        mutationRate = 0.1
        for layer in self.layers:
            for i in range(len(layer.weights)):
                for j in range(len(layer.weights[i])):
                    if np.random.random() < mutationRate:
                        layer.weights[i, j] += np.random.normal(0, 0.5)
            for i in range(len(layer.biases)):
                if np.random.random() < mutationRate:
                    layer.biases[i] += np.random.normal(0, 0.5)
    
    def copy(self):
        return deepcopy(self)
                        
                        
if __name__ == '__main__':
    # nn = NeuralNetworkGentic(5, 3, 1)
    # nn2 = NeuralNetworkGentic(5, 3, 1)
    # print(NeuralNetworkGentic.crossover(nn, nn2))
    
    inputs = [[0.34, 5.2, 3.1, 4.5],
            [0.45, 2.3, 1.1, 0.01]]    

    d1 = LayerDense(4, 3)
    a1 = ActivationSigmoid()
    # a1 = ActivationReLU()

    # d2 = LayerDense(3, 2)
    # a2 = ActivationSoftmax()

    d1.forward(inputs)
    a1.forward(d1.output)

    # d2.forward(a1.output)
    # a2.forward(d2.output)
    # print(a2.output, "\n\n")

    # nn = NeuralNetworkGentic(2, 2)
    # print(nn.activations)
    # nn.forward(inputs)
    # print(nn.output)
    # nn.mutate()
