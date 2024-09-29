import random
import math
from abc import ABC, abstractmethod
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt


# 1순위
# 점수 best solution 리스트로 표현할까?
# 상위 5개를 보여주는거야

# 2순위
# Quine McClusky 클래스 코드 정리

class CrossoverStrategy(ABC):
    @abstractmethod
    def process(self, parents, gene_size):
        pass


class SinglePointCrossover(CrossoverStrategy):
    def process(self, parents, gene_size):
        random_point = random.randrange(gene_size)
        mask = (1 << random_point) - 1
        child_genome = (parents[1] & mask) | (parents[0] & ~mask)
        return child_genome


class UniformCrossover(CrossoverStrategy):
    def process(self, parents, gene_size):
        genome = 0
        for i in range(gene_size):
            if random.random() < 0.5:
                genome |= (parents[0] & (1 << i))
            else:
                genome |= (parents[1] & (1 << i))
        return genome


class SelectionStrategy(ABC):
    @abstractmethod
    def process(self, parent_population_size, genomes_with_fitness):
        pass

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

class RouletWheelSelection(SelectionStrategy):
    def __init__(self, population_size):
        self.population_size = population_size
    def __lower_bound(self, fitness_sum, find):
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
        for genome_with_fitness in genomes_with_fitness:
            if not fitness_sum:
                fitness_sum.append(genome_with_fitness[0])
            else:
                fitness_sum.append(fitness_sum[-1] + genome_with_fitness[0])
            total_fitness += genome_with_fitness[0]
        idx = 0

        while idx < parent_population_size:
            random_number = random.randrange(total_fitness + 1)

            genome_idx = self.__lower_bound(fitness_sum, random_number)
            selected_genome = genomes_with_fitness[genome_idx][1]
            parent_genomes.append(selected_genome)
            idx += 1
        return parent_genomes

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
    def evaluate_fitness(self, genomes, epoch, weight=1):
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
            fitness = weight * len(cover_set) + len(self.prime_implicants) - used_prime_implicant
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
            total_fitness, min_genome, max_genome, child_genomes = self.evaluate_fitness(genomes, epoch, weight=2)
            fitness_plot.update(epoch, total_fitness / self.population_size, max_genome[0], min_genome[0])
            best_gene_hitmap.append(self.__binary_gene_to_list(max_genome[1]))
            covered_minterm_hitmap.append(self.__generate_mintom_cover_list(max_genome[1]))
            genomes = self.__select_next_genomes(child_genomes)
        self.__render_result()
        fitness_plot.finalize()
        covered_minterm_hitmap.show('Greys', has_colorbar=True, has_min_limit=True)
        best_gene_hitmap.show('Blues')


class FitnessPlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.avg_history = []
        self.best_history = []
        self.worst_history = []
        self.avg_line, = self.ax.plot([], [], label='Average Fitness')
        self.best_line, = self.ax.plot([], [], label='Best Fitness')
        self.worst_line, = self.ax.plot([], [], label='Worst Fitness')

    def init(self):
        plt.xlabel("Epoch")
        plt.ylabel("Fitness")
        plt.legend()
        plt.ion()


    def update(self, epoch, avg_fitness, best_fitness, worst_fitness):
        self.avg_history.append(avg_fitness)
        self.best_history.append(best_fitness)
        self.worst_history.append(worst_fitness)

        self.avg_line.set_data(range(len(self.avg_history)), self.avg_history)
        self.best_line.set_data(range(len(self.best_history)), self.best_history)
        self.worst_line.set_data(range(len(self.worst_history)), self.worst_history)

        self.ax.relim()
        self.ax.autoscale_view()

        plt.pause(0.05)

    def finalize(self):
        plt.ioff()
        plt.show()


class HitmapPlot:
    def __init__(self, title):
        self.data_list = []
        self.title = title

    def append(self, data):
        self.data_list.append(data)

    def show(self, color, has_colorbar=False, has_min_limit=False):
        plt.matshow(self.data_list, cmap=plt.get_cmap(color))
        if has_colorbar:
            plt.colorbar(shrink=0.8, aspect=10)
        if has_min_limit:
            plt.clim(vmin=0)
        plt.title(self.title)
        plt.savefig(f'{self.title}.png')


