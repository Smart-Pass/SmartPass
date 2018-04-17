'''
Main Window Module for 'SmartPass'
-----NOTES-----
DOWNLOAD OUR APP LOGO AND PUT IN SAME DIRECTORY AS CODE FOR BEST AESTHETICS: https://tinyurl.com/ydgyg4yg
'''
#=====IMPORTS=====#
import sys,os,csv,ctypes,shutil,subprocess
editor_directory=os.getcwd()
#ensures Tkinter imports correctly based on Python version (Python 2 and Python 3 import Tkinter with different names)

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory,askopenfilename
from tkinter.ttk import Progressbar
from accessFiles import add,read,delete,prioritize,wipeall
from accessFiles import FileHandler

#initialization code
user32=ctypes.windll.user32

#=====FUNCTION DEFINITIONS=====#
def windowSetup(root): #takes all the attributes common to all windows and applies it to the window root (TK Window object)
    root.attributes('-topmost',True)
    root.attributes('-topmost',False)
    root.focus_force()
    try:root.wm_iconbitmap(os.path.join(editor_directory,'logo.ico')) #icon created by me in Adobe Photoshop CC 2018
    except: pass
    
def configGrid(root,rows,columns): #configures a grid
    for row in range(0,rows):
        root.rowconfigure(row,weight=1)
        for column in range(0,columns):
            root.columnconfigure(column,weight=1)
def getStrength(password): #password strength checker
    tally=0
    #check password length (15 characters is considered excellent)
    if len(password)>10: tally+=10
    else: tally+=round((len(password)/15)*10)
    #check for ratio of capital letters to lowercase letters
    pattern = r"[A-Z]"
    ratio=round(len(re.findall(pattern, password))/len(password))
    tally+=ratio*10
    #check for numbers
    pattern=r"[0-9]"
    tally+=len(re.findall(pattern, password))*2
    #check for special characters
    pattern=r"[^A-Za-z0-9]"
    tally+=len(re.findall(pattern, password))*5
    return tally

         
def about_menu(selector): #handles all functions related to the "About" menu; arg 'selector' specifies which of the 3 menu options were selected
    aboutWindow=Tk()
    def manage_about(*event):
        aboutWindow.destroy()
        try: aboutmenu.entryconfig(("About the Software" if selector==1 else "Updates" if selector==2 else "Help"),state="normal") 
        except: pass #Tells program not to worry about the main menu if user has closed that before closing the About window.
    aboutWindow.title("About the Software" if selector==1
                      else "Software Updates" if selector==2 else "Help")
    aboutWindow.geometry('1000x400')
    #setting directory and opening .txt file
    try: text=open(os.path.join(editor_directory,('about.txt'if selector==1 else 'updates.txt' if selector==2 else 'help.txt'))).read()#try to open About.txt
    except: #if file not found . . . .
        messagebox.showerror("Error","'about.txt' file is not found") #throw error message window
        try: aboutWindow.destroy() #After user has acknowledged the error, attempt to destroy the window
        except: pass #If the user has already destroyed the window, do nothing
    try: #if the txt file has been found and the window is not destroyed, run the following code
        textbox=Text(aboutWindow,height=24,width=117)
        textbox.pack()
        textbox.insert(END,str(text))
        textbox.configure(state='disabled')
        windowSetup(aboutWindow)
        aboutWindow.resizable(False,False)
        aboutWindow.protocol("WM_DELETE_WINDOW",manage_about) #wait for "window deleted" protocol, and when recieved, run manage_about()
        aboutWindow.bind('<Escape>',manage_about)
        aboutWindow.mainloop()
    except: aboutmenu.entryconfig(("About the Software" if selector==1 else "Updates" if selector==2 else "Help"),state='normal') #otherwise, reset the "About" Menu button and move on.
#when received, call about_menu() to open the right window (done for abstraction and because arguments cannot be passed through button commands)


