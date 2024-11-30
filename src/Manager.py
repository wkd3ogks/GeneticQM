import os, json, time
from datetime import datetime

from src.QuineMcCluskey import QuineMcCluskey
from src.GeneticAlgorithm import GeneticAlgorithm
from src.KnuthX import KnuthX

# visualization
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog, OptionMenu, Scrollbar, Listbox


class Manager(tk.Tk): # intergrate QuineMcCluskey, GeneticAlgorithm, KnuthX
    def __init__(self):

        # initialize the GUI
        super().__init__()
        self.title("Genetic Quine-McCluskey")
        self.__create_widgets()

    def __create_widgets(self):
        self.label = tk.Label(self, text="Testcase File:", pady=5)
        self.label.grid(row=0, sticky="e")

        self.testcase_entry = tk.Entry(self)
        self.testcase_entry.grid(row=0, column=1, sticky="we")

        self.browse_button = tk.Button(self, text="Browse", command=self.__browse_file)
        self.browse_button.grid(row=0, column=2, sticky="e")

        choices = ["Genetic Algorithm", "Knuth X"]
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

    def __plot_fitness(self, data, title="Fitness Plot"):
        epoch = len(data['average'])
        plt.plot(range(epoch),data['min'], label='Min Fitness', color='green')
        plt.plot(range(epoch),data['average'], label='Average Fitness', color='blue')
        plt.plot(range(epoch),data['max'], label='Max Fitness', color='orange')

        plt.title(title)
        plt.xlabel("Epoch")
        plt.ylabel("Fitness")
        plt.legend(loc='best', framealpha=0.5)
        plt.savefig(f"{os.path.join(self.output_directory, 'Fitness_Plot.png')}")
        plt.close()

    def __binary_gene_to_list(self, gene, gene_size):
            ret = [0 for _ in range(gene_size)]
            for i in range(gene_size):
                if (gene >> i) & 1:
                    ret[gene_size - 1 - i] = 1
            return ret

    def __generate_minterm_cover_list(self, gene, gene_size, prime_implicants, minterms):
        minterm_to_idx = dict()
        for i, idx in enumerate(minterms):
            minterm_to_idx[idx] = i
        ret = [0 for _ in range(len(minterms))]
        for i in range(gene_size):
            if (gene >> i) & 1:
                for j in prime_implicants[gene_size - 1 - i]:
                    if j in minterm_to_idx:
                        ret[minterm_to_idx[j]] += 1
        return ret

    def __plot_hitmap(self, data, color, title="Hitmap Plot", has_colorbar=False, has_min_limit=False):
        plt.matshow(data, cmap=plt.get_cmap(color))
        plt.title(title)
        if has_colorbar:
            plt.colorbar(shrink=0.8, aspect=10)
        if has_min_limit:
            plt.clim(vmin=0)
        plt.savefig(f"{os.path.join(self.output_directory, title + '.png')}")
        plt.close()

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
            fitness_data, max_genomes, best_solution, visualization_params = self.algorithm.process()
            end_time = time.time() 
            self.__write_log("Algorithm process completed")
            self.__write_log(f"Excution Time: {end_time - start_time:.5f} seconds")

        gene_size = visualization_params['gene_size']
        prime_implicants = visualization_params['prime_implicants']
        minterms = visualization_params['minterms']

        # write the results to log
        best_genome_to_binary = format(best_solution[0], 'b').zfill(gene_size)
        self.__write_log(f"Best Solution: {best_genome_to_binary}")
        self.__write_log(f"Number of Used Prime Implicants: {best_solution[3]}")
        self.__write_log(f"Number of Covered Minterms: {best_solution[2]}")
        self.__write_log(f"Covered Minterms / Total Minterms: {(best_solution[2]/len(minterms)) * 100}%")
        self.__write_log(f"Epoch: {best_solution[4]}")

        # save the visualization results
        self.__plot_fitness(fitness_data)
        best_genome_data = list(map(lambda gene: self.__binary_gene_to_list(gene, gene_size), max_genomes))
        self.__plot_hitmap(best_genome_data, 'Blues', title="Prime_Implicants_Usage_Heatmap")
        best_genome_cover_data = list(map(lambda gene: self.__generate_minterm_cover_list(gene, gene_size, prime_implicants, minterms), max_genomes))
        self.__plot_hitmap(best_genome_cover_data, 'Greys', title="Minterm_Coverage_Hitmap", has_colorbar=True, has_min_limit=True)