class QuineMcClusky:
    def __init__(self, minterms, dontcares):
        self.minterms = minterms
        self.dontcares = dontcares
        self.max_bit = len(bin(max(minterms + dontcares))) - 2
        self.prime_implicants = []

    def __init_table(self):
        table = {}
        for term in self.minterms + self.dontcares:
            bit_count = term.bit_count()
            if bit_count not in table:
                table[bit_count] = [((term,), 0)]
            else:
                table[bit_count].append(((term,), 0))
        self.__render_table(1, table)
        return table

    def __combine_minterm_with_dash(self, binary_minterm, dash):
        combine_minterm_with_dash = [bit for bit in binary_minterm]
        for i in range(self.max_bit):
            if (dash >> i) & 1:
                combine_minterm_with_dash[self.max_bit - 1 - i] = '-'
        return ''.join(combine_minterm_with_dash)

    def __render_table(self, step_number, table):
        render_table = Table(title=f"Column {step_number}")
        for column in ["Group No.", "Minterms", "Binary of Minterms"]:
            render_table.add_column(column)

        for bit_count in sorted(table):
            is_first_row = True
            group_size = len(table[bit_count])
            for idx, term in enumerate(sorted(table[bit_count])):
                # combine with dash
                term_to_binary = self.__combine_minterm_with_dash(integer_to_binary.process(term[0][0], self.max_bit), term[1])
                if is_first_row:
                    render_table.add_row(str(bit_count),
                                         ', '.join(map(str, term[0])),
                                         term_to_binary,
                                         style='bright_green',
                                         end_section=(idx == group_size - 1)
                                         )
                    is_first_row = False
                else:
                    render_table.add_row(' ',
                                         ', '.join(map(str, term[0])),
                                         term_to_binary,
                                         style='bright_green',
                                         end_section=(idx == group_size - 1)
                                         )
        console.print(render_table)

    def __merge_minterm(self, step_number, table):  # return True or False
        new_table = {}
        generated_minterms_set = set()
        not_prime_implicants = set()
        groups = sorted(table)
        for group_bit_count in groups:
            group = sorted(table[group_bit_count])
            if group_bit_count + 1 not in table:
                for minterm in group:
                    if tuple(minterm[0]) not in not_prime_implicants:
                        self.prime_implicants.append(tuple(minterm[0]))
                continue
            target_group = sorted(table[group_bit_count + 1])
            for minterm in group:
                if tuple(minterm[0]) not in not_prime_implicants:
                    is_prime_implicant = True
                else:
                    is_prime_implicant = False
                for target_minterm in target_group:
                    if minterm[1] != target_minterm[1]:  # "-" 가 동일한 위치에 있지 않은 경우
                        continue
                    minterm_with_dash = minterm[0][0] | minterm[1]
                    target_minterm_with_dash = target_minterm[0][0] | target_minterm[1]
                    if (minterm_with_dash ^ target_minterm_with_dash).bit_count() == 1:
                        is_prime_implicant = False
                        not_prime_implicants.add(tuple(target_minterm[0]))
                        if tuple(sorted(minterm[0] + target_minterm[0])) in generated_minterms_set:  # 중복 제거
                            continue
                        if group_bit_count not in new_table:
                            new_table[group_bit_count] = []
                        new_table[group_bit_count].append((sorted(minterm[0] + target_minterm[0]),
                                                           (minterm_with_dash ^ target_minterm_with_dash) + minterm[1]))
                        generated_minterms_set.add((tuple(sorted(minterm[0] + target_minterm[0]))))
                if is_prime_implicant:
                    self.prime_implicants.append(tuple(minterm[0]))
        if new_table:
            self.__render_table(step_number, new_table)
        return new_table

    def __set_prime_implicant(self):
        new_table = self.__init_table()
        step_number = 2
        while True:
            table = new_table
            new_table = self.__merge_minterm(step_number, table)
            step_number += 1
            if not new_table:
                break
        return self.prime_implicants

    def __display_prime_implicant_chart(self):
        render_table = Table(title="Prime Implicant Chart")
        minterm_dict = {}
        for idx, minterm in enumerate(self.minterms):
            minterm_dict[minterm] = idx
        for column in ["Prime Implicants \\ Minterms"] + list(map(str, self.minterms)):
            render_table.add_column(column)
        for prime_implicant in self.prime_implicants:
            data = [' ' for _ in range(len(self.minterms))]
            for minterm in prime_implicant:
                if minterm in minterm_dict:
                    data[minterm_dict[minterm]] = 'X'
            render_table.add_row(str(prime_implicant), *data, end_section=True)
        console.print(render_table)
    # 민텀과 주항 리턴
    def process(self, builder):
        self.__set_prime_implicant()
        self.__display_prime_implicant_chart()
        builder.set_prime_implicants(self.prime_implicants)
        builder.set_minterms(self.minterms)
        algorithm = builder.build()
        algorithm.process()
        return (self.prime_implicants, self.minterms)