def new_login(edit=False,fillers=None): #lets user save a new login to the data file
    createWindow=Tk()
    priority=IntVar(createWindow)
    b_new_login.config(state='disabled')
    b_access_login.config(state='disabled')
    def destroy_window(*event): #handles events that occur when window is to be destroyed
        createWindow.destroy()
        try:
            b_new_login.config(state='normal')
            b_access_login.config(state='normal')
        except: pass
    def register(*event): #register/save the login to the data file
        description=str(e_description.get())
        passed=True #tracks whether the description passes the "doesnt already exist" test
        if len(str(description))>0 and len(description)>0 and len(str(e_password.get()))>0: #checks to see if all fields are filled in
            for i in range(int(read()[1])): #check if entered description already exists
                if str(read()[0][i][0])!=description or edit==True: #if itereated description mathces what the user entered...
                    pass
                else:
                    l_descf.configure(text="Description already exists")
                    l_descf.grid()
                    passed=False #mark as fail if description already exists
                    break
            if passed==True: #only register if passed test
                if edit==True: delete(description==fillers[0])
                l_descf.grid_remove()
                add(str(e_description.get()),str(e_username.get()),str(e_password.get())) #add() function written by my partner (encrypts and writes the information to data file)
                if priority.get()==1: prioritize(description=str(e_description.get())) #prioritize() function written by my partner (puts the login as first item of aggregator)
                destroy_window()
                if edit==True: access_login()
        else:
            if len(str(e_description.get()))==0:
                l_descf.configure(text="*Required Field")
                l_descf.grid()
            else: l_descf.grid_remove()
            if len(str(e_username.get()))==0: l_userf.grid()
            else: l_descf.grid_remove()
            if len(str(e_password.get()))==0: l_passf.grid()
            else: l_passf.grid_remove()
    createWindow.title("Save a New Login" if edit==False else "Edit a Login")
    createWindow.geometry(str(int(user32.GetSystemMetrics(0)/3))+'x'+str(int(user32.GetSystemMetrics(1)/3))) #sets screen size to a third of the monitor size
    windowSetup(createWindow)
    configGrid(createWindow,5,2)
    Label(createWindow,text="Save a Login" if edit==False else "Edit a Login",font=("Times New Roman",25)).grid(row=0,column=0,columnspan=3,padx=10,pady=0,sticky="W")
    Label(createWindow,text="Description:",font=("Calibri")).grid(row=1,column=0,sticky='W',padx=20)
    Label(createWindow,text="Username/Email:",font=("Calibri")).grid(row=2,column=0,sticky='W',padx=20)
    Label(createWindow,text="Password:",font=("Calibri")).grid(row=3,column=0,sticky='W',padx=20)
    e_description=Entry(createWindow,width=40)
    e_description.grid(row=1,column=1,sticky='W')
    e_username=Entry(createWindow,width=40)
    e_username.grid(row=2,column=1,sticky='W')
    e_password=Entry(createWindow,width=40,show='*')
    e_password.grid(row=3,column=1,sticky='W')
    if edit==True:
        e_description.insert(0,fillers[0])
        e_username.insert(0,fillers[1])
        e_password.insert(0,fillers[2])
    b_showpassword=Button(createWindow,text="Show",width=5)
    b_showpassword.grid(row=3,column=1,sticky='E')
    def show(event):e_password.configure(show='')
    def hide(event):e_password.configure(show='*')
    b_showpassword.bind('<ButtonPress-1>',show)
    b_showpassword.bind('<ButtonRelease-1>',hide)
    c_prioritize=Checkbutton(createWindow,text="Prioritize (Most recent creation will have highest priority rank)",onvalue=1,offvalue=0,variable=priority)
    c_prioritize.grid(row=4,column=0,columnspan=3)
    l_descf=Label(createWindow,text="*Required Field",fg='red')
    l_descf.grid(row=1,column=2,sticky='W',padx=10)
    l_userf=Label(createWindow,text="*Required Field",fg='red')
    l_userf.grid(row=2,column=2,sticky='W',padx=10)
    l_passf=Label(createWindow,text="*Required Field",fg='red')
    l_passf.grid(row=3,column=2,sticky='W',padx=10)
    l_descf.grid_remove()
    l_userf.grid_remove()
    l_passf.grid_remove()
    Button(createWindow,text="OK",command=register,width=15).grid(row=5,column=1,sticky='E',padx=5,pady=10)
    Button(createWindow,text="Cancel",command=destroy_window,width=15).grid(row=5,column=2,sticky='W',padx=5,pady=10)
    createWindow.bind('<Return>',register)
    createWindow.bind('<Escape>',destroy_window)
    createWindow.resizable(False,False)
    createWindow.protocol("WM_DELETE_WINDOW",destroy_window)
    createWindow.mainloop()
    
