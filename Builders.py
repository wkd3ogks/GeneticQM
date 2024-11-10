from abc import ABC, abstractmethod

from GeneticAlgorithm import GeneticAlgorithm

from Crossover import SinglePointCrossover
from Selection import RouletWheelSelection


class Builder(ABC):
    def __init__(self):
        self.prime_implicants = None
        self.minterms = None
    def set_prime_implicants(self, prime_implicants):
        self.prime_implicants = prime_implicants
        return self

    def set_minterms(self, minterms):
        self.minterms = minterms
        return self
    @abstractmethod
    def build(self):
        pass

# population_size 관련 오류가 있음
class GeneticAlgorithmBuilder(Builder):
    def __init__(self):
        super().__init__()
        self.gene_size = None
        self.population_size = 100
        self.epoch = 100
        self.weight = 1
        self.mutation_rate = 0.9
        self.parent_population_size = 50
        self.crossover_strategy = SinglePointCrossover()
        self.selection_strategy = RouletWheelSelection(self.population_size)
        self.bit_mutation_rate = 0.015
    def set_prime_implicants(self, prime_implicants):
        super().set_prime_implicants(prime_implicants)
        self.gene_size = len(self.prime_implicants)
        return self
    def set_population_size(self, population_size):
        self.population_size = population_size
        # Population_size에 영향을 받는다.
        self.parent_population_size = population_size // 2
        self.selection_strategy = RouletWheelSelection(self.population_size)
        return self
    def set_bit_mutation_rate(self, bit_mutation_rate):
        self.bit_mutation_rate = bit_mutation_rate
        return self
    def set_epoch(self, epoch):
        self.epoch = epoch
        return self
    def set_weight(self, weight):
        self.weight = weight
        return self
    def set_mutation_rate(self, mutation_rate):
        self.mutation_rate = mutation_rate
        return self
    def set_parent_population_size(self, parent_population_size):
        self.parent_population_size = parent_population_size
        return self
    def set_crossover_strategy(self, crossover_strategy):
        self.crossover_strategy = crossover_strategy
        return self
    def set_selection_strategy(self, selection_strategy):
        self.selection_strategy = selection_strategy
        return self
    def build(self):
        return GeneticAlgorithm(
            self.prime_implicants,
            self.minterms,
            self.crossover_strategy,
            self.population_size,
            self.epoch,
            self.weight,
            self.mutation_rate,
            self.parent_population_size,
            self.selection_strategy,
            self.bit_mutation_rate
        )