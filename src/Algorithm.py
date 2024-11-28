"""
    Base class for setting prime implicants and minterms
"""

class Algorithm:
    def __init__(self):
        self.prime_implicants = None
        self.minterms = None
    
    def set_prime_implicants(self, prime_implicants):
        self.prime_implicants = prime_implicants
    
    def set_minterms(self, minterms):
        self.minterms = minterms