def access_login(): #decrypts and displays all the user's logins in a file-directory like fashion
    desc=[] #list of descriptions ordered by priority
    abc=[] #list of descriptions ordered in abc order
    logins = read()[0]
    for login in logins:
        desc.append(login[0])
        abc.append(login[0])
    abc.sort()
    #create GUI Window
    accessWindow=Tk()
    configGrid(accessWindow,4,4)
    accessWindow.resizable(True,False)
    windowSetup(accessWindow)
    accessWindow.title("Access My Logins")
    accessWindow.geometry('1060x575')
    listmode=IntVar(accessWindow)
    listmode.set(1) #settings default to sorting data by priority 
    topLayer=Frame(accessWindow)
    topLayer.grid(row=0,rowspan=2,column=0,columnspan=5,sticky="NESW")
    configGrid(topLayer,2,5)
    canvas=Canvas(accessWindow)                              
    b_access_login.config(state='disabled')                   
    b_new_login.config(state='disabled')
    def destroy_window(*event): #function for handling window killing event
        accessWindow.destroy()
        try:
            b_access_login.config(state='normal')
            b_new_login.config(state='normal')
        except: pass
    def i_delete(data,index):
        result=messagebox.askyesno("Delete this login?","Are you sure you want to delete the following login?\nDescription: "+str(data[index]))
        if result==True:
            delete(description=str(data[index]))
            destroy_window()
            access_login()
        else:
            pass
    def i_edit(data,index):
        fillers=[
            str(data[index]),
            str(read(description=data[index])[1]),
            str(read(description=data[index])[2]),
            ]
        destroy_window()
        new_login(edit=True,fillers=fillers)
    def populate(frame,data): #populates the scroll frame with login data from the data file
        choice=StringVar(frame)
        for widget in frame.winfo_children(): widget.destroy() #clears the frame before populating it
        if len(data)>0:
            b_deleteall.configure(state='normal')
            x=1
            for login in data:
                description=str(login)
                username=str(read(description=login)[1])
                password=str(read(description=login)[2])
                strength=getStrength(str(password))
                strengthlevel="Strong" if strength >= 21 else "Fair" if 11<strength<21 else "Weak" if strength<=11 else None
                Label(frame,text=str(data.index(login)+1),width=5,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=0)
                Label(frame,text=description if len(description)<44 else description[:44]+' ...',width=40,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=1)
                Label(frame,text=username if len(username)<44 else username[:44]+' ...',width=40,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=2)
                Label(frame,text=password if len(password)<29 else password[:29]+' ...',width=30,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=3)
                Label(frame,text=strengthlevel,width=15,
                    bg="light grey" if x==1 else "white",
                    fg='dark green' if strengthlevel=="Strong" else 'orange' if strengthlevel=="Fair" else 'red',
                    anchor='w').grid(row=data.index(login),column=4,sticky='EW')
                
                b_edit=Button(frame,text="Edit",command=lambda i=data.index(login): i_edit(data=data,index=i))
                b_edit.grid(row=data.index(login),column=5)
                b_close=Button(frame,text='X',command=lambda i=data.index(login): i_delete(data=data,index=i),width=2)
                b_close.grid(row=data.index(login),column=6,padx=3,pady=3 if x==0 else 0)
                x=1 if x==0 else 0
        else:
            b_deleteall.configure(state='disabled')
            Label(frame,text="No Saved Logins" if len(desc)==0 else "No Results",font=("Calibri",15),anchor=CENTER,width=90,bg='light grey').grid(row=0,columnspan=5,sticky='EW')
        l_results.config(text="Results: "+str(len(data)))
    def configureFrame(canvas): #configures the canvas
        canvas.configure(scrollregion=canvas.bbox("all")) #CODE FROM http://effbot.org/tkinterbook/canvas.htm
    #display logins
    display=Frame(accessWindow,width=550,height=225)
    display.grid(row=3,column=0,columnspan=5,sticky="NSEW",padx=20)
    configGrid(display,0,6)
    scroll=Scrollbar(accessWindow,orient="vertical",command=canvas.yview)
    scroll.grid(row=2,column=4,sticky="NSE",padx=20)
    canvas.configure(yscrollcommand=scroll.set)
    def mousewheel(event):canvas.yview_scroll(int(-1*(event.delta/120)),"units") #CODE FROM https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar/37858368
    canvas.bind_all("<MouseWheel>",mousewheel)
    display.bind("<Configure>", lambda event, canvas=canvas: configureFrame(canvas))
   
    canvas.create_window((4,4),window=display) #code from https://stackoverflow.com/questions/29319445/tkinter-how-to-get-frame-in-canvas-window-to-expand-to-the-size-of-the-canvas
    
    Label(topLayer,text="Access My Logins",font=("Times New Roman",25)).grid(row=0,columnspan=10,padx=10,pady=10,sticky="NW")
    #Listing all data ordered either by priority or abc order
    r_priority=Radiobutton(topLayer,text="Sort all by\nPriority",variable=listmode,value=1,command=lambda:populate(frame=display,data=desc))
    r_priority.grid(row=1,column=3,sticky='E')
    r_abc=Radiobutton(topLayer,text="Sort all\nAlphabetically",variable=listmode,value=2,command=lambda:populate(frame=display,data=abc))
    r_abc.grid(row=1,column=4)
    #Listing results of a search
    def search(*event):
        listmode.set(0)
        searchdata=[]
        if len(str(e_search.get()))!=0:
            for login in desc:
                if str(e_search.get()).lower() in login.lower(): searchdata.append(login)
            populate(frame=display,data=searchdata)    
    l_search=Label(topLayer,text="Search: ",font=("Calibri"))
    l_search.grid(row=1,column=0,sticky='E',padx=10)
    e_search=Entry(topLayer,width=100)
    e_search.grid(row=1,column=1,sticky='EW')
    b_search=Button(topLayer,text="Search",command=search,width=7)
    b_search.grid(row=1,column=2,sticky='W')
    accessWindow.bind("<Return>",search)
    
    #labels
    labels=Frame(topLayer) #new fram topLayer
    labels.grid(row=2,column=0,columnspan=5,sticky="NEW",padx=20)
    configGrid(labels,0,4)
    Label(labels,text="#",width=5,anchor='w').grid(row=0,column=0)
    Label(labels,text="Description",width=40,anchor='w').grid(row=0,column=1)
    Label(labels,text="Username/Email",width=40,anchor='w').grid(row=0,column=2)
    Label(labels,text="Password",width=30,anchor='w').grid(row=0,column=3)
    Label(labels,text="Password\nStrength",width=9,anchor='w').grid(row=0,column=4)
    #bottom layer (close button and options to delete all logins button)
    def verifydelete():
        b_deleteall.configure(state="disabled")
        result=messagebox.askyesno("Delete All?","Are you sure you want to wipe all of your saved logins?")
        if result==True:
            delete()
            try:destroy_window()
            except: pass
        else: 
            try:b_deleteall.configure(state="normal")
            except: pass
    bottom=Frame(accessWindow)
    bottom.grid(row=3,column=0,columnspan=5,sticky="NSEW")
    configGrid(bottom,0,4)
    Button(bottom,text="Close",command=destroy_window,width=10).grid(padx=10,pady=20,row=0,column=4)
    b_deleteall=Button(bottom,text="Delete All",command=verifydelete,width=10)
    b_deleteall.grid(pady=20,row=0,column=3)
    l_results=Label(bottom)
    l_results.grid(row=0,column=0,padx=20)
    load=Frame(bottom,width=750)
    load.grid(row=0,column=1,columnspan=2)
    progress=Progressbar(load,orient=HORIZONTAL,length=500,mode='determinate')
    progress.grid(row=0,column=1)
    l_loading=Label(load,text='Loading...',anchor='w',width=35)
    l_loading.grid(row=0,column=2)
    progress.grid_remove() 
    l_loading.grid_remove() 
    canvas.grid(row=2,column=0,columnspan=5,sticky="NSEW",padx=20)
    topLayer.tkraise()
    labels.tkraise()
    bottom.tkraise()
    populate(frame=display,data=desc)#initialize window with priority sorted data
    accessWindow.protocol("WM_DELETE_WINDOW",destroy_window)
    accessWindow.bind('<Escape>',destroy_window)
    accessWindow.mainloop()
    
