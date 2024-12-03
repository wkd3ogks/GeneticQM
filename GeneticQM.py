"""
    Main application for running the Genetic, Quine-McCluskey algorithm
"""

import os, json, time
from datetime import datetime

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, Listbox

from QuineMcCluskey import QuineMcCluskey
from GeneticAlgorithm import GeneticAlgorithm


class GeneticQM(tk.Tk):
    def __init__(self):
        super().__init__() # initialize the GUI
        self.title("Genetic Quine-McCluskey")
        self.__create_widgets()

    def __create_widgets(self):
        """
            Create GUI widgets for the application
        """

        # Testcase File Selection
        self.label = tk.Label(self, text="Testcase File:", pady=5)
        self.label.grid(row=0, sticky="e")

        self.testcase_entry = tk.Entry(self)
        self.testcase_entry.grid(row=0, column=1, sticky="we")

        self.browse_button = tk.Button(self, text="Browse", command=self.__browse_file)
        self.browse_button.grid(row=0, column=2, sticky="e")

        # Run Button
        self.run_button = tk.Button(self, text="Run", command=self.process)
        self.run_button.grid(row=0, column=3, sticky="e")

        # Log window
        self.log = Listbox(self)
        self.log.grid(row=1, columnspan=4, sticky="we")

        self.__write_log("Application started")

    def __browse_file(self):
        """
            Open a file dialog to select a testcase file(.json)
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON file", "*.json")])
        if file_path:
            self.testcase_entry.delete(0, tk.END)
            self.testcase_entry.insert(0, file_path)
        
    def __write_log(self, message):
        """
        Write a log message to the log window

        Args:
            message (str): log message
        """
        self.log.insert(tk.END, f"[{datetime.now().strftime("%H:%M:%S")}] {message}")
        self.log.update()
        self.log.see(tk.END)
        
    def __create_output_directory(self):
        """
        Create a directory to store the output files

        Returns:
            str: path of the created directory
        """
        directory_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_directory = os.path.join("./outputs", directory_name) # location of main.py is the root directory
        os.makedirs(output_directory, exist_ok=True)
        return output_directory

    def __plot_fitness(self, data, title="Fitness Plot"):
        """
            Save the fitness plot to the output directory

        Args:
            data (dict[str, num]): fitness data (min, average, max)
            title (str, optional): plot title. Defaults to "Fitness Plot".
        """
        # x-axis: epoch, y-axis: fitness
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

    def __plot_normalized_fitness(self, data, title="Normalized Fitness Plot"):
        epoch = len(data['average'])
        
        # normalize the average fitness data
        max_average, min_average = max(data['average']), min(data['average'])
        normalized_epoch = list(map(lambda x: x / epoch, range(epoch)))
        normalized_fitness_data = list(map(lambda x: (x - min_average) / (max_average - min_average), data['average']))

        # x-axis: epoch, y-axis: normalized fitness
        plt.plot(normalized_epoch, normalized_fitness_data, label='Average Fitness', color='blue')

        plt.title(title)
        plt.xlabel("Epoch")
        plt.ylabel("Fitness")
        plt.legend(loc='best', framealpha=0.5)
        plt.savefig(f"{os.path.join(self.output_directory, 'Normalized_Fitness_Plot.png')}")
        plt.close()

    def __binary_gene_to_list(self, gene, gene_size):
        """
        Convert a binary genome to a list of 0s and 1s for visualization

        Args:
            gene (int): number type genome
            gene_size (int): bit size of the genome

        Returns:
            list[int]: list type genome (0s and 1s)
        """
        ret = [0 for _ in range(gene_size)]
        for i in range(gene_size):
            if (gene >> i) & 1:
                ret[gene_size - 1 - i] = 1
        return ret

    def __generate_minterm_cover_list(self, gene, gene_size, prime_implicants, minterms):
        """
        Generate a list of minterm coverage for the given genome 

        Args:
            gene (int): int type genome
            gene_size (int): bit size of the genome
            prime_implicants (list[tuple[int]]): list of prime implicants(set of minterms)
            minterms (list[int]): list of minterms

        Returns:
            list[int]: list of minterm coverage
        """
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

    def __plot_genetic_diversity(self, data, title="Genetic Diversity Plot"):
        """_summary_

        Args:
            data (list[int]): genetic diversity data(number of unique genomes)
            title (str, optional): plot title. Defaults to "Genetic Diversity Plot".
        """

        # x-axis: epoch, y-axis: genetic diversity
        epoch = len(data)
        plt.plot(range(epoch), data, label='Genetic Diversity', color='purple')

        plt.title(title)
        plt.xlabel("Epoch")
        plt.ylabel("Genetic Diversity")
        plt.savefig(f"{os.path.join(self.output_directory, 'Genetic_Diversity_Plot.png')}")
        plt.close()
    
    def __plot_group_genetic_diversity(self, data, group=10, title="Genetic Diversity(Group) Plot"):
        """
        Plot the genetic diversity for each group of epochs(average of group epochs) 

        Args:
            data (list[int]): genetic diversity data(number of unique genomes)
            group (int, optional): number of epochs in a group. Defaults to 10.
            title (str, optional): plot title. Defaults to "Genetic Diversity(Group) Plot".
        """
        if len(data) % group != 0:
            raise ValueError("Population size % group should be 0")
        
        # x-axis: epoch, y-axis: genetic diversity
        group_size = len(data) // group
        x_data = range(0, len(data) - 1, group_size)
        
        # calculate the average of the group epochs
        group_data = []
        for i in range(0, len(data) - 1, group_size):
            group = sum(data[i:i + group_size]) / group_size
            group_data.append(group)
        
        # plot the group genetic diversity
        plt.plot(x_data, group_data, color='purple')
        plt.title(title)
        plt.xlabel("Epoch")
        plt.ylabel("Genetic Diversity")
        plt.savefig(f"{os.path.join(self.output_directory, 'Genetic_Diversity_Group_Plot.png')}")
        plt.close()

    def __plot_hitmap(self, data, color, title="Hitmap Plot", has_colorbar=False, has_min_limit=False):
        """
        Plot a hitmap for the given data

        Args:
            data (list[int]): hitmap data 
            color (str): color map
            title (str, optional): Plot title. Defaults to "Hitmap Plot".
            has_colorbar (bool, optional): colorbar option. Defaults to False.
            has_min_limit (bool, optional): minimum limit option. Defaults to False.
        """
        plt.matshow(data, cmap=plt.get_cmap(color))
        plt.title(title)
        if has_colorbar:
            plt.colorbar(shrink=0.8, aspect=10)
        if has_min_limit:
            plt.clim(vmin=0)
        plt.savefig(f"{os.path.join(self.output_directory, title + '.png')}")
        plt.close()

    def process(self):
        """
            Run the Quine-McCluskey algorithm and the Genetic Algorithm
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
            self.algorithm = GeneticAlgorithm(testcase["parameters"], testcase["strategy"])

            # run the algorithm
            start_time = time.time()
            fitness_data, max_genomes, best_solution, diversity_data, visualization_params = self.algorithm.process(prime_implicants, minterms)
            end_time = time.time() 
            self.__write_log("Genetic Algorithm process completed")
            self.__write_log(f"Excution Time: {end_time - start_time:.5f} seconds")

        gene_size = visualization_params['gene_size']
        prime_implicants = visualization_params['prime_implicants']
        minterms = visualization_params['minterms']

        # write the results to result.txt
        with open(os.path.join(self.output_directory, "result.txt"), 'w') as f:
            best_genome_to_binary = format(best_solution[0], 'b').zfill(gene_size)
            f.write(f"Best Solution: {best_genome_to_binary}\n")
            f.write(f"Number of Used Prime Implicants: {best_solution[3]}\n")
            f.write(f"Number of Covered Minterms: {best_solution[2]}\n")
            f.write(f"Covered Minterms / Total Minterms: {(best_solution[2]/len(minterms)) * 100}%\n")
            f.write(f"Epoch: {best_solution[4]}\n")

        # save the visualization results
        self.__plot_fitness(fitness_data)
        self.__plot_normalized_fitness(fitness_data)
        self.__plot_genetic_diversity(diversity_data)
        self.__plot_group_genetic_diversity(diversity_data, group=testcase["visulization"]["group"])
        best_genome_data = list(map(lambda gene: self.__binary_gene_to_list(gene, gene_size), max_genomes))
        self.__plot_hitmap(best_genome_data, 'Blues', title="Prime_Implicants_Usage_Heatmap")
        best_genome_cover_data = list(map(lambda gene: self.__generate_minterm_cover_list(gene, gene_size, prime_implicants, minterms), max_genomes))
        self.__plot_hitmap(best_genome_cover_data, 'Greys', title="Minterm_Coverage_Hitmap", has_colorbar=True, has_min_limit=True)

if __name__ == '__main__':
    GeneticQM().mainloop()