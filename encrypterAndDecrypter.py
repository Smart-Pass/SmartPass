'''
Encryption and Decryption Handling Module for SmartPass
'''
from random import randint
from base64 import b64encode, b64decode
from hashlib import sha512 as shake
from re import findall

class Cipher(): ###ENCRYPTION AND DECRYPTION CLASS
    
    ###--------------self.nums_key, self.pad, and self.unpad were taken from link below--------------###
    #####https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256#####
    ########## Written by "mnothic" and edited by "gregoltsov" ##########
    def __init__(self, key): ###INITIALIZES CIPHER AND EVERYTHING NEEDED TO ENCRYPT AND DECRYPT
        #self.nums_key = list(map(lambda x: ord(chr(x)), shake(key.encode()).digest())) #64 nums long
        self.shooketh = shake(key.encode()).digest()
        self.nums_key = list(map(lambda x: ord(chr(x)), self.shooketh)) #_#change ord(chr(x)) to ord(x)#_#
        self.block_size = 64 #block_size is 64 cause key must be 64 characters long
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size) ###pads the password to be 64 characters long
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])] ###unpads to its orginal character length
        
    def encrypter(self, plaintext):  ###ENCRYPTS DATA
        nums_pass = list(map(lambda x: ord(x), self.pad(plaintext))) ###pads plaintext that is entered and changes it to the number
        nums_encrypted = self.encRoundTwo(self.encRoundOne(nums_pass)) ###puts each number through round one and two of the encryption
        chars_encrypted = "".join(list(map(lambda x: chr(x), nums_encrypted))) ###changes each number into a character 
        encrypted = b64encode(chars_encrypted.encode()).decode() #encodes the strings of characters through the base64 encoding
        random = self.random(len(encrypted) + 15).decode()[:len(encrypted)+10] ###calls the random string function and assigns it to random
        if "=" not in encrypted: ###sometimes, encoding won't be padded with an '=' at the end, so it can't be decoded. This encodes the plaintext with no encryption and add it to the end of the random string
            ciphertext = random + b64encode(plaintext.encode()).decode()
            ciphertext += str(len(b64encode(plaintext.encode()).decode())) + "-\!="
        else: ###ELSE INTERTWINE THE ENCRYPTED AND THE RANDOM
            ciphertext = self.intertwine(encrypted, random)
        return ciphertext.encode()
        
    def encRoundOne(self, msg): ###ROUND ONE OF ENCRYPTION
        round1 = []
        nums_key_matched = self.nums_key
        for c in range(len(msg) - len(nums_key_matched)):
            nums_key_matched.append(self.nums_key[c])

        for i in range(len(msg)):
            round1.append(msg[i] + self.nums_key[i]) ###adds each number of the msg and the corresponding number of the key
        return round1
        
    def encRoundTwo(self, msg): ###ROUND TWO OF ENCRYPTION
        round2 = []
        for i in range(len(msg)):
            round2.append(msg[i] + self.nums_key[::-1][i]) ###adds each number of msg and the inverted corresponding number of the key
        return round2
        
    def decrypter(self, ciphertext): ###DECRYPTS DATA
        if  ciphertext.decode().endswith("-\!="): ###IF CIPHERTEXT ENDS WITH THAT STRING, THEN THAT MEANS JUST DECODE THE LAST BIT OF THE STRING BY PULLING THE LENGTH AND ONLY DECODING UP TO THAT LENGTH
            cipher_rev = ciphertext.decode()[:-1]
            cipher_rev = cipher_rev[::-1]
            end, beginning = cipher_rev.split("=")[0], "".join(cipher_rev.partition("=")[1:])
            pattern = r"[0-9]"
            number = findall(pattern, end)
            plength = int("".join(number[::-1]))
            encrypted = beginning[:plength][::-1]
            plaintext = b64decode(encrypted.encode())
            return plaintext.decode()
        else: ###ELSE IT WAS ENCODED NORMALLY AND SHOULD BE DECRYPTED BY REVERSING ROUND ONE AND TWO
            ciphertext = ciphertext.decode()[11:] ###first it needs to cut off the random string
            encrypted = ciphertext[::2]
            chars_encrypted_ = b64decode(encrypted.encode())#.decode() #_#b64decode(unicode(encrypted.encode()))#_#
            chars_encrypted = chars_encrypted_.decode() #_#something is wrong here#_#
            nums_encrypted = list(map(lambda x: ord(x), chars_encrypted))
            nums_pass = self.decRoundTwo(self.decRoundOne(nums_encrypted))
            plaintext = self.unpad("".join(list(map(lambda x: chr(x), nums_pass))))
            return plaintext
        
    def decRoundOne(self, msg): ###ROUND ONE OF DECRYPTION
        round1 = []
        nums_key_matched = self.nums_key
        for c in range(len(msg) - len(nums_key_matched)):
            nums_key_matched.append(self.nums_key[c])
        for i in range(len(msg)):
            round1.append(abs(msg[i] - nums_key_matched[::-1][i]))
        return round1
        
    def decRoundTwo(self, msg): ###ROUND TWO OF DECRYPTION
        round2 = []
        for i in range(len(msg)):
            round2.append(abs(msg[i] - self.nums_key[i]))
        return round2
        
    @staticmethod
    def random(length): ###MAKES A TOTALLY RANDOM STRING ENDING WITH OVER 150 BYTES TO INTIMIDATE AND CONFUSE HACKERS
        randStr = ""
        for i in range(length):
            randStr += chr(randint(0, 128))
        return b64encode(randStr.encode()) 
        
    @staticmethod
    def intertwine(ciphertext, random): ###INTERTWINES RANDOM AND ENCRYPTED STRING SO ENCRYPTED STRING ISN'T SO EASY TO SEE
        clength = len(ciphertext)
        crev = ciphertext[::-1]
        rlength = len(random)
        rrev = random[::-1]
        if rlength <= clength: raise ValueError("Length of ciphertext must be less than length of random text")
        intertwined = ""
        for i in range(clength):
            intertwined += crev[i] + rrev[i]
        erev = intertwined + rrev[clength:]
        return erev[::-1]
        
        
def encrypt(password): ###CALLS ENCRYPT FUNC
    cipher = Cipher("SmartPassLoginInformation")
    return cipher.encrypter(password)
    
def decrypt(password):
    cipher = Cipher("SmartPassLoginInformation") ###CALLS DECRYPT FUNC
    return cipher.decrypter(password)
