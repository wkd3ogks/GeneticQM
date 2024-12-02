import os

class QuineMcCluskey:
    def __init__(self, minterms, dontcares, output_directory):
        self.minterms = minterms
        self.dontcares = dontcares
        self.max_bit = len(bin(max(minterms + dontcares))) - 2 # 2 is the length of '0b'
        self.prime_implicants = []

        # create quine_mccluskey output directory
        self.output_directory = os.path.join(output_directory, 'quine_mccluskey')
        os.makedirs(self.output_directory, exist_ok=True)

    def __init_table(self):
        """ 
        Initialize the table with minterms and dontcares

        Returns:
            dict: key: bit_count(group), value: list of tuple (minterms, dash_position)
        """
        table = {} 
        for term in self.minterms + self.dontcares:
            bit_count = term.bit_count() # number of 1s in the binary representation
            if bit_count not in table:
                table[bit_count] = [((term,), 0)] 
            else:
                table[bit_count].append(((term,), 0))

        self.__save_table_to_csv(table)
        # self.__render_table(1, table)
        return table

    def __combine_minterm_with_dash(self, binary_minterm, dash):
        """
        for debugging purpose, combine minterm with dash information

        Args:
            binary_minterm (str): minterm in binary format string
            dash (int): dash location information

        Returns:
            str: combined minterm with dash
        """
        combine_minterm_with_dash = [bit for bit in binary_minterm]
        for i in range(self.max_bit):
            if (dash >> i) & 1:
                combine_minterm_with_dash[self.max_bit - 1 - i] = '-'
        return ''.join(combine_minterm_with_dash)

    def __save_table_to_csv(self, table, step_name='step_1'):
        """
        save the quine mccluskey table to csv file

        Args:
            table (dict): key: bit_count(group), value: list of tuple (minterms, dash_position)
            step_name (str, optional): step name. Defaults to 'step_1'.
        """
        with open(os.path.join(self.output_directory, f'{step_name}_table.csv'), 'w') as f:
            for bit_count in sorted(table):
                for minterms, dash_position in sorted(table[bit_count]):
                    integer_to_binary = format(minterms[0], 'b').zfill(self.max_bit) # convert integer to binary format
                    term_to_binary = self.__combine_minterm_with_dash(integer_to_binary, dash_position)
                    f.write(f"{bit_count}, {term_to_binary}\n")

    def __save_prime_implicants_to_csv(self):
        """
        save the prime implicants to csv file
        first element is the index of the prime implicant and second element is the prime implicant's minterms
        """
        with open(os.path.join(self.output_directory, 'prime_implicants.csv'), 'w') as f:
            for index, prime_implicant in enumerate(self.prime_implicants):
                f.write(f"{index + 1}, {'(' + ' '.join(map(str, prime_implicant)) + ')'}\n") 

    def __merge_minterm(self, step_number, table):
        """
        merge minterms to find prime implicants

        Args:
            step_number (int): _description_
            table (): _description_

        Returns:
            dict: key: bit_count(group), value: list of tuple (minterms, dash_position)
        """
        new_table = {}
        generated_minterms_set = set()
        not_prime_implicants = set() # set of not prime implicants
        groups = sorted(table) # sort by group number(bit_count) to compare with the next group
        for group_bit_count in groups: 
            group = sorted(table[group_bit_count])
            if group_bit_count + 1 not in table: # unable to find 1 bit difference group
                for minterm, _ in group: 
                    if tuple(minterm) not in not_prime_implicants:
                        self.prime_implicants.append(tuple(minterm))
                continue
            else: # find 1 bit difference group
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
            self.__save_table_to_csv(new_table, f'step_{step_number}')
        return new_table

    def process(self):
        """
        Quine McCluskey main process

        Returns:
            (int, int): prime implicants(list[tuple[int]]) and minterms(list[int])
        """
        new_table = self.__init_table()
        step_number = 2
        while True:
            table = new_table
            new_table = self.__merge_minterm(step_number, table)
            step_number += 1
            if not new_table: # empty table
                break
        self.__save_prime_implicants_to_csv()
        return (self.prime_implicants, self.minterms)
