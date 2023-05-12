import math
import random

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights1 = [[random.random() for _ in range(hidden_size)] for _ in range(input_size)]
        self.weights2 = [[random.random() for _ in range(output_size)] for _ in range(hidden_size)]
        self.bias1 = [random.random() for _ in range(hidden_size)]
        self.bias2 = [random.random() for _ in range(output_size)]

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def forward(self, X):
        # Compute the dot product of the input and the first set of weights, and add the bias term
        z = [sum(map(lambda x, w: x*w, X, self.weights1[j])) + self.bias1[j] for j in range(self.hidden_size)]
        print(z)
        # Apply the sigmoid activation function to the result
        z2 = [self.sigmoid(z[j]) for j in range(self.hidden_size)]
        # Compute the dot product of the resulting hidden layer and the second set of weights, and add the bias term
        z3 = [sum(map(lambda x, w: x*w, z2, self.weights2[j])) + self.bias2[j] for j in range(self.output_size)]
        # Apply the sigmoid activation function again to obtain the final output
        o = [self.sigmoid(z3[j]) for j in range(self.output_size)]
        return o

