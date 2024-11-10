from rich.console import Console

class IntegerToBinaryConverter:
    def process(self, integer, max_bit):
        return format(integer, 'b').zfill(max_bit)

integer_to_binary = IntegerToBinaryConverter()
console = Console()