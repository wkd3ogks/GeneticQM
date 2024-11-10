from rich.table import Table
from Utils import integer_to_binary, console

# rich 말고 이미지로 차트 저장하기.
# prime implicant chart 출력 방식 변경하기

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