from PRG import PRG

class PRF():
    def __init__(self, p, n):
        self.n = n
        self.PRG = PRG(p, n, 2*n)
    def generate(self, x, y): # x and y together form 2*n length vector. 
        binary_x = self.PRG.to_binary(x, self.n)
        Gxi=self.PRG.generate(y)
        first_half, second_half = self.PRG.break_halves(Gxi, 2*self.n)
        for i in binary_x[:-1]:
            if i == 0:
                Gxi = self.PRG.generate(first_half)
            else:
                Gxi = self.PRG.generate(second_half)
            first_half, second_half = self.PRG.break_halves(Gxi, 2*self.n)
        if binary_x[-1]==0:
            return first_half
        else:
            return second_half

if __name__ == "__main__":
    p = 397597169
    n = 16
    prg=PRG(p, n, 2*n)
    random_32_bit = 4039927112
    first, second=prg.break_halves(random_32_bit, 32)
    prf=PRF(p, n)

    print(prf.generate(first, second))