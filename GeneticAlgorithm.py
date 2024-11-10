import math
import random
from rich.table import Table

from Visualization import HitmapPlot, FitnessPlot
from Utils import integer_to_binary, console

# 평가할때 돈캐어는 처리하면 안된다.
class GeneticAlgorithm:
    def __init__(self, prime_implicants, minterms, crossover_strategy, population_size,
                 epoch, weight, mutation_rate, parent_population_size, selection_strategy, bit_mutation_rate):
        self.prime_implicants = prime_implicants
        self.minterms = minterms
        self.gene_size = len(self.prime_implicants)
        self.population_size = population_size
        self.best_solution = (0, -math.inf, -math.inf, math.inf, -1) # 유전자, 적합도, 커버한 민텀, 사용한 주항, epoch
        self.epoch = epoch
        self.weight = weight
        self.mutation_rate = mutation_rate
        self.crossover_strategy = crossover_strategy
        self.parent_population_size = parent_population_size
        self.selection_strategy = selection_strategy
        self.bit_mutation_rate = bit_mutation_rate

    def __init_population(self):
        bit_limit = 1 << self.gene_size  # 2 ** self.gene_size
        return random.sample(range(bit_limit), self.population_size)

    def __mutation(self, genome):
        if random.random() < self.mutation_rate:
            for i in range(self.gene_size):
                if random.random() < self.bit_mutation_rate:
                    genome ^= (1 << i)  # i번째 비트를 뒤집음
        return genome

    def __crossover(self, parents):
        return self.crossover_strategy.process(parents, self.gene_size)

    def __selection(self, genomes):
        return self.selection_strategy.process(self.parent_population_size, genomes)

    def __select_next_genomes(self, genomes):
        parent_genomes = self.__selection(genomes)
        next_genomes = []
        for _ in range(self.population_size):
            random_number1 = random.randrange(self.parent_population_size)
            random_number2 = random.randrange(self.parent_population_size)
            next_genomes.append(
                self.__mutation(self.__crossover((parent_genomes[random_number1], parent_genomes[random_number2]))))
        return next_genomes

    # 모든 민텀을 커버하면서 가장 적은 민텀을 가지는 것이 가장 중요하다.
    def evaluate_fitness(self, genomes, epoch):
        genomes_with_fitness = []  # 각 유전자의 적합도와 함께 저장
        min_genome = [math.inf, None]
        max_genome = [-math.inf, None]
        total_fitness = 0
        for genome in genomes:
            used_prime_implicant = genome.bit_count()
            cover_set = set()

            for i in range(self.gene_size):
                if (genome >> i) & 1:
                    for covered_minterm in self.prime_implicants[self.gene_size - 1 - i]:
                        # 검색 시간 느림(list)
                        if covered_minterm in self.minterms:
                            cover_set.add(covered_minterm)
            fitness = self.weight * len(cover_set) + len(self.prime_implicants) - used_prime_implicant
            #fitness = (len(cover_set) * weight ) * ( len(self.prime_implicants) - used_prime_implicant)
            total_fitness += fitness

            if fitness < min_genome[0]:
                min_genome = [fitness, genome]

            if fitness > max_genome[0]:
                max_genome = [fitness, genome]

            if fitness > self.best_solution[1]:
                self.best_solution = (genome, fitness, len(cover_set), used_prime_implicant, epoch)
            genomes_with_fitness.append((fitness, genome))
        return (total_fitness, min_genome, max_genome, genomes_with_fitness)

    def __binary_gene_to_list(self, gene):
        ret = [0 for _ in range(self.gene_size)]
        for i in range(self.gene_size):
            if (gene >> i) & 1:
                ret[self.gene_size - 1 - i] = 1
        return ret


    def __generate_mintom_cover_list(self, gene):
        minterm_to_idx = dict()
        for i, idx in enumerate(self.minterms):
            minterm_to_idx[idx] = i
        ret = [0 for _ in range(len(self.minterms))]
        for i in range(self.gene_size):
            if (gene >> i) & 1:
                for j in self.prime_implicants[self.gene_size - 1 - i]:
                    if j in minterm_to_idx:
                        ret[minterm_to_idx[j]] += 1
        return ret
    def __render_result(self):
        render_table = Table(title="Genetic Algorithm Result")
        for column in ["Used Prime Implicants", "Number of Used Prime Implicants",
                       "Number of Covered Minterms", "Covered Minterms / Total Minterms", "Epoch"]:
            render_table.add_column(column)
        render_table.add_row(integer_to_binary.process(self.best_solution[0], self.gene_size), str(self.best_solution[3]),
                             str(self.best_solution[2]), str((self.best_solution[2]/len(self.minterms)) * 100) + '%', str(self.best_solution[4]))
        console.print(render_table)
    def process(self):
        fitness_plot = FitnessPlot()
        best_gene_hitmap = HitmapPlot("Best Gene Hitmap(Used Prime Implicants)")
        covered_minterm_hitmap = HitmapPlot("Cover Minterms")

        fitness_plot.init()
        genomes = self.__init_population()
        for epoch in range(self.epoch):
            total_fitness, min_genome, max_genome, child_genomes = self.evaluate_fitness(genomes, epoch)
            fitness_plot.update(epoch, total_fitness / self.population_size, max_genome[0], min_genome[0])
            best_gene_hitmap.append(self.__binary_gene_to_list(max_genome[1]))
            covered_minterm_hitmap.append(self.__generate_mintom_cover_list(max_genome[1]))
            genomes = self.__select_next_genomes(child_genomes)
        self.__render_result()
        fitness_plot.finalize()
        covered_minterm_hitmap.show('Greys', has_colorbar=True, has_min_limit=True)
        best_gene_hitmap.show('Blues')