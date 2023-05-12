import math
import random

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights1 = [[random.random() for _ in range(input_size)] for _ in range(hidden_size)]
        self.weights2 = [[random.random() for _ in range(hidden_size)] for _ in range(output_size)]
        self.bias1 = [random.random()*2-1 for _ in range(hidden_size)]
        self.bias2 = [random.random()*2-1 for _ in range(output_size)]

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def printTab(self,tab):
        v = [];
        for val in tab:
            v.append(math.floor(val*1000)/1000)
        print(v)

    def calcVal(self,tabInput, tabW, bias, outputLenght):
        res = [];
        for k in range(outputLenght):
            v = bias[k];
            for i in range(len(tabInput)-1):
                v += tabInput[i] * tabW[k][i];
            res.append(v);
        return res



    def forward(self, X):
        self.printTab(X)
        z = self.calcVal(X, self.weights1, self.bias1, self.hidden_size);
        self.printTab(z)
        # Apply the sigmoid activation function to the result
        z2 = [self.sigmoid(z[j]) for j in range(self.hidden_size)]
        self.printTab(z2)
        # Compute the dot product of the resulting hidden layer and the second set of weights, and add the bias term
        z3 = self.calcVal(z2, self.weights2, self.bias2, self.output_size)
        self.printTab(z3)
        # Apply the sigmoid activation function again to obtain the final output
        o = [self.sigmoid(z3[j]) for j in range(self.output_size)]
        self.printTab(o)
        print()
        return o