def wipe(): #deletes all files/directories created by this program
    mainWindow.withdraw()
    result=messagebox.askyesno("Reset the Application?",
                               '''Are you sure you want to wipe all data?\nThis will perform a \"Factory Reset\" on this Application.
                               All app data will be lost\n(This will not uninstall the application)''')
    if result==True:
        messagebox.showwarning("Warning","For this action to execute successfully, please close File Explorer (Windows) or Finder (Mac)")
        FileHandler.makeVincible() #FileHandler class created by my partner
        shutil.rmtree(r'C:\SmartPass')
        os._exit(1)
    else: mainWindow.deiconify()
def importExport(option): #allows user to import/export the data file for cross device usage.
    mainWindow.withdraw()
    def destroy_window(*event): #handles window killing event
        mainWindow.deiconify()
        ie.destroy()
    bindirectory='C:\\SmartPass\\bin'
    source=r'C:\SmartPass\bin\SmartPassLoginInformation.csv'
    ie=Tk()
    ie.title("Copy Data File")
    windowSetup(ie)
    ie.geometry('650x275')
    ie.resizable(False,False)
    configGrid(ie,3,2)
    def copyfile(newdir): #copy the data to directory specified by user
        FileHandler.makeVincible(isHidden=True) #FileHandler class created by my partner; allows csv file to be moved
        shutil.copy(source,newdir)
        FileHandler.makeInvincible() #FileHandler class created by my partner
        destroy_window()
    def importfile(directory): #import the data file from directory specified by user
        try:
            FileHandler.makeVincible() #FileHandler class created by my partner
            os.remove(source)
        except: pass
        shutil.move(directory,bindirectory)
        FileHandler.makeInvincible() #FileHandler class created by my partner; disables all actions done to csv file
        destroy_window()
    def dialog(): #creates a GUI file dialog for a more user friendly way of finding a directory
        ie.withdraw()
        f_dir=filedialog.askdirectory() if option==1 else filedialog.askopenfilename(filetypes=[('SmartPassLoginInformation.csv','SmartPassLoginInformation.csv')]) #only file that will show up in search
        ie.deiconify()
        e_location.configure(state='normal')
        e_location.delete(0,END)
        e_location.insert(0,f_dir)
        e_location.configure(state='disabled')
        if len(str(e_location.get()))!=0:
            Button(ie,
                   text='Copy' if option==1 else 'Import',width=10,
                   command=lambda:copyfile(f_dir) if option==1 else importfile(f_dir)).grid(row=4,column=1,pady=10)
    Label(ie,text="Export Copy of Data File" if option==1 else "Import Data File",font=("Times New Roman",23)).grid(row=0,column=0,columnspan=2,padx=20,pady=10,sticky='NW')
    Label(ie,text='''This will place a copy of the data file into a specified destination.
          \nWe recommend saving the copy file to a flash drive and importing it using our software on another device.
          \nPlease select the destination folder in which to copy the data file.''' if option==1
          else '''Please locate the data file named "con.csv"
          \nThe file should be where you have previously saved it with this software on another device
          \nImporting a data file will overwrite all data previously saved by this device.''',
          font=("Calibri",10),anchor=CENTER).grid(row=1,column=0,columnspan=3,padx=20)
    e_location=Entry(ie,width=50,state='disabled')
    e_location.grid(row=3,column=0,sticky='E',pady=10)
    Button(ie,text='...',command=dialog).grid(row=3,column=1,sticky='W',pady=10)
    Button(ie,text='Cancel',command=destroy_window,width=10).grid(row=4,column=2,padx=5,pady=10)
    ie.protocol("WM_DELETE_WINDOW",destroy_window)
    ie.bind('<Escape>',destroy_window)
    ie.mainloop()
