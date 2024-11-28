import os

from src.QuineMcCluskey import QuineMcCluskey

from src.GeneticAlgorithm import GeneticAlgorithm, VectorizedGeneticAlgorithm
from src.KnuthX import KnuthX

from datetime import datetime

class Manager: # intergrate QuineMcCluskey, GeneticAlgorithm, KnuthX
    def __init__(self, algorithm = "genetic_algorithm", parameters = None):
        """Constructor of Manager class to initialize the algorithm

        Args:
            algorithm (str, optional): algorithm to use. Defaults to "genetic_algorithm".
            parameters (dict, optional): genetic algorithm parameters. Defaults to None.
        """
        self.output_directory = self.__create_output_directory()

        # initialize the algorithm
        if algorithm == "genetic_algorithm":
            if parameters is None:
                raise ValueError("Genetic Algorithm requires parameters")
            self.algorithm = GeneticAlgorithm(parameters)
        elif algorithm == "vectorized_genetic_algorithm":
            if parameters is None:
                raise ValueError("Genetic Algorithm requires parameters")
            self.algorithm = VectorizedGeneticAlgorithm(parameters)
        elif algorithm == "knuth_x":
            self.algorithm = KnuthX()
        else:
            raise ValueError("Invalid algorithm")
    
    def __create_output_directory(self):
        directory_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_directory = os.path.join("./outputs", directory_name) # location of main.py is the root directory
        os.makedirs(output_directory, exist_ok=True)
        return output_directory

    def process(self, p_minterms, p_dont_cares):
        """Run the Quine-McCluskey algorithm and the selected algorithm(Knuth or Genetic)

        Args:
            p_minterms (list[int]): problem minterms
            p_dont_cares (list[int]): problem dont_cares
        """
        self.__create_output_directory()
        qm = QuineMcCluskey(p_minterms, p_dont_cares, self.output_directory)
        prime_implicants, minterms = qm.process() # get prime implicants and minterms

        # initialize the algorithm with prime implicants and minterms
        self.algorithm.set_prime_implicants(prime_implicants)
        self.algorithm.set_minterms(minterms)

        # run the algorithm
        self.algorithm.process()