'''
File Management module for SmartPass
'''
from datetime import datetime
import subprocess
import os
import shutil
import csv
#from encrypterAndDecrypter import encrypt, decrypt
from tempEncrypterAndDecrypter import encrypt, decrypt

class FileProperties(): ###HOLDS FILE PROPERTIES LIKE HIDING AND SHOWING FILE
    
    @staticmethod
    def hideFile(filename): ###SETS ATTRIBUTES TO HIDDEN AND READ-ONLY
        subprocess.call("attrib +r +h " + filename)
    
    @staticmethod
    def showFile(filename): ###SETS ATTRIBUTES TO SHOWING AND READ AND WRITE
        subprocess.call("attrib -r -h " + filename)

class CSVHandler(): ###DOES EVERYTHING WITH THE CSV FILE
    
    def __init__(self): ###INTIALIZE VARIABLE FILENAME AND DATA
        os.chdir("C:\\")
        self.dirname = r"C:\SmartPass\bin"
        self.filename = self.dirname + r"\SmartPassLoginInformation.csv"
        CSVHandler.filename = self.filename
        self.secret_dirname = "\\"+ "\\" + ".\\" + r"C:\SmartPass\bin"
        self.secret_filename = self.secret_dirname + r"\con.csv"
        CSVHandler.secret_filename = self.secret_filename
        self.data = []
        if os.path.isfile(self.secret_filename) == os.path.isfile(self.filename) == False: ###this notation is needed to ensure that files aren't being made every single time an object for the class is made
            subprocess.call("mkdir " + self.secret_dirname, shell=True)
            with open(self.secret_filename, "w") as f: FileProperties.hideFile(self.secret_filename)
    
    def adder(self, description, username, password): ###ADDS TO FILE  
        self.description = description
        self.username = username
        self.password = password
        self.dateStamp = str(datetime.now().date().month) + "/" + str(datetime.now().date().day) + "/" + str(datetime.now().date().year) + " (" + str(datetime.now().time()) + ")"
        
        passwords = self.grabEverything() ###ADDS WHATEVER IS IN CSV FILE RIGHT NOW TO DATA, THEN ADDS NEW ENCRYPTED PASSWORD TO DATA AS WELL  
        for element in passwords: self.data.append([encrypt(element[0]), encrypt(element[1]), encrypt(element[2]), encrypt(element[3])]) #$encrypt(element[3])$#
        self.data.append([encrypt(description), encrypt(username), encrypt(password), encrypt(self.dateStamp)]) #$encrypt(self.dateStamp)$#

        self.write()
        
    def reader(self, line, description): ###READS WHOLE CSV FILE; IF LINE IS SPECIFIED AS SOMETHING OTHER THAN NONE, JUST READS PASSWORD CONTAINED IN THAT LINE
        with open(self.secret_filename, "r") as f:
            reader = csv.reader(f)
            i = 0
            if description == None and line == None:
                passwords = []
                for row in reader:
                    if row == []: continue ###without this, csv file would make unecessary and random empty rows 
                    else:
                        passwords.append([decrypt(row[0][2:-1].encode()), decrypt(row[1][2:-1].encode()), decrypt(row[2][2:-1].encode()), decrypt(row[3][2:12].encode())]) #$$#
                        i += 1
                return passwords, i
            elif line != None: ###if line has an value other than None, read that specific line
                for row in reader:
                    i += 1
                    if line == i:
                        return [decrypt(row[0][2:-1].encode()), decrypt(row[1][2:-1].encode()), decrypt(row[2][2:-1].encode()), decrypt(row[3][2:12].encode())] ###[2:-1] gets rid of b' in beginning and ' in end. [2:12] gets rid of time login was created
            elif description != None: ###if description has a value other than None, read from that description
                elements = []
                passwords = self.reader(None, None)[0]
                for element in passwords:
                    if description == element[0]:
                        elements.append(element)
                return elements #$$returns a list, not a single description$$#
            
            else: raise ValueError("Arguments not inputted correctly") ###if for some reason none of the above statements are called, raise this error
    
    def deleter(self, line, description, username, password): ###DELETES EVERYTHING ON CSV FILE; IF LINE IS SPECIFIED AS SOMETHING OTHER THAN NONE, JUST DELETES PASSWORD CONTAINED IN THAT LINE; IF PASSWORD IS SPECIFIED AS SOMETHING OTHER THAN NONE, JUST DELETES PASSWORD
        passwords = self.grabEverything()
        if line == description == username == password == None: passwords = [] ###if no arguments specified, delete everything
        elif line != None: del passwords[line-1] ###delete the line specified
        elif description != None: ###look for the description and delete 
            for element in passwords:
                if description == element[0]:
                    passwords.remove(element)
        elif username != None: ###look for the username and delete
            for element in passwords:
                if username == element[1]:
                    passwords.remove(element)
        elif password != None: ###look for the password and delete
            for element in passwords:
                if password == element[2]:
                    passwords.remove(element)
        else: raise ValueError("Arguments not inputted correctly") ###if not going through if statements, arguments aren't inputted correctly
        
        for password in passwords: self.data.append([encrypt(password[0]), encrypt(password[1]), encrypt(password[2]), encrypt(password[3])]) ###REWRITES FILE WITH NEW DATA
        
        self.write()
        
    def prioritizer(self, line, description, username, password): ###ALLOWS FOR A SPECIFIC LINE, DESCRIPTION, USERNAME, OR PASSWORD TO BE PRIORITIZED TO BE AT THE TOP OF THE LIST
        passwords = self.reader(None, None)[0]
        if line != None: ###prioritize based on line number
          starred = passwords.pop(line-1)
          passwords.insert(0, starred)
        elif description != None: ###prioritize based on description
            i = 0
            for element in passwords:
                i += 1
                if description == element[0]: passwords.insert(0, passwords.pop(i-1))
        elif username != None: ###prioritize based on username
            i = 0
            for element in passwords:
                i += 1
                if username == element[1]: passwords.insert(0, passwords.pop(i-1))
        elif password != None: ###prioritize based on password
            i = 0
            for element in passwords:
                i += 1
                if password == element[2]: passwords.insert(0, passwords.pop(i-1))
        else: raise ValueError("Arguments not inputted correctly (One argument must be equal to something other than None)") ###all aruments are equal to None, which can't happen, so error is raised
          
        for password in passwords: self.data.append([encrypt(password[0]), encrypt(password[1]), encrypt(password[2]), encrypt(password[3])]) ###REWRITES FILE WITH NEW DATA

        self.write()

    def sorter(self, description, username, password, dateStamp, isIncreasing): ###SORTS LOGINS ACCORDING TO WHICHEVER PARAMETER IS TRUE. ISINCREASING REVERSES SORT DEPENDING ON ITS BOOLEAN VALUE
        passwords = self.grabEverything()

        def descriptionSort(): ###sort by description in alphabetical order
            descriptions = []
            for arr in passwords:
                descriptions.append(arr[0]) ###pull out descriptions out of each login
            sortedDescriptions = sorted(descriptions, reverse=not(isIncreasing))
            for description in sortedDescriptions:
                for i in range(len(descriptions)):
                    if description == descriptions[i]:
                        self.data.append([encrypt(passwords[i][0]), encrypt(passwords[i][1]), encrypt(passwords[i][2]), encrypt(passwords[i][3])])
                        del descriptions[i]
                        del passwords[i]
                        break

        def dateSort(): ###sort by the dates each login information was created
            dateStamps = []
            for arr in passwords:
                dateStamps.append(arr[3]) ###pull out only dates out of each login
            sortedStamps = sorted(dateStamps, key = lambda date: datetime.strptime(date, "%m/%d/%Y (%H:%M:%S.%f)"), reverse=not(isIncreasing)) ###sort each date and assign to new variable
            for stamp in sortedStamps: ###use sorted list and unsorted list to get index of date in old list, grab index of login from original list, then sort and assign to self.data
                for i in range(len(dateStamps)):
                    if stamp == dateStamps[i]:
                        self.data.append([encrypt(passwords[i][0]), encrypt(passwords[i][1]), encrypt(passwords[i][2]), encrypt(passwords[i][3])])

        if description: descriptionSort()
        elif dateStamp: dateSort()
        self.write()

    def write(self): ###IS USED TO ACTUALLY WRITE EACH CSV FILE. USED ONLY WITHIN THE CLASS
        FileProperties.showFile(self.secret_filename)
        with open(self.secret_filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data) ###rewrites csv file with data
        FileProperties.hideFile(self.secret_filename)

    def grabEverything(self): ###SIMILAR TO READER FUNCTION EXCEPT GRABS EVERY BIT OF DATA. USED ONLY WITHIN THE CLASS
        logins = []
        with open(self.secret_filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row == []: continue
                else:
                    logins.append([decrypt(row[0][2:-1].encode()), decrypt(row[1][2:-1].encode()), decrypt(row[2][2:-1].encode()), decrypt(row[3][2:-1].encode())])
        return logins
            
            
class FileHandler(CSVHandler): ###GIVES USER ACCESS TO FILE
    
    @staticmethod
    def deleteFolder(): ###FOR THE SAKE OF THE PROJECT, USER IS GIVEN OPTION TO DELETE FOLDER ONCE DONE WITH USING IT OR GRADING IT
        FileHandler.makeVincible(0)
        shutil.rmtree(r"C:\SmartPass")
        
    @staticmethod
    def makeVincible(isHidden=False): ###ALLOWS FRONTEND DEVELOPER TO MESS WITH FILE IF NEEDED
        handle = CSVHandler()
        FileProperties.showFile(CSVHandler.secret_filename)
        os.rename(CSVHandler.secret_filename, CSVHandler.filename)
        if isHidden == True:
            FileProperties.hideFile(CSVHandler.filename)
        
    @staticmethod
    def makeInvincible(isHidden=True): ###ONCE FRONTEND DEVELOPER IS DONE WITH THE FILE, IT BECOMES INVINCIBLE AGAIN
        handle = CSVHandler()
        FileProperties.showFile(CSVHandler.filename)
        os.rename(CSVHandler.filename, CSVHandler.secret_filename)
        if isHidden == True:
            FileProperties.hideFile(CSVHandler.secret_filename)

def add(description, username, password): ###CALLS ADDER FUNC
    handle = CSVHandler()
    return handle.adder(description, username, password)
    
def read(line=None, description=None): ### CALLS READER FUNC
    handle = CSVHandler()
    return handle.reader(line, description)

def delete(line=None, description=None, username=None, password=None): ###CALLS DELETER FUNC
    handle = CSVHandler()
    return handle.deleter(line, description, username, password)

def sort_(description=False, username=False, password=False, dateStamp=False, isLowerToHigher=True): ###CALLS SORTER FUNC
    handle = CSVHandler() 
    return handle.sorter(description, username, password, dateStamp, isLowerToHigher)

def prioritize(line=None, description=None, username=None, password=None): ###CALLS PRIORITIZER FUNC
    handle = CSVHandler()
    return handle.prioritizer(line, description, username, password)
    
def wipeall(): FileHandler.deleteFolder() ###DELETES ALL DATA AND FOLDER DATA IS STORED IN, USEFUL FOR WHEN USER IS DELETING APP

