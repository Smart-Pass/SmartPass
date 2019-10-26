import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

###link below holds where Cipher came from###
###https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256###
class AESCipher():

    def __init__(self, key): 
        self.block_size = AES.block_size ###block size is of length 16
        self.key = hashlib.sha256(key.encode()).digest() ###key length is 32
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size) ###pads the password to be 16 characters long
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])] ###unpads to its orginal character length

    def encrypter(self, plaintext):
        plaintext = self.pad(plaintext)
        iv = Random.new().read(AES.block_size) ###makes random string and attaches to finished ciphertext
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(plaintext))

    def decrypter(self, ciphertext):
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(ciphertext[AES.block_size:]))#.decode()

def encrypt(string):
  cipher = AESCipher("SmartPassLoginSaver")
  return cipher.encrypter(string)

def decrypt(string):
  cipher = AESCipher("SmartPassLoginSaver")
  return cipher.decrypter(string)
