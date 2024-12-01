""" 
Genetic Algorithm
    1. Initialize the population with random genomes. [ __init_population method ]
    2. Evaluate the fitness of each genome. [ evaluate_fitness method ]
    3. Select the parents based on the fitness. [ __selection method ]
    4. Generate the next generation by crossover(mixing the genes of the parents) [ __crossover method ] 
    5. Mutate the genes of the next generation. [ __mutation method ]
    6. Replace the current generation with the next generation. [ __select_next_genomes method ]
    7. Repeat steps 2-6 until maximum epoch is reached.
"""

import math, random

from src.strategy.Crossover import Uniform
from src.strategy.Selection import RouletteWheel

class GeneticAlgorithm:
    def __init__(self, parameters):
        self.prime_implicants = None
        self.minterms = None

        # paramerter dictionary unpacking
        self.population_size = int(parameters["population_size"])
        self.epoch = int(parameters["epoch"])
        self.weight = int(parameters["weight"])
        self.mutation_rate = float(parameters["mutation_rate"])
        self.parent_population_size = int(parameters["parent_population_size"])
        self.bit_mutation_rate = float(parameters["bit_mutation_rate"])

        self.crossover_strategy = Uniform()
        self.selection_strategy = RouletteWheel(self.population_size)
        self.best_solution = (0, -math.inf, -math.inf, math.inf, -1) # 유전자, 적합도, 커버한 민텀, 사용한 주항, epoch

        # data for visualization
        self.fitness_data = {'average': [], 'max': [], 'min': []}
        self.max_genomes = []
    
    def set_minterms(self, minterms):
        self.minterms = minterms

    def set_prime_implicants(self, prime_implicants):
        self.prime_implicants = prime_implicants
        self.gene_size = len(self.prime_implicants) # number of prime implicants

    def __init_population(self):
        """
        Initialize the population with random genomes.

        Returns:
            list[int]: list of random genomes
        """
        bit_limit = 1 << self.gene_size  # 2 ** self.gene_size
        random_genomes = []
        for _ in range(self.population_size): # select random genome from 0 to 2 ** self.gene_size - 1
            random_genomes.append(random.randrange(bit_limit))
        return random_genomes

    def __mutation(self, genome):
        if random.random() < self.mutation_rate:
            for i in range(self.gene_size):
                if random.random() < self.bit_mutation_rate:
                    genome ^= (1 << i)  # flip i-th bit
        return genome

    def __crossover(self, parents):
        return self.crossover_strategy.process(parents, self.gene_size)

    def __selection(self, genomes):
        return self.selection_strategy.process(self.parent_population_size, genomes)

    def __generate_next_genomes(self, genomes):
        """
        Generate the next genomes by selection, crossover and mutation.

        Args:
            genomes (list[(int, int)]): list of genomes with fitness (fitness, genome)

        Returns:
            list[int]: next generation list of genomes
        """
        parent_genomes = self.__selection(genomes)
        next_genomes = []
        for _ in range(self.population_size):
            random_number1 = random.randrange(self.parent_population_size)
            random_number2 = random.randrange(self.parent_population_size)
            next_genomes.append(
                self.__mutation(self.__crossover((parent_genomes[random_number1], parent_genomes[random_number2]))))
        return next_genomes

    def __evaluate_fitness(self, genomes, epoch):
        """
        fitness function:
            weight * number of covered minterms + total_prime_implicants - number of used prime implicants

        Args:
            genomes (list[int]): list of genomes
            epoch (int): current epoch

        Returns:
            (int, int, int, list[(int, int)]): result of the evaluation ( total_fitness, min_genome, max_genome, genomes_with_fitness) )
        """
        genomes_with_fitness = []  # list of (evaluated fitness, genome)

        # initialize min_genome, max_genome, total_fitness
        min_genome = [math.inf, None]
        max_genome = [-math.inf, None]
        total_fitness = 0

        # using set for faster search
        minterms = set(self.minterms)

        for genome in genomes:
            used_prime_implicant = genome.bit_count()
            cover_set = set() # len(cover_set):  number of covered minterms

            # find covered minterms
            for i in range(self.gene_size): # i: index of prime implicant
                if (genome >> i) & 1: # check back to front(gene_size - 1 to 0-th bit)
                    for covered_minterm in self.prime_implicants[self.gene_size - 1 - i]:
                        if covered_minterm in minterms:
                            cover_set.add(covered_minterm)
            # evaluate fitness
            covered_minterms, total_prime_implicants = len(cover_set), len(self.prime_implicants)
            fitness = self.weight * covered_minterms  + total_prime_implicants - used_prime_implicant
            total_fitness += fitness

            # update min_genome, max_genome and best_solution
            if fitness < min_genome[0]:
                min_genome = [fitness, genome]
            if fitness > max_genome[0]:
                max_genome = [fitness, genome]
            if fitness > self.best_solution[1]:
                self.best_solution = (genome, fitness, len(cover_set), used_prime_implicant, epoch)

            genomes_with_fitness.append((fitness, genome))
        return (total_fitness, min_genome, max_genome, genomes_with_fitness)
    
    def process(self):
        genomes = self.__init_population()
        for epoch in range(self.epoch):
            total_fitness, min_genome, max_genome, genomes_with_fitness = self.__evaluate_fitness(genomes, epoch)

            # set fitness data
            self.fitness_data['average'].append(total_fitness / self.population_size)
            self.fitness_data['max'].append(max_genome[0])
            self.fitness_data['min'].append(min_genome[0])
            
            # set hitmap data
            self.max_genomes.append(max_genome[1])

            genomes = self.__generate_next_genomes(genomes_with_fitness)

        visualization_params = {'gene_size': self.gene_size,
                                'minterms': self.minterms,
                                'prime_implicants': self.prime_implicants}
        return self.fitness_data, self.max_genomes, self.best_solution, visualization_params