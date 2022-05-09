import math

class PRG():
    def __init__(self, p, k, l):
        self.p = p
        self.k = k
        self.l = l
        self.g = self.find_g()
        print("g", self.g)
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
    
    def find_g(self):
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

        
    def to_binary(self, x, bit_length): #input is decimal
        binary=[char for char in bin(x).replace("0b", "").zfill(bit_length)]
        binary = [eval(i) for i in binary]
        return binary
    
    def to_decimal(self, list_bin):
        dec=0
        power=1
        list_bin.reverse()
        for i in list_bin:
            dec+=(power*i)
            power*=2
        return dec
    
    def get_last_bit(self, dec, bit_length):
        binary=self.to_binary(dec, bit_length)
        return binary[-1]
    
    def break_halves(self, dec, bit_length):
        binary = self.to_binary(dec, bit_length)
        first_half = self.to_decimal(binary[:int(len(binary)/2)])
        second_half = self.to_decimal(binary[int(len(binary)/2):])
        return first_half, second_half
    
    def generate_one_bit(self, x, y, bit_length): # bit length is the x, y bit length # all arguments in decimal format
        f = pow(self.g, x, self.p)
        bit_and = x&y
        bit_and_bin=self.to_binary(bit_and, bit_length)
        b=0
        for i in bit_and_bin:
            b = b^i
        return self.to_decimal(self.to_binary(f, bit_length)+self.to_binary(y, bit_length)+[b])
    
    def generate(self, s):
        t=s
        r=[]
        for i in range(self.l):
            halves=self.break_halves(t, self.k)
            t=self.generate_one_bit(halves[0], halves[1], int(self.k/2))
            r = r+[self.get_last_bit(t, self.k)]
            t = self.to_decimal(self.to_binary(t, self.k+1)[:-1])
        return self.to_decimal(r)

if __name__ == "__main__":
    prg=PRG(397597169, 16, 32) # prime number, length of seed in binary and length of output in binary
    random=prg.generate(4039927112)
    print(random)
    for i in range(10):
        random = prg.generate(random)
        print(random)
