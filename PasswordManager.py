'''
Password Management
'''
import string
from random import choice, shuffle

class PasswordGenerator(): ###GENERATES PASSWORDS IF WANTED, CONTAINS AN ALGORITHM TO MAKE PASSWORDS BASED OFF OF THE USER'S PREFERENCE TO SYMBOLS, CAPITAL LETTERS, AND NUMBERS

    def __init__(self, length, capitals, numbers, characters, restricted, isExactly): ###INITIALIZES PASSWORD OBJECT
        self.length = length #desired length of password
        self.capitals = capitals #how many capitals the user wants
        self.numbers = numbers #how many numbers the user wants
        self.characters = characters #how many characters the user wants
        self.restricted = restricted #what letters, numbers, or characters cannot be in the password
        self.isExactly = isExactly #if true, password has exactly the amount of letters, numbers, and characters provided. If false, has at least those numbers
        ###BELOW ARE CONSTANTS
        self.LOWERCASE = self.removeRestricted(string.ascii_lowercase, restricted)
        self.UPPERCASE = self.removeRestricted(string.ascii_uppercase, restricted)
        self.DIGITS = self.removeRestricted(string.digits, restricted)
        self.CHARS = self.removeRestricted(" " + string.punctuation, restricted)
        self.ALL = self.LOWERCASE + self.UPPERCASE + self.DIGITS + self.CHARS

    def generator(self): ###GENERATES THE PASSWORD RANDOMLY
        password = [choice(self.UPPERCASE) for i in range(self.capitals)] + [choice(self.DIGITS) for i in range(self.numbers)] + [choice(self.CHARS) for i in range(self.characters)]
        if self.isExactly:
            password += [choice(self.LOWERCASE) for i in range(self.length - len(password))]
        else:
            password += [choice(self.ALL) for i in range(self.length - len(password))]
        shuffle(password)
        password = "".join(password)
        return password

    def exceptionHandler(self):
        

    @staticmethod 
    def removeRestricted(word, notAllowed): ###DELETES RESTRICTED LETTERS, NUMBERS, AND CAPITALS FROM CONSTANDS DEFINED ABOVE
        for c in notAllowed:
            word = word.replace(c, "")
        return word


def generate(len_ = 15, caps = 2, nums = 2, chars = 2, notAllowed = "", exactly = False):
    word = PasswordGenerator(len_, caps, nums, chars, notAllowed, exactly)
    return word.generator()
