"""
    Selection module contains the selection strategies for selecting parents based on their fitness.
"""

import random
from abc import ABC, abstractmethod

class SelectionStrategy(ABC):
    @abstractmethod
    def process(self, parent_population_size, genomes_with_fitness):
        """
        Abstract method to select parents based on their fitness.

        Args:
            parent_population_size (int): The number of parents to select.
            genomes_with_fitness (list[tuple[int, int]]): A list of tuples containing genomes and their fitness.

        Returns:
            list: A list of selected parent genomes.
        """
        pass

class RouletteWheel(SelectionStrategy):
    def __init__(self, population_size):
        self.population_size = population_size
    def __lower_bound(self, fitness_sum, find):
        """
        Perform binary search to find the lower bound index for the given fitness sum.

        Args:
            fitness_sum (list): A list of cumulative fitness sums. fitness_sum > 0
            find (int): The target fitness value to find.

        Returns:
            int: The index of the lower bound.
        """
        left = 0
        right = self.population_size - 1
        answer = -1
        mid = (left + right) // 2
        while left <= right:
            if fitness_sum[mid] >= find:
                answer = mid
                right = mid - 1
            elif fitness_sum[mid] < find:
                left = mid + 1
            mid = (left + right) // 2
        return answer

    def process(self, parent_population_size, genomes_with_fitness):
        parent_genomes = []
        fitness_sum = []
        total_fitness = 0
        
        # Calculate cumulative fitness sums.
        for genome_with_fitness in genomes_with_fitness:
            if not fitness_sum:
                fitness_sum.append(genome_with_fitness[0])
            else:
                fitness_sum.append(fitness_sum[-1] + genome_with_fitness[0]) # prefix_sum
            total_fitness += genome_with_fitness[0]

        # Select parents based on their fitness.
        for _ in range(parent_population_size):
            random_number = random.randrange(total_fitness + 1)
            genome_idx = self.__lower_bound(fitness_sum, random_number)
            selected_genome = genomes_with_fitness[genome_idx][1]
            parent_genomes.append(selected_genome)
        return parent_genomes