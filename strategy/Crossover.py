import random
from abc import ABC, abstractmethod

class CrossoverStrategy(ABC):
    @abstractmethod
    def process(self, parents, gene_size):
        """
        Abstract method to perform crossover on the given parents to generate a child genome.

        Args:
            parents (tuple): A tuple containing two parent genomes.
            gene_size (int): The size of the genome.

        Returns:
            int: The child genome generated by crossover.
        """
        pass


class SinglePoint(CrossoverStrategy):
    def process(self, parents, gene_size):
        # Select a random crossover point.
        random_point = random.randrange(gene_size) 
        # Create a mask at the crossover point.
        mask = (1 << random_point) - 1 
        # Generate the child genome by combining the parent genomes at the crossover point.
        child_genome = (parents[1] & mask) | (parents[0] & ~mask)
        
        return child_genome


class Uniform(CrossoverStrategy):
    def process(self, parents, gene_size):
        genome = 0
        for i in range(gene_size):
            # Randomly select each bit from one of the parents.
            if random.random() < 0.5:
                genome |= (parents[0] & (1 << i))
            else:
                genome |= (parents[1] & (1 << i))
        return genome