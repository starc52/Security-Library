import math
import random
from PRG import PRG

class DLP_Hash():
    def __init__(self, p, bit_length):
        self.p = p
        self.bit_length=bit_length
        self.prg = PRG(p, bit_length, bit_length)
        self.g = self.find_primitve_root()
        self.h = pow(self.g, random.randint(0, 2**self.bit_length-1), self.p)

    def prime_factors(self, number):
        prime_factor=set([])
        while not number%2:
            prime_factor.add(2)
            number//=2
        sqt = int(math.sqrt(number))
        for i in range(3, sqt, 2):
            while not number%i:
                prime_factor.add(i)
                number//=i
        if(number>=1):
            prime_factor.add(number)
        return list(prime_factor)

    def find_primitve_root(self):
        phi = self.p-1
        phi_prime_factors = self.prime_factors(phi)

        for i in range(2, phi+1):
            flag=True
            for pr in phi_prime_factors:
                if pow(i, phi//pr, self.p) == 1:
                    flag=False
                    break
            if flag == True:
                return i
        return -1
    def find_hash(self, x1, x2):
        return pow(pow(self.g, x1, self.p)*pow(self.h, x2, self.p), 1, self.p)

if __name__=="__main__":
    p = 397597169
    n = 32
    dlphash = DLP_Hash(397597169, 32)
    random_64_bit = 8223120412262738161
    prg = PRG(p, n, n)
    x1, x2 = prg.break_halves(random_64_bit, 64)
    hash=dlphash.find_hash(x1, x2)
    print(prg.to_binary(hash, n))