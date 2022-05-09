from PRG import PRG
from PRF import PRF

class fixedLengthMAC():
    def __init__(self, p, n):
        self.n = n
        self.PRG = PRG(p, n, n)
        self.PRF = PRF(p, n)
        self.key = self.PRG.generate(4294967295)
    
    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def update_key(self):
        self.key = self.PRG.generate(self.key)
    
    def generate_tag(self, message):
        tag = self.PRF.generate(self.key, message)
        return tag

    def verify(self, message, key, tag):
        check_tag = self.PRF.generate(key, message)
        if check_tag == tag:
            return True
        else:
            return False

class variableLengthMAC():
    def __init__(self, p, n):
        self.n = n
        self.PRG = PRG(p, n, n)
        self.PRGby4 = PRG(p, int(n/4), int(n/4))
        self.rby4 = 211
        self.PRF = PRF(p, n)
        self.flMAC = fixedLengthMAC(p, n)
        self.key = self.flMAC.get_key()
        self.num_blocks=0
    def get_key(self):
        return self.flMAC.get_key()
    
    def update_key(self):
        self.key = self.flMAC.update_key()

    def get_nby4_bits(self, tag):
        binar=self.PRG.to_binary(tag, ((self.num_blocks*self.n)+int(self.n/4)))
        return binar[:int(self.n/4)]

    def generate_tag(self, message, msg_size, rby4=None, key=None):
        bin_msg=self.PRG.to_binary(message, msg_size)
        
        assert len(bin_msg)<=pow(2, int(self.n/4)-1)

        nby4blocks = [bin_msg[i:i+int(self.n/4)] for i in range(0, len(bin_msg), int(self.n/4))]
        while len(nby4blocks[-1])<int(self.n/4):
            nby4blocks[-1].append(0)
        self.num_blocks = len(nby4blocks)
        if rby4==None:
            self.rby4 = self.PRG.to_binary(self.PRGby4.generate(self.rby4), int(self.n/4))
        else:
            self.rby4 = rby4

        if key!=None:
            self.flMAC.set_key(key)

        d_encode = self.PRG.to_binary(len(nby4blocks), int(self.n/4))
        concats = [self.rby4+d_encode+self.PRG.to_binary(id, int(self.n/4))+v for id, v in enumerate(nby4blocks)]
        tags = [self.PRG.to_binary(self.flMAC.generate_tag(self.PRG.to_decimal(i)), self.n) for i in concats]

        tag=self.rby4
        for i in tags:
            tag+=i
        return self.PRG.to_decimal(tag)
    
    def verify(self, message, msg_size, key, tag):
        rby4=self.get_nby4_bits(tag)
        check_tag=self.generate_tag(message, msg_size, rby4=rby4, key=key)
        if check_tag == tag:
            return True
        else:
            return False

if __name__ == "__main__":
    p = 397597169
    n = 32
    flmac=fixedLengthMAC(p, n)
    vlmac = variableLengthMAC(p, n)
    # message = 1801809519
    message = 2333730895
    msg_size = 32
    tag=vlmac.generate_tag(message, msg_size)
    key = vlmac.get_key()
    print(vlmac.verify(message, msg_size, key, tag))

    flmac_tag = flmac.generate_tag(message)
    flmac_key = flmac.get_key()
    print(flmac.verify(message, flmac_key, flmac_tag))
