import numpy as np


class ActivationSigmoid:
    def forward(self, inputs):
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                inputs[i, j] = self.sigmoid(inputs[i, j])
        self.output = inputs
         
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
            
        

class ActivationReLU:
    def forward(self, inputs):
        # print(inputs, "->", end="")
        self.output = np.maximum(0, inputs)
        # print(self.output)
        
class ActivationSoftmax:
    def forward(self, inputs):
        expValues = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = expValues / np.sum(expValues, axis=1, keepdims=True)
        self.output = probabilities