class IntegerToBinaryConverter:
    def process(self, integer, max_bit):
        return format(integer, 'b').zfill(max_bit)

if __name__ == '__main__':
    console = Console()

    # testcase 1
    # minterms = [2, 3, 1, 5]
    # dontcares = [6, 7]

    # testcase 2 (21, 3)
    # minterms = [0, 1, 2, 5, 6, 7, 8, 9, 10, 14]
    # dontcares = []

    # testcase 3 (7, 3)
    # minterms = [2, 6, 8, 9, 10, 11, 14, 15]
    # dontcares = []

    # testcase 4
    # minterms = [5, 9, 23]
    # dontcares = []

    # testcase 5 (25, 3)
    # minterms = [4, 8, 10, 11, 12, 15]
    # dontcares = []

    # minterms = [2, 6, 8, 9, 10, 11, 14, 15, 41, 27, 36]
    # dontcares = []

    # 0-11--,01--0-,101-0-,0100-1,10-0-1,0-0001,0-1-10,10-10-,-0-100,-00010
    # a'cd + a'be' + ab'ce' + a'bc'd'f + ab'd'f + a'c'd'e'f + a'cef' + ab'de' + b'de'f' + b'c'd'ef'
    minterms = [1, 2, 4, 10, 12, 13, 14, 15, 16, 17, 19, 20, 21, 24, 25, 26, 28, 29, 30, 31, 33, 34, 35, 36, 37, 40, 41, 43, 44, 45]
    dontcares = []
    # (202391, 10)
    # minterms = [42, 95, 246, 287, 301, 323, 392, 462, 489, 563, 572, 612, 623, 677, 686, 696, 728, 730, 750, 751, 755, 784, 802, 810, 821, 872, 935, 938, 989, 993]
    # dontcares = []

    # minterms = [1, 3, 6, 8, 10, 11, 34, 38, 41, 54, 57, 61, 62, 65, 67, 69, 70, 87, 91, 96]
    # dontcares = []
    #
    # minterms = [3, 5, 7, 11, 12, 13, 20, 21, 23, 25, 26, 30, 34, 44, 48, 49, 52, 53, 59, 60, 68, 72, 74, 77, 82, 87, 91, 96, 99, 100]
    # dontcares = []
    #
    # minterms = [1, 4, 6, 7, 9, 10, 11, 15, 16, 19, 20, 25, 31, 32, 33, 34, 38, 41, 42, 43, 47, 48, 49, 52, 59, 60, 68, 77, 79, 80, 81, 83, 85, 86, 89, 90, 92, 93, 96, 98]
    # dontcares = []
    #
    # minterms = [29, 51, 66, 106, 116, 134, 161, 162, 184, 229, 264, 280, 305, 306, 312, 323, 349, 361, 405, 420, 431, 477, 495, 523, 549, 573, 580, 603, 626, 648, 656, 661, 673, 685, 689, 707, 719, 720, 775, 786, 793, 876, 878, 916, 924, 926, 947, 974, 988, 995]
    # dontcares = []
    #
    minterms = [1, 12, 21, 24, 27, 30, 33, 40, 46, 48, 49, 50, 53, 55, 57, 62, 65, 66, 70, 72, 77, 85, 90, 91, 94, 98, 103, 107, 113, 117, 126, 133, 136, 144, 146, 151, 154, 157, 164, 173, 174, 177, 178, 197, 198, 204, 205, 219, 227, 238]
    dontcares = []
    # minterms = [2,6,8,9,10,11,14,15]
    # dontcares = [4, 7]

    integer_to_binary = IntegerToBinaryConverter()
    qm = QuineMcClusky(minterms, dontcares)
    gene_builder = (GeneticAlgorithmBuilder().set_crossover_strategy(UniformCrossover())
     .set_population_size(400)
     .set_epoch(350)
     .set_weight(1.5)
     .set_mutation_rate(0.2))
    qm.process(gene_builder)