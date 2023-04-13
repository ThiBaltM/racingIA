import random
import math
from classGame import Game;

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights1 = self.initialize_weights(input_size, hidden_size)
        self.bias1 = self.initialize_weights(1, hidden_size)
        self.weights2 = self.initialize_weights(hidden_size, output_size)
        self.bias2 = self.initialize_weights(1, output_size)
    
    def initialize_weights(self, input_size, output_size):
        weights = []
        for i in range(input_size):
            row = []
            for j in range(output_size):
                row.append(random.uniform(-1, 1))
            weights.append(row)
        return weights
    
    def forward(self, input):
        hidden = self.sigmoid(self.dot_product(input, self.weights1) + self.bias1)
        output = self.sigmoid(self.dot_product(hidden, self.weights2) + self.bias2)
        return output
    
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def dot_product(self, x, y):
        result = []
        for i in range(len(y[0])):
            row = []
            for j in range(len(x)):
                row.append(x[j] * y[j][i])
            result.append(sum(row))
        return result
    
    def train(self, data, population_size, num_generations):
        population = []
        for i in range(population_size):
            network = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
            population.append(network)
        
        for  generation in range(num_generations):
            fitness_scores = []

            sorted_population = Game(population);
            elite = sorted_population[0]
            new_population = [elite]
            
            while len(new_population) < population_size:
                parent1 = self.select_parent(sorted_population)
                parent2 = self.select_parent(sorted_population)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            population = new_population
        
        return elite
    
    def evaluate_fitness(self, network, data):
        error = 0
        for input, target in data:
            output = network.forward(input)
            error += (target[0] - output[0]) ** 2
        return -error
    
    def select_parent(self, population):
        total_fitness = sum([self.evaluate_fitness(x, data) for x in population])
        r = random.uniform(0, total_fitness)
        running_sum = 0
        for network in population:
            running_sum += self.evaluate_fitness(network, data)
            if running_sum > r:
                return network
    
    def crossover(self, parent1, parent2):
        child = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        child.weights1 = self.combine_arrays(parent1.weights1, parent2.weights1)
        child.bias1 = self.combine_arrays(parent1.bias1, parent2.bias1)
        child.weights2 = self.combine_arrays(parent1.weights2, parent2.weights2)
        child.bias2 = self.combine_arrays(parent1.bias2, parent2.bias2)
        return child
    
    def combine_arrays(self, array1, array2):
        combined_array = []
        for i in range(len(array1)):
            row = []
            for j in range(len(array1[0])):
                if random.random() < 0.5:
                    row.append(array1[i][j])
                else:
                    row.append(array2[i][j])
            combined_array.append(row)
        return combined_array

    def mutate(self, network):
        mutated_network = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        mutated_network.weights1 = self.mutate_array(network.weights1)
        mutated_network.bias1 = self.mutate_array(network.bias1)
        mutated_network.weights2 = self.mutate_array(network.weights2)
        mutated_network.bias2 = self.mutate_array(network.bias2)
        return mutated_network

    def mutate_array(self, array):
        mutated_array = []
        for i in range(len(array)):
            row = []
            for j in range(len(array[0])):
                if random.random() < 0.1:
                    row.append(random.uniform(-1, 1))
                else:
                    row.append(array[i][j])
            mutated_array.append(row)
        return mutated_array