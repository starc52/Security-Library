from DLP_Hash import DLP_Hash
from PRG import PRG
import math 
class MD_Hash():
    
    def __init__(self, p, bit_length):
        self.p = p
        self.bit_length = bit_length
        self.prg = PRG(p, bit_length, bit_length)
        self.initialisation_vector = self.prg.to_binary(0, bit_length)
        self.dlphash = DLP_Hash(p, bit_length)
    
    def find_hash(self, x, size):
        num_blocks=math.ceil(size/self.bit_length)
        bin_x=self.prg.to_binary(x, size)
        block_bin_x = [bin_x[i:i+self.bit_length] for i in range(0, size, self.bit_length)]
        while len(block_bin_x[-1])<int(self.bit_length):
            block_bin_x[-1].append(0)
        Zi=self.dlphash.find_hash(self.prg.to_decimal(self.initialisation_vector), self.prg.to_decimal(block_bin_x[0]))
        for i in block_bin_x[1:]:
            Zi = self.dlphash.find_hash(Zi, self.prg.to_decimal(i))
        return Zi

if __name__ == "__main__":
    p = 397597169
    n = 32
    x = 60434036081813467198957516500056721430357908593353927313557709841642217411163
    size = 256
    mdhash=MD_Hash(p, n)
    prg = PRG(p, n, n)
    print(prg.to_binary(mdhash.find_hash(x, 256), n))