from src.Algorithm import Algorithm
from overrides import overrides

class KnuthX(Algorithm):
    def __init__(self):
        super().__init__()

        # dictionary for minterm to index
        self.minterm_to_index = {}

        # logical deletion of rows and columns
        self.deleted_rows = set() # also solution set
        self.deleted_columns = set()
        
    def __init_minterm_to_index(self):
        """
        Initialize the dictionary for minterm to index.
        """
        for index, minterm in enumerate(self.minterms):
            self.minterm_to_index[minterm] = index
        return None

    def create_knuth_table(self):
        """
        Create a table for Knuth's Algorithm X.

        Args:
            prime_implicants (list[int]): list of prime implicants

        Returns:
            list[list[int]]: table for Knuth's Algorithm X
        """
        self.__init_minterm_to_index()
        minterm_size = len(self.minterms)
        prime_implicant_size = len(self.prime_implicants)

        # initialize the table with False
        self.table = []
        for _ in range(prime_implicant_size):
            self.table.append([False for __ in range(minterm_size)])
        
        # fill the table
        for i, prime_implicant in enumerate(self.prime_implicants):
            for minterm in prime_implicant:
                if minterm in self.minterm_to_index: # ignore dont cares
                    self.table[i][self.minterm_to_index[minterm]] = True

        # set rows and columns size
        self.row_size = len(self.table)
        self.column_size = len(self.table[0])

        # print the table for debugging
        for i in range(prime_implicant_size):
            for j in range(minterm_size):
                print(self.table[i][j], end=" ")
            print()  

        return self.table
    
    def find_target_column(self):
        """
        Find the column with the minimum number of 1's in the table.

        Returns:
            int: the index of the column
        """

        # initialize the minimum number of 1's and the target column
        min_ones = float('inf')
        target_column = -1

        for x in range(self.column_size):
            # skip logically deleted columns
            if x in self.deleted_columns:
                continue
            ones = 0
            for y in range(self.row_size):
                # skip logically deleted rows
                if y in self.deleted_rows: 
                    continue
                if self.table[y][x]: # check if the element is 1
                    ones += 1
            if ones < min_ones:
                min_ones = ones
                target_column = x
        return target_column

    def include_partial_solution(self, column_index):
        for y in range(self.row_size):
            # skip logically deleted rows
            if y in self.deleted_rows:
                continue
            if self.table[y][column_index]:
                self.deleted_rows.add(y)
                for x in range(self.column_size):
                    if self.table[y][x]:
                        self.deleted_columns.add(x)