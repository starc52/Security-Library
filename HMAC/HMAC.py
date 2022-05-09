import math
from MD_Hash import MD_Hash
from PRG import PRG

class HMAC():
    def __init__(self, p, bit_length, ipad, opad): #ipad and opad are binary lists
        self.p = p
        self.bit_length = bit_length
        self.prg = PRG(p, bit_length, bit_length)
        self.ipad = self.prg.to_decimal(ipad*int(self.bit_length/len(ipad)))
        self.opad = self.prg.to_decimal(opad*int(self.bit_length/len(opad)))
        self.mdhash = MD_Hash(p, bit_length)
        self.initialisation_vector = self.prg.to_binary(0, self.bit_length)
        self.key = self.prg.generate(4294967295)

    def get_key(self):
        return self.key
    
    def update_key(self):
        self.key = self.prg.generate(self.key)

    def set_key(self, key):
        self.key = key

    def generate_tag(self, message, msg_len):
        input_bin = self.prg.to_binary(self.key^self.ipad, self.bit_length)
        output_bin = self.prg.to_binary(self.key^self.opad, self.bit_length)
        message_bin = self.prg.to_binary(message, msg_len)
        
        x = self.prg.to_decimal(input_bin+message_bin)
        first_mdhash = self.mdhash.find_hash(x, self.bit_length+msg_len)
        
        xnew = self.prg.to_decimal(output_bin+self.prg.to_binary(first_mdhash, self.bit_length))
        second_mdhash = self.mdhash.find_hash(xnew, self.bit_length*2)

        return second_mdhash

if __name__ == "__main__":
    p = 397597169
    bit_length = 32
    ipad = [0, 1, 0, 1, 1, 1, 0, 0]
    opad = [0, 0, 1, 1, 0, 1, 1, 0]
    message = 2333730895
    msg_len = 32
    hmac=HMAC(p, bit_length, ipad, opad)
    prg = PRG(p, bit_length, bit_length)
    print(prg.to_binary(hmac.generate_tag(message, msg_len), bit_length))