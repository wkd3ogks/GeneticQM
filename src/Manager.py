import os, json, time
from datetime import datetime

from src.QuineMcCluskey import QuineMcCluskey
from src.GeneticAlgorithm import GeneticAlgorithm, VectorizedGeneticAlgorithm
from src.KnuthX import KnuthX

import tkinter as tk
from tkinter import filedialog, OptionMenu, Scrollbar, Listbox


class Manager(tk.Tk): # intergrate QuineMcCluskey, GeneticAlgorithm, KnuthX
    def __init__(self):
        """Constructor of Manager class to initialize the algorithm

        Args:
            algorithm (str, optional): algorithm to use. Defaults to "genetic_algorithm".
            parameters (dict, optional): genetic algorithm parameters. Defaults to None.
        """

        # initialize the GUI
        super().__init__()
        self.title("Genetic Quine-McCluskey")
        self.__create_widgets()

        # # initialize the algorithm
        # if algorithm_name == "genetic_algorithm":
        #     if parameters is None:
        #         raise ValueError("Genetic Algorithm requires parameters")
        #     self.algorithm = GeneticAlgorithm(parameters)
        # elif algorithm_name == "vectorized_genetic_algorithm":
        #     if parameters is None:
        #         raise ValueError("Genetic Algorithm requires parameters")
        #     self.algorithm = VectorizedGeneticAlgorithm(parameters)
        # elif algorithm_name == "knuth_x":
        #     self.algorithm = KnuthX()
        # else:
        #     raise ValueError("Invalid algorithm")

    def __create_widgets(self):
        self.label = tk.Label(self, text="Testcase File:", pady=5)
        self.label.grid(row=0, sticky="e")

        self.testcase_entry = tk.Entry(self)
        self.testcase_entry.grid(row=0, column=1, sticky="we")

        self.browse_button = tk.Button(self, text="Browse", command=self.__browse_file)
        self.browse_button.grid(row=0, column=2, sticky="e")

        choices = ["Genetic Algorithm", "Vectorized Genetic Algorithm", "Knuth X"]
        self.algorithm_label = tk.Label(self, text="Algorithm:")
        self.algorithm_label.grid(row=1, sticky="e", pady=5)
        self.default_algorithm = tk.StringVar()
        self.default_algorithm.set(choices[0])
        self.algorithm_option = OptionMenu(self, self.default_algorithm, *choices)
        self.algorithm_option.grid(row=1, column=1, sticky="w")

        self.scroll = Scrollbar(self, orient='horizontal')
        self.log = Listbox(self, xscrollcommand=self.scroll.set)
        self.scroll.config(command=self.log.yview)
        self.log.grid(row=2, columnspan=3, sticky="we")

        self.run_button = tk.Button(self, text="Run", command=self.process)
        self.run_button.grid(row=1, column=2, sticky="e")

        self.__write_log("Application started")
    def __browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.testcase_entry.delete(0, tk.END)
            self.testcase_entry.insert(0, file_path)
    def __write_log(self, message):
        self.log.insert(tk.END, f"[{datetime.now().strftime("%H:%M:%S")}] {message}")
        self.log.update()
        self.log.see(tk.END)
    def __create_output_directory(self):
        """Create a directory to store the output files

        Returns:
            str: path of the created directory
        """
        directory_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_directory = os.path.join("./outputs", directory_name) # location of main.py is the root directory
        os.makedirs(output_directory, exist_ok=True)
        return output_directory

    def __plot_hitmap(self, data, title="Hitmap Plot", has_colorbar=False):
        pass

    def process(self):
        """Run the Quine-McCluskey algorithm and the selected algorithm(Knuth or Genetic)

        Args:
            p_minterms (list[int]): problem minterms
            p_dont_cares (list[int]): problem dont_cares
        """

        with open(self.testcase_entry.get(), 'r') as json_file:
            testcase = json.load(json_file)
            self.__write_log(f"Testcase loaded")
            self.output_directory = self.__create_output_directory()
            self.__write_log(f"Output directory created{self.output_directory}")
            qm = QuineMcCluskey(testcase["minterms"], testcase["dontcares"], self.output_directory)
            prime_implicants, minterms = qm.process() # get prime implicants and minterms
            self.__write_log("Quine-McCluskey process completed")

            # initialize the algorithm
            self.algorithm = GeneticAlgorithm(testcase["parameters"])
            self.algorithm.set_prime_implicants(prime_implicants)
            self.algorithm.set_minterms(minterms)

            # run the algorithm
            start_time = time.time()
            self.algorithm.process()
            end_time = time.time() 
            self.__write_log("Algorithm process completed")
            self.__write_log(f"Excution Time: {end_time - start_time:.2f} seconds")

        # save the visualization results