'''
setup module for 'SmartPass'
-----NOTES-----
This module is the backbone module, meaning when run, it will call any other 
libraries/modules necessary for a successful run of the project.
DOWNLOAD OUR APP LOGO AND PUT IN SAME DIRECTORY AS CODE FOR BEST AESTHETICS: https://tinyurl.com/ydgyg4yg
'''
import sys,os,shutil

from encrypterAndDecrypter import encrypt,decrypt


from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
#DEFINE VARIABLES
qchoices={"What primary/elementray school did you attend?",
          "Which teacher gave you your first failing grade?",
          "What city were you born in?",
          "What kind of music do you like best?",
          "How many pets did you own?",
          "What is your favorite sports team?"} #dictionary containing the security questions

#DEFINE FUNCTIONS
def windowSetup(root): #takes attributes common to all windows and applies it to root, an argument passed as a Tk Window Object
    root.attributes('-topmost',True)
    root.attributes('-topmost',False)
    root.focus_force()
    try:root.wm_iconbitmap('logo.ico') #icon created by me in Adobe Photoshop CC 2018
    except: pass
    
def startMainSequence(): import main #starts the actual application after setup and login is complete

def end(*event): os._exit(1) #function that handles program killing; 1 *arg parameter for keyboard binding

def configGrid(root,n_grid): #configures a square array of n_grid size in the window specified by the first parameter root
    count=0
    while count<n_grid:
        root.rowconfigure(count, weight=1)
        root.columnconfigure(count, weight=1)
        count += 1
        
def createLogin(): #allows user to set up security question login if they are new to the program
    create=Tk()
    agree=IntVar(create)
    def close(*event): #handles events that occur upon closing of this window
        def killfile(): #remove the user info file as login creation was interrupted 
            try: os.remove("~$uildf.txt")
            except: pass
        create.withdraw()
        result=messagebox.askyesno("Quit?","Are you sure you want to quit?\nAll data saved to this point will be lost")
        if result==True:
            killfile()
            end()
        else: create.deiconify()
        
    def save(*event): #encrypt and save the information to the user info file
        if len(e_answer.get())>0 and question.get()!="Choose a security question" and e_answer.get()!="Answer" and agree.get()==1:
            f_info=open(os.path.join(bindirectory,"~$uildf.txt"),'w')
            f_info.write(str(encrypt(question.get()))[2:]+'\n') #encrypt() function created by my partner
            f_info.write(str(encrypt(e_answer.get()))[2:]+'\n')
            f_info.close()
        else:
            create.withdraw()
            messagebox.showerror("Error","Please provide an answer to all fields")
            create.deiconify()
    question=StringVar(create)
    question.set("Choose a security question")
    create.title("Create a Login")
    create.geometry("375x210")
    Label(create,text="Let's get started by saving your login info.\nThis will be how you log in",font=("Times New Roman",12)).pack(pady=5)
    OptionMenu(create,question,*qchoices).pack(pady=5) # qchoices passed as an *arg allows for an infinite number of arguments to be passed (in most cases: dictionaries)
    e_answer=Entry(create,width=40)
    e_answer.pack()
    c_terms=Checkbutton(create,text="By checking this, I give this software permission to\ncreate indestructible files and directories on your computer.\nThese files can be deleted through the software.",onvalue=1,offvalue=0,variable=agree)
    c_terms.pack(pady=5)
    Button(create,text="Ok",width=15,command=lambda:[save(),create.destroy(),login()]).pack(side=RIGHT,padx=10)
    windowSetup(create)
    create.resizable(False,False)
    create.bind('<Escape>',close)
    create.bind('<Return>',save)
    create.protocol("WM_DELETE_WINDOW",close)
    create.mainloop()
    
def locateFile(): #ask user to locate the user information file if program cannot find it
    locate=Tk() 
    def findInfo(): #opens a file dialog for convenience in locating the file
        locate.withdraw()
        f_dir=filedialog.askopenfilename(filetypes=[('~$uildf.txt','~$uildf.txt')]) #the only file the user can select is the user info file.
        locate.deiconify()
        e_filepath.configure(state='normal')
        e_filepath.delete(0,END)
        e_filepath.insert(0,f_dir)
        e_filepath.configure(state='disabled')
        if len(e_filepath.get())!=0:
            Button(locate,text="Ok",command=lambda: [shutil.move(f_dir,"C:\\SmartPass\\bin"),locate.destroy(),mainsetup()]).grid(row=2,column=1,sticky='EW') #button only appears when file is found
            locate.bind('<Return>',lambda: [shutil.move(f_dir,"C:\\SmartPass\\bin"),locate.destroy(),mainsetup()])
    def cantFind(): #if user cannot locate file, prompt user to create new login
        b_cantfind.configure(state="disabled")
        b_locatefile.configure(state="disabled")
        result=messagebox.askyesno("Can't Find File","Without this file, the program cannot run properly.\nWould you like to reset?\n(Requires creation of new login; other data kept)")
        if result==True:
            locate.destroy()
            createLogin()
        else:
            b_cantfind.configure(state="normal")
            b_locatefile.configure(state="normal")
    configGrid(locate,4)
    locate.title('Locate File')
    locate.geometry('425x200')
    Label(locate,text="I am unable to locate a file needed by this software.\nMind locating that for me?",font=('Times New Roman',12)).grid(row=0,columnspan=5)
    e_filepath=Entry(locate,state='disabled')
    e_filepath.grid(row=1,column=1,columnspan=2,sticky="EW")
    b_locatefile=Button(locate,text="...",command=findInfo,width=2,height=1)
    b_locatefile.grid(row=1,column=3,sticky="W")
    b_cantfind=Button(locate,text="Can't Find It",command=cantFind)
    b_cantfind.grid(row=2,column=2,sticky='EW',padx=5)
    locate.protocol("WM_DELETE_WINDOW",end)
    locate.bind('<Escape>',end)
    locate.resizable(False,False)
    windowSetup(locate)
    locate.mainloop()
    
def newUser(): #if unable to find a user info file, ask user whether they are new
    result=messagebox.askyesno("New User?","Hello, There!\nAre you a new user?")
    if result==True:createLogin()
    else:locateFile()
    
def login(): #log the user in through answering the security question
    content=[]
    #read contents of the info file
    f=open(os.path.join(bindirectory,"~$uildf.txt"),'r')
    for line in f:
        content.append(line[:-2])
    f.close()
    #decrypt the content
    question=decrypt(str.encode(content[0])) #decrypt() function created by my partner
    answer=decrypt(str.encode(content[1]))
    wlogin=Tk()
    def verify(*event): #verify that answer provided by user matches the info saved upon set up
        if (e_uanswer.get()).lower()==str(answer).lower(): 
            wlogin.destroy()
            startMainSequence()
        else: l_incorrect.grid()
    wlogin.title('Login')
    windowSetup(wlogin)
    configGrid(wlogin,4)
    wlogin.geometry("425x200")
    Label(wlogin,text="Login",font=("Times New Roman",20)).grid(row=0,column=0,columnspan=5,sticky="W",padx=10)
    Label(wlogin,text=question,font=("Calibri",12)).grid(row=1,column=0,columnspan=5)
    e_uanswer=Entry(wlogin)
    e_uanswer.grid(row=2,column=0,columnspan=5,sticky="EW",padx=15)
    l_incorrect=Label(wlogin,text="Answer provided is incorrect.",fg="red")
    l_incorrect.grid(row=3,column=0,columnspan=5,)
    l_incorrect.grid_remove()
    Button(wlogin,text="Log In",command=verify,width=15).grid(row=4,column=3,pady=10)
    Button(wlogin,text="Quit",command=end,width=15).grid(row=4,column=4,pady=10,padx=5)
    wlogin.protocol("WM_DELETE_WINDOW",end)
    wlogin.bind('<Return>',verify)
    wlogin.bind('<Escape>',end)
    wlogin.mainloop()
def mainsetup(): #attempts to find the user info file 
    try:
        infofile=open(os.path.join(bindirectory,"~$uildf.txt"),'r') #uildf = "User Information and Login Details File
        infofile.close()
    except:
        newUser()
    login()
######MAIN CODE#######
editor_directory=os.getcwd() #set editor directory to current working directory
#attempt to create this directory if it does not exist already
try: os.mkdir('C:\\SmartPass')
except: pass
try:os.mkdir('C:\\SmartPass\\bin')
except: pass
bindirectory='C:\\SmartPass\\bin' #set bin directory to the directory that was just created
mainsetup() #run main setup defined above
       
        