def deletefiles(): #gives user option to delete individual files (user info file or data file) [This is primarily used for testing purposes]
    fdelete=Tk()
    mainWindow.withdraw()
    def destroy_window(*event): #handles file killing event
        mainWindow.deiconify()
        fdelete.destroy()
    def execute(*event): #perform the action of deleting the files
        f_data=r'C:\SmartPass\bin\SmartPassLoginInformation.csv'
        result=messagebox.askyesno("Delete Selected Files?","Are you sure you want to delete these files?")
        if result==True:
            if v_loginf.get()==1:
                try: os.remove(r'C:\SmartPass\bin\~$uildf.txt')
                except: pass
            if v_dataf.get()==1:
                try:
                    FileHandler.makeVincible() #FileHandler class created by my partner (makes file movable)
                    os.remove(f_data)
                except: pass
        else: pass
        destroy_window()
    v_loginf=IntVar(fdelete)
    v_dataf=IntVar(fdelete)
    fdelete.title("Delete Files")
    windowSetup(fdelete)
    fdelete.geometry('350x150')
    fdelete.resizable(False,False)
    configGrid(fdelete,2,2)
    Label(fdelete,text='Delete Files',font=('Times New Roman',22)).grid(columnspan=2,padx=20,pady=10,sticky='NW')
    c_loginf=Checkbutton(fdelete,text="Info File \n('~$uildf.txt')",onvalue=1,offvalue=0,variable=v_loginf)
    c_loginf.grid(row=1,column=0,padx=5)
    c_dataf=Checkbutton(fdelete,text="Data File \n(File containing all login data)",onvalue=1,offvalue=0,variable=v_dataf)
    c_dataf.grid(row=1,column=1,padx=5,columnspan=2)
    Button(fdelete,text="Cancel",width=10,command=destroy_window).grid(row=2,column=2,padx=10,pady=10)
    Button(fdelete,text="Delete Files",width=10,command=execute).grid(row=2,column=1,pady=10,sticky='E')
    fdelete.mainloop()
    
#=====MAIN CODE=====#

mainWindow=Tk()

#variable declarations
t_resizable = IntVar(mainWindow)
t_resizable.set(0)

mainWindow.resizable(bool(t_resizable.get()),bool(t_resizable.get())) #update screen after default variables are set

#configures a 4x4 grid

configGrid(mainWindow,4,4) #function declared in setup.py
    
#Header and Version Info
version="SmartPass v1.0" #Any updates to name or version here will update everything else in the program
mainWindow.title(version)
mainWindow.geometry(str(int(user32.GetSystemMetrics(0)/3))+'x'+str(int(user32.GetSystemMetrics(1)/3))) #sets screen size to a third of the monitor size
welcomeLabel=Label(mainWindow,text=("Welcome to "+version),font=("Times New Roman",24)).grid(row=0,columnspan=5)
versionLabel=Label(mainWindow,text=version).grid(row=4,column=4)

#menu bar
menubar=Menu(mainWindow)

filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="Wipe All Data",command=wipe)
filemenu.add_command(label="Delete Files",command=deletefiles)
filemenu.add_separator()
filemenu.add_command(label="Export Copy of Logins Data File",command=lambda:importExport(1))
filemenu.add_command(label="Import Logins from Existing File",command=lambda:importExport(2))
menubar.add_cascade(label="File",menu=filemenu)

optionsmenu=Menu(menubar,tearoff=0)
optionsmenu.add_checkbutton(label="Screen Resizable",onvalue=1,offvalue=0,variable=t_resizable,command=lambda: mainWindow.resizable(bool(t_resizable.get()),bool(t_resizable.get())))
optionsmenu.add_command(label="Reset Default Screen Size",command=lambda: mainWindow.geometry(str(int(user32.GetSystemMetrics(0)/3))+'x'+str(int(user32.GetSystemMetrics(1)/3))))
menubar.add_cascade(label="Options",menu=optionsmenu)


aboutmenu=Menu(menubar,tearoff=0)
aboutmenu.add_command(label="About the Software",command=lambda:[about_menu(selector=1),aboutmenu.entryconfig("About the Software",state='disabled')]) #FEATURES,FUNCTION,ETC. OF SOFTWARE
aboutmenu.add_command(label="Updates",command=lambda:[about_menu(selector=2),aboutmenu.entryconfig("Updates",state='disabled')]) #UPDATES
aboutmenu.add_separator()
aboutmenu.add_command(label="Help",command=lambda:[about_menu(selector=3),aboutmenu.entryconfig("Help",state='disabled')]) # TROUBLESHOOTING, HOW TO USE
menubar.add_cascade(label="About",menu=aboutmenu)

mainWindow.config(menu=menubar)

#buttons
b_new_login=Button(mainWindow,text="Save New Login",command=new_login)
b_new_login.grid(row=1,columnspan=5,sticky="NWSE",padx=50) 
b_access_login=Button(mainWindow,text="Access My Logins",command=access_login)
b_access_login.grid(row=2,columnspan=5,sticky="NWSE",padx=50,pady=10)

windowSetup(mainWindow)
mainWindow.protocol("WM_DELETE_WINDOW",lambda:os._exit(1))
mainWindow.mainloop()

