from PRG import PRG
from PRF import PRF

class CPA_secure_encrypt():
    def __init__(self, p, n): # n is 32 for normal operation
        self.n = n
        self.PRG = PRG(p, n, n)
        self.PRF = PRF(p, n) # because PRF implementation takes 2 n bit numbers and outputs 1 n bit number 
        self.rndm = 4039927112 # 32 bit random number
        self.key = self.PRG.generate(4294967295) # 1^32
    
    def get_key(self):
        return self.key
    
    def update_key(self):
        self.key = self.PRG.generate(self.key)

    def encrypt(self, message):
        self.rndm=self.PRG.generate(self.rndm)
        f_random=self.PRF.generate(self.key, self.rndm)
        encrypted = self.PRG.to_decimal(self.PRG.to_binary(self.rndm, self.n)+self.PRG.to_binary(f_random^message, self.n))
        return encrypted
        
class CPA_secure_decrypt():
    def __init__(self, p, n): # n is 32
        self.n = n
        self.PRG = PRG(p, n, n)
        self.PRF = PRF(p, n)
    
    def decrypt(self, cipher, key):
        rndm, xor_message=self.PRG.break_halves(cipher, 2*self.n)
        f_random=self.PRF.generate(key, rndm)
        message = f_random^xor_message
        return message

if __name__ == "__main__":
    p = 397597169
    encryption = CPA_secure_encrypt(p, n=32)
    decryption = CPA_secure_decrypt(p, n=32)
    encryption_key = encryption.get_key()
    # message = 1801809518
    message = 2333730895
    print("message", message)
    cipher=encryption.encrypt(message)
    print("cipher", cipher)
    print("decrypted message", decryption.decrypt(cipher, encryption_key))

