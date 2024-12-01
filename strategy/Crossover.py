import random
from abc import ABC, abstractmethod

class CrossoverStrategy(ABC):
    @abstractmethod
    def process(self, parents, gene_size):
        pass


class SinglePoint(CrossoverStrategy):
    def process(self, parents, gene_size):
        random_point = random.randrange(gene_size)
        mask = (1 << random_point) - 1
        child_genome = (parents[1] & mask) | (parents[0] & ~mask)
        return child_genome


class Uniform(CrossoverStrategy):
    def process(self, parents, gene_size):
        genome = 0
        for i in range(gene_size):
            if random.random() < 0.5:
                genome |= (parents[0] & (1 << i))
            else:
                genome |= (parents[1] & (1 << i))
        return genome