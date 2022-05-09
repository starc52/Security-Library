from CPA_Secure import *
from Secure_MAC import *
from PRG import PRG
from PRF import PRF

class CCA_secure_encrypt():
    def __init__(self, p, n):
        self.n = n
        self.PRG = PRG(p, n, n)
        self.PRF = PRF(p, n)
        self.CPA_en = CPA_secure_encrypt(p, n)
        self.CPA_de = CPA_secure_decrypt(p, n)
        self.vlmac = variableLengthMAC(p, n)
        self.CPA_en.update_key()
        self.vlmac.update_key()
        self.vlmac.update_key()

    def get_key_cpa(self):
        return self.CPA_en.get_key()
    
    def get_key_vlmac(self):
        return self.vlmac.get_key()
    
    def encrypt(self, message, msg_size):
        bin_msg=self.PRG.to_binary(message, msg_size)
        bin_msg_blocks = [self.PRG.to_decimal(bin_msg[i:i+self.n]) for i in range(0, msg_size, self.n)]
        cipher_text_blocks=[self.CPA_en.encrypt(block) for block in bin_msg_blocks]
        cipher_binary_blocks=[self.PRG.to_binary(block, 2*self.n) for block in cipher_text_blocks]
        
        cipher = []
        for i in cipher_binary_blocks:
            cipher+=i
        cipher_size = len(cipher)
        cipher_dec = self.PRG.to_decimal(cipher)
        tag=self.vlmac.generate_tag(cipher_dec, cipher_size)
        tag_size = (self.vlmac.num_blocks*self.n)+int(n/4)
        return cipher_dec, tag, cipher_size, tag_size

class CCA_secure_decrypt():
    def __init__(self, p, n):
        self.n = n
        self.PRG = PRG(p, n, n)
        self.PRF = PRF(p, n)
        self.CPA_en = CPA_secure_encrypt(p, n)
        self.CPA_de = CPA_secure_decrypt(p, n)
        self.vlmac = variableLengthMAC(p, n)
    
    def decrypt(self, cipher_dec, tag_dec, key_cpa, key_vlmac, cipher_size, tag_size):
        cipher_bin=self.PRG.to_binary(cipher_dec, cipher_size)
        tag_bin = self.PRG.to_binary(tag_dec, tag_size)
        check_authencity=self.vlmac.verify(cipher_dec, cipher_size, key_vlmac, tag_dec)
        if not check_authencity:
            return -1
        ciphermessage = cipher_bin[:cipher_size]
        cipher_dec_blocks = [self.PRG.to_decimal(ciphermessage[i:i+2*self.n]) for i in range(0, cipher_size, 2*self.n)]
        msg_bin_blocks = [self.PRG.to_binary(self.CPA_de.decrypt(i, key_cpa), self.n) for i in cipher_dec_blocks]
        msg=[]
        for i in msg_bin_blocks:
            msg+=i
        dec_msg = self.PRG.to_decimal(msg)
        return dec_msg

if __name__ == "__main__":
    p = 397597169
    n = 32
    encryption = CCA_secure_encrypt(p, n)
    decryption = CCA_secure_decrypt(p, n)
    message = 13114889359570883559
    print("message", message)
    msg_size = 64
    key_cpa = encryption.get_key_cpa()
    key_vlmac = encryption.get_key_vlmac()
    cipher_dec, tag_dec, cipher_size, tag_size=encryption.encrypt(message, msg_size)
    print("cipher", cipher_dec)
    print("tag", tag_dec)
    print("decryption", decryption.decrypt(cipher_dec, tag_dec, key_cpa, key_vlmac, cipher_size, tag_size))
