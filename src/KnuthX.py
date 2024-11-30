from src.Algorithm import Algorithm

class KnuthX(Algorithm):
    def __init__(self):
        super().__init__()
        self.deleted_rows = set()
        self.deleted_columns = set()
    
    def create_knuth_table(self):
        """
        Create a table for Knuth's Algorithm X.

        Args:
            prime_implicants (list[int]): list of prime implicants

        Returns:
            list[list[int]]: table for Knuth's Algorithm X
        """
        pass
    