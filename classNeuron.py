import math
import random
import json

class NeuralNetwork:
    def __init__(self, input_size=None, hidden_size=None,output_size=None, data=None, data2=None):
        if(data2==None and data==None):
            self.input_size = input_size
            self.hidden_size = hidden_size
            self.output_size = output_size
            self.weights1 = [[random.random() for _ in range(input_size)] for _ in range(hidden_size)]
            self.weights2 = [[random.random() for _ in range(hidden_size)] for _ in range(output_size)]
            self.bias1 = [random.random()*2-1 for _ in range(hidden_size)]
            self.bias2 = [random.random()*2-1 for _ in range(output_size)]
        elif data2==None:
            parent1 = json.dumps(data)

            self.input_size = parent1["input_size"]
            self.hidden_size = parent1["hidden_size"]
            self.output_size = parent1["output_size"]
            self.weights1 = parent1["weights1"];
            self.weights2 = parent1["weights2"]
            self.bias1 = parent1["bias1"]
            self.bias2 = parent1["bias2"]

        else:
            parent1 = json.dumps(data)
            parent2 = json.dumps(data2)
            print(parent1)
            self.input_size = parent1["input_size"]
            self.hidden_size = parent1["hidden_size"]
            self.output_size = parent1["output_size"]
            self.weights1 = [];
            for w1, w2 in parent1["weights1"], parent2["weights1"]:
                if(random.random()<0.999):
                    self.weights1.append(random.uniform(w1,w2))
                else:
                    print("mutation")
                    self.weights1.append(random.random())
            
            self.weights2 = [];
            for w1, w2 in parent1["weights2"], parent2["weights2"]:
                if(random.random()<0.999):
                    self.weights2.append(random.uniform(w1,w2))
                else:
                    print("mutation")
                    self.weights2.append(random.random())

            self.bias1 = [];
            for b1, b2 in parent1["bias1"], parent2["bias1"]:
                if(random.random()<0.999):
                    self.bias1.append(random.uniform(b1,b2))
                else:
                    print("mutation")
                    self.bias1.append(random.random())
            
            self.bias2 = [];
            for b1, b2 in parent1["bias2"], parent2["bias2"]:
                if(random.random()<0.999):
                    self.bias2.append(random.uniform(b1,b2))
                else:
                    print("mutation")
                    self.bias2.append(random.random())

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def printTab(self,tab):
        v = [];
        for val in tab:
            v.append(math.floor(val*1000)/1000)

    def calcVal(self,tabInput, tabW, bias, outputLenght):
        res = [];
        for k in range(outputLenght):
            v = bias[k];
            for i in range(len(tabInput)-1):
                v += tabInput[i] * tabW[k][i];
            res.append(v);
        return res



    def forward(self, X):

        z = self.calcVal(X, self.weights1, self.bias1, self.hidden_size);

        # Apply the sigmoid activation function to the result
        z2 = [self.sigmoid(z[j]) for j in range(self.hidden_size)]

        # Compute the dot product of the resulting hidden layer and the second set of weights, and add the bias term
        z3 = self.calcVal(z2, self.weights2, self.bias2, self.output_size)

        # Apply the sigmoid activation function again to obtain the final output
        o = [self.sigmoid(z3[j]) for j in range(self.output_size)]

        return o

    def export(self):
        data={
            'input_size':self.input_size,
            'hidden_size':self.hidden_size,
            'output_size':self.output_size,
            'weights1':self.weights1,
            'weights2':self.weights2,
            'bias1':self.bias1, 
            'bias2':self.bias2
        };
        return json.dumps(data);
