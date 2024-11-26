import os
from rich.console import Console

class IntegerToBinaryConverter:
    def process(self, integer, max_bit):
        return format(integer, 'b').zfill(max_bit)

def validate_testcase(testcase_file):
    # validate testcase file
    if not testcase_file.endswith('.json'):
        print("[Error] Testcase file must be a json file.")
        exit(1)
    if not os.path.exists(testcase_file):
        print(f"[Error] Testcase file '{testcase_file}' not found.")
        exit(1)

integer_to_binary = IntegerToBinaryConverter()
console = Console()