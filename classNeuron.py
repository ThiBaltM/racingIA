import math
import random
import json

class NeuralNetwork:
    def __init__(self, input_size=None, hidden1_size=None, hidden2_size=None, output_size=None, data=None, data2=None):
        noMutateRate = 0.990
        if(data2==None and data==None):
            self.input_size = input_size
            self.hidden1_size = hidden1_size
            self.hidden2_size = hidden2_size
            self.output_size = output_size
            self.weights1 = [[random.random()*random.choice([1,-1]) for _ in range(input_size)] for _ in range(hidden1_size)]
            self.weights2 = [[random.random()*random.choice([1,-1]) for _ in range(hidden1_size)] for _ in range(hidden2_size)]
            self.weights3 = [[random.random()*random.choice([1,-1]) for _ in range(hidden2_size)] for _ in range(output_size)]
            self.bias1 = [(random.random()*random.choice([1,-1])) for _ in range(hidden1_size)]
            self.bias2 = [(random.random()*random.choice([0.5,-0.5])) for _ in range(hidden2_size)]
            self.bias3 = [(random.random()*random.choice([0.1,-0.1])) for _ in range(output_size)]
        elif data2==None:
            parent1 = json.loads(data)

            self.input_size = parent1["input_size"]
            self.hidden1_size = parent1["hidden1_size"]
            self.hidden2_size = parent1["hidden2_size"]
            self.output_size = parent1["output_size"]
            self.weights1 = parent1["weights1"]
            self.weights2 = parent1["weights2"]
            self.weights3 = parent1["weights3"]
            self.bias1 = parent1["bias1"]
            self.bias2 = parent1["bias2"]
            self.bias3 = parent1["bias3"]
        else:
            parent1 = json.loads(data)
            parent2 = json.loads(data2)
            self.input_size = parent1["input_size"]
            self.hidden1_size = parent1["hidden1_size"]
            self.hidden2_size = parent1["hidden2_size"]
            self.output_size = parent1["output_size"]
            self.weights1 = []
            for k in range(len(parent1["weights1"])):
                self.weights1.append([])
                for i in range(len(parent1["weights1"][0])):
                    w1 = parent1["weights1"][k][i]
                    w2 = parent2["weights1"][k][i]
                    if(random.random()<noMutateRate):
                        self.weights1[k].append(random.uniform(w1,w2))
                    else:

                        self.weights1[k].append(random.random())

            self.weights2 = []
            for k in range(len(parent1["weights2"])):
                self.weights2.append([])
                for i in range(len(parent1["weights2"][0])):
                    w1 = parent1["weights2"][k][i]
                    w2 = parent2["weights2"][k][i]
                    if(random.random()<noMutateRate):
                        self.weights2[k].append(random.uniform(w1,w2))
                    else:
                        self.weights2[k].append(random.random())

            self.weights3 = []
            for k in range(len(parent1["weights3"])):
                self.weights3.append([])
                for i in range(len(parent1["weights3"][0])):
                    w1 = parent1["weights3"][k][i]
                    w2 = parent2["weights3"][k][i]
                    if(random.random()<noMutateRate):
                        self.weights3[k].append(random.uniform(w1,w2))
                    else:
                        self.weights3[k].append(random.random())

            self.bias1 = []
            for k in range(len(parent1["bias1"])):
                b1 = parent1["bias1"][k]
                b2 = parent2["bias1"][k]
                if(random.random()<noMutateRate):
                    self.bias1.append(random.uniform(b1,b2))
                else:
                    self.bias1.append(random.random())

            self.bias2 = []
            for k in range(len(parent1["bias2"])):
                b1 = parent1["bias2"][k]
                b2 = parent2["bias2"][k]
                if(random.random()<noMutateRate):
                    self.bias2.append(random.uniform(b1,b2))
                else:
                    self.bias2.append(random.random())

            self.bias3 = []
            for k in range(len(parent1["bias3"])):
                b1 = parent1["bias3"][k]
                b2 = parent2["bias3"][k]
                if(random.random()<noMutateRate):
                    self.bias3.append(random.uniform(b1,b2))
                else:
                    self.bias3.append(random.random())

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def printTab(self, tab):
        v = []
        for val in tab:
            v.append(math.floor(val*1000)/1000)

    def calcVal(self, tabInput, tabW, bias, outputLength):
        res = []
        for k in range(outputLength):
            v = bias[k]
            for i in range(len(tabInput)-1):
                v += tabInput[i] * tabW[k][i]
            res.append(v)
        return res

    def forward(self, X):
        z = self.calcVal(X, self.weights1, self.bias1, self.hidden1_size)
        z2 = [self.sigmoid(z[j]) for j in range(self.hidden1_size)]
        z3 = self.calcVal(z2, self.weights2, self.bias2, self.hidden2_size)
        z4 = [self.sigmoid(z3[j]) for j in range(self.hidden2_size)]
        z5 = self.calcVal(z4, self.weights3, self.bias3, self.output_size)
        o = [self.sigmoid(z5[j]) for j in range(self.output_size)]
        return o

    def export(self):
        data = {
            'input_size': self.input_size,
            'hidden1_size': self.hidden1_size,
            'hidden2_size': self.hidden2_size,
            'output_size': self.output_size,
            'weights1': self.weights1,
            'weights2': self.weights2,
            'weights3': self.weights3,
            'bias1': self.bias1,
            'bias2': self.bias2,
            'bias3': self.bias3
        }
        return json.dumps(data)