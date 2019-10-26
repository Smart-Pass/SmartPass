'''
Password Management
'''
import string
from random import choice, shuffle

def generate(length = 15, caps = 2, nums = 2, chars = 2, restricted = "", isExactly = False):
    ###BELOW ARE CONSTANTS
    LOWERCASE = removeRestricted(string.ascii_lowercase, restricted)
    UPPERCASE = removeRestricted(string.ascii_uppercase, restricted)
    DIGITS = removeRestricted(string.digits, restricted)
    CHARS = removeRestricted(" " + string.punctuation, restricted)
    ALL = LOWERCASE + UPPERCASE + DIGITS + CHARS

    password = [choice(UPPERCASE) for i in range(caps)] + [choice(DIGITS) for i in range(nums)] + [choice(CHARS) for i in range(chars)]
    if isExactly:
        password += [choice(LOWERCASE) for i in range(length - len(password))]
    else:
        password += [choice(ALL) for i in range(length - len(password))]
    shuffle(password)
    password = "".join(password)
    return password

def removeRestricted(word, notAllowed): ###DELETES RESTRICTED LETTERS, NUMBERS, AND CAPITALS FROM CONSTANDS DEFINED ABOVE
        for c in notAllowed:
            word = word.replace(c, "")
        return word
