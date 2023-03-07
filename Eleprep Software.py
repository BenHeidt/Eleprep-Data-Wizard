from tkinter import * 
from PIL import ImageTk, Image
from tkinter import ttk 
from tkinter import messagebox
from PSEsPicoLib import *
import matplotlib
from matplotlib import pyplot as plt 
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time 
import pandas as pd 
import originpro as op
from tkinter import filedialog
import DAlib
# Imports for runMethod: 
import serial      
import os.path  
import PSEsPicoLib 
import matplotlib.pyplot as plt
import csv
import winsound

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def displayResults(enddata): 
    monitorWindow = Toplevel()
    monitorWindow.title("Data Plot")
    monitorWindow.iconbitmap("ui_graphics/Elepreplogosmall.ico")


def bugfixing():
    print("")




def safeData(enddata):

    eNumber = 0
    file = filedialog.asksaveasfile(defaultextension='.csv')
    

    for electrode in enddata:
        eNumber = eNumber+1
        print(' ')
        print(' ')
        print('Electrode '+str(eNumber) + ' Measurements:')

        file.write(' \n')
        file.write(' \n')
        file.write('Electrode '+str(eNumber) + ' Measurements: \n')

        #print(electrode)
        for measurement in electrode:
            print(measurement)
            measurement = str(measurement)
            measurement = measurement[1:-1]
            file.write(f"{measurement}\n")
    file.close()


def safeDatatoExcel(data, wPlot, lastload):

    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel Files', '*.xlsx')])

    print(file_path)

     
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    for i, sheet in enumerate(data):
        sheet.to_excel(writer, sheet_name = "Sheet "+str(i+1), index=False)

    writer.save()
    writer.close()

    if wPlot == None:
        pass

    else: 
        DAlib.safePlot(data, wPlot, file_path) 

    #Adds the method to the sheet, if the text was inserted by hand it uses the current_method file, if a method file was loaded it uses that one 

    if lastload == None:
      
        DAlib.safeMethodtoExcel(file_path, "used_methods/current_method.mscr")

    else: 
        DAlib.safeMethodtoExcel(file_path, lastload)



comport = "COM3"

def setcomport(useport):
    global comport
    comport = useport
    print("Comport set to: ")
    print(comport)


def safeMethod():
    
    getSettings()

        #Open the currentMethod file to safe somewhere else
    with open('used_methods/current_method.mscr', 'r') as file: 
        filedata = file.read()
    print("CurrentMethod Opened:")
    print(filedata)

    file = filedialog.asksaveasfile(defaultextension='.mscr')
    file.write(filedata)
    file.close()

#this value tells the program if a method was loaded or entered manually 
lastload = None

def openMethod():
    global lastload
    global frameStatus
    filepath = filedialog.askopenfilename(filetypes= [("Methodscript Files", ".mscr")])
    print(filepath)
    openLocationAndName = filepath.rsplit('/', 1 )
    print(openLocationAndName[0])
    print(openLocationAndName[1])
    runMethod(openLocationAndName[0],openLocationAndName[1])
    lastload = filepath
    statusChange("Done", "green")
    



root = Tk()
root.title("Eleprep Data Wizard")
root.iconbitmap("ui_graphics/Elepreplogosmall.ico")

#root.resizable(width=False, height=False)

#root.geometry("1200x800")

#Number Electrodes and Fields to be used 
nEle = 8
nFields = 10 
usedmethod = None

#for drawing the empty graph: 
applied_potential = []
measured_current = []

for i in range(nEle):
    applied_potential.append([])
    measured_current.append([])

nFieldsForMethods = {
        "ca" : 4,
        "cv" : 7,
        "eis" : 7,
        "lsv" : 4
    }


fieldDescription = {
        "ca" : [" ", "t equibrilation", "E dc", "t interval", "t run"],
        "cv" : [" ", "t equibrilation", "E begin", "E vertex 1", "E vertex 2", "E step", "Scan rate", "Number scans"],
        "eis": [" ","t equibrilation", "E dc", "E ac", "n frequencies", "Max. frequency", "Min. freqnency", "t Max. OCP"],
        "lsv": [" ","Lower Boundry", "Higher Boundry", "E step", "Scan rate"]
    }

choiceofblank = { 
        "ca" : "blank_methods\method_ca.mscr",
        "cv" : "blank_methods\method_cv.mscr",
        "eis" : "blank_methods\method_eis.mscr",
        "lsv" : "blank_methods\method_lsv.mscr"
}

#for sending data to origin, not yet working
def printToOrigin():
    wks = op.new_sheet()
    wks.from_list('A', applied_potential,"Applied Potential", "V", axis='x')
    wks.from_list('B', measured_current, "Measured Current", "A", axis="y")




#MENUES___________________________________________________________________________________________________

menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=fileMenu)
fileMenu.add_command(label='Save Method', command=safeMethod)
fileMenu.add_command(label='Open and Run Method', command=openMethod)
fileMenu.add_separator()
fileMenu.add_command(label='Safe Data (CSV)', command= lambda: safeData(enddata))

subMenu = Menu(fileMenu, tearoff = 0)
fileMenu.add_cascade(label = "Safe Data (Excel)", menu=subMenu)

subMenu.add_command(label='Data Only', command= lambda: safeDatatoExcel(dfenddata, None, lastload))
subMenu.add_command(label='Data with C/V Plot', command= lambda: safeDatatoExcel(dfenddata, "else", lastload))
subMenu.add_command(label='Data with Nyquist Plot', command= lambda: safeDatatoExcel(dfenddata, "eis", lastload))
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=quit)


#Multi electrode menue to change nEle settings, deacvtivated for now since running with less than 8 electrodes can cause problems 
'''eMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Electrodes', menu=eMenu)
eMenu.add_command(label='1 Electrode', command=lambda: chooseEle(1))
eMenu.add_command(label='2 Electrodes', command=lambda: chooseEle(2))
eMenu.add_command(label='3 Electrodes', command=lambda: chooseEle(3))
eMenu.add_command(label='4 Electrodes', command=lambda: chooseEle(4))
eMenu.add_command(label='5 Electrodes', command=lambda: chooseEle(5))
eMenu.add_command(label='6 Electrodes', command=lambda: chooseEle(6))
eMenu.add_command(label='7 Electrodes', command=lambda: chooseEle(7))
eMenu.add_command(label='8 Electrodes', command=lambda: chooseEle(8))'''

mMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Method', menu=mMenu)
mMenu.add_command(label='Chrono Amperometry', command=lambda: chooseMethod("ca"))
mMenu.add_command(label='Cyclic Voltametry', command=lambda: chooseMethod("cv"))
mMenu.add_command(label='Linear Sweep Voltametry', command=lambda: chooseMethod("lsv"))
mMenu.add_command(label='Electrochemica impeadance Analysis', command=lambda: chooseMethod("eis"))

cMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Ports', menu=cMenu)
cMenu.add_command(label='COM1', command=lambda: setcomport("COM1"))
cMenu.add_command(label='COM2', command=lambda: setcomport("COM2"))
cMenu.add_command(label='COM3', command=lambda: setcomport("COM3"))
cMenu.add_command(label='COM4', command=lambda: setcomport("COM4"))
cMenu.add_command(label='COM5', command=lambda: setcomport("COM5"))
cMenu.add_command(label='COM6', command=lambda: setcomport("COM6"))
cMenu.add_command(label='COM7', command=lambda: setcomport("COM7"))
cMenu.add_command(label='COM8', command=lambda: setcomport("COM8"))

rMenu = Menu(menubar, tearoff= 0)
menubar.add_cascade(label = 'Monitor', menu= rMenu)
rMenu.add_command(label = "Voltage vs. Current Plot", command =lambda: DAlib.plotResults(dfenddata, "others"))
rMenu.add_command(label = "Nyquist Plot", command =lambda: DAlib.plotResults(dfenddata, "eis"))

'''
bMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Developer Tools", menu = bMenu)
bMenu.add_command(label="Bugfix Function", command=bugfixing)
'''

#Create Base Frame Architecture: ____________________________________________________________________________________________________
#Frame Positions: 

frameHeaderPos={"row":0, "col":2}
frameElectrodesPos={"row":1, "col":2}
frameDescriptionPos={"row":1, "col":1}
frameButtonPos={"row":4,"col":2}
frameMonitorPos={"row":2, "col":2}
frameStatusPos={"row":3, "col":2}


frameHeader = LabelFrame(root,borderwidth=0, highlightthickness=0)
frameHeader.grid(row=frameHeaderPos["row"], column=frameHeaderPos["col"], pady=30)

frameDescription = LabelFrame(root, text = "Description")
frameDescription.grid(row=frameDescriptionPos["row"],column=frameDescriptionPos["col"])

frameElectrodes = LabelFrame(root, text="Electrodes", borderwidth=0,highlightthickness=0)
frameElectrodes.grid(row=frameElectrodesPos["row"],column=frameElectrodesPos["col"], padx=20, pady=20)

frameMonitor = LabelFrame(root, text= "Monitor")
frameMonitor.grid(row=frameMonitorPos["row"], column=frameMonitorPos["col"], pady = 15)

frameStatus = LabelFrame(root, text= "Status")
frameStatus.grid(row=frameStatusPos["row"], column=frameStatusPos["col"])

StatusLabel = Label(frameStatus, text = "Choosing Method")
StatusLabel.pack()

#create and pack Header
logobig = ImageTk.PhotoImage(Image.open("ui_graphics/Logobig.png"))
logolabel = Label(frameHeader,image=logobig)
logolabel.grid(row=0, column=0)



#Main part __________________________________________________________________________________________________________________________________

#set number of electrodes 
def chooseEle(ele):
    global nEle
    nEle = (ele)
    print("Electrode is set to: " + str(ele))
    createWindow()


#set number of input fields
def chooseMethod(met):
    global nFields
    global usedmethod

    usedmethod = met

    nFields = nFieldsForMethods[met]
    print("Method is set to: " + met)
    print("Number of Fields is therefore: " + str(nFields))
    createWindow()

#change the status text while running

def statusChange(status, color):
    global StatusLabel
    
    StatusLabel.destroy()
    StatusLabel = Label(frameStatus, text = status, fg = color)
    StatusLabel.pack()
 


def createWindow():

    #CREATING THE FRAMES 
    
    #destroy and recreate old frames to update information 
    global frameElectrodes
    global frameDescription
    global allColummns
    global frameMonitor
    global frameStatus
    global frameButton
    global applied_potential
    global measured_current

    frameElectrodes.destroy()
    frameDescription.destroy()

    frameDescription = LabelFrame(root, text = "Settings")
    frameDescription.grid(row=frameDescriptionPos["row"],column=frameDescriptionPos["col"], sticky='nsew')
    
    frameElectrodes = LabelFrame(root, text="Electrodes",borderwidth=0,highlightthickness=0)
    frameElectrodes.grid(row=frameElectrodesPos["row"],column=frameElectrodesPos["col"], padx=20)

     #Create Status 
    statusChange("Idle", "green")

    #placeholder item

    Label(text="    ").grid(row=1, column=0)
     #Label(text="   ").grid(row= frameElectrodesPos["row"]+1,pady=30)
 
    
    #create Frames #Pack Frames 

    allFrames=[]
    for i in range(nEle):
        allFrames.append(LabelFrame(frameElectrodes, text= "Electrode " + str(i+1)))
        allFrames[i].grid(row=0, column=i, padx=3)
        print("Frame Nummer " + str(i))

  
    #Create and Pack Entry Fields 
    allColummns = []
    for i in range(nEle):
        allColummns.append([])

    for n in range(nEle):
        for i in range(nFields):

            allColummns[n].append(Entry(allFrames[n], width=10))
            allColummns[n][i].grid(row=i, column = 1, pady=5, padx=25)

    
    #Create and pack field descriptions 
    for i in range(nFields+1):
        description = Label(frameDescription, text = fieldDescription[usedmethod][i], pady=4)
        description.grid(row=i,column =0)
        print(fieldDescription[usedmethod][i])
        print("in row: " + str(i))


    #Create and pack button to start measurement 
    frameButton = LabelFrame(root)
    frameButton.grid(row = frameButtonPos["row"], column= frameButtonPos["col"], pady=15)
    startButton = Button(frameButton, text="Start Measurement", command=buttonPress).pack()



# conducts the measurement
def runMethod(MSfilepath, MScriptFile):


    global dfenddata
    global enddata
    global frameMonitor
    
    #combine the path and filename 
    MScriptPathandFile = os.path.join(MSfilepath, MScriptFile)


    #initialization and open the port
    ser = serial.Serial()   #Create an instance of the serial object

    myport = comport                            #set the comport
    if PSEsPicoLib.OpenComport(ser,myport,1):   #open myport with 1 sec timeout
        print("Succesfuly opened: " + ser.port  )
        try:
            if PSEsPicoLib.IsConnected(ser):             #Check if EmstatPico is connected
                print("Connected!")                  
                
                # Send the MethodSCRIPT file
                PSEsPicoLib.SendScriptFile(ser,MScriptPathandFile)  

                #Change indicator to indicate running measurement
                statusChange("Running Method!", "red")
                root.update_idletasks()

                #Get the results and store it in datafile
                datafile=PSEsPicoLib.GetResults(ser)                             # fetch the results

                #Create "data" subfolder 
                (prefix, sep, suffix) = MScriptFile.rpartition('.')   #split the file-extension and the filename
                ResultFile = prefix + '.dat'                          #change the extension to .dat
                ResultPath = ".\data"                      #use subfolder for the data
                try:  
                    os.mkdir(ResultPath)
                except OSError:  
                    print ("Creation of the directory %s failed" % ResultPath)
                else:  
                    print ("Successfully created the directory %s " % ResultPath)

                                   
                ResultFile = os.path.join(ResultPath, ResultFile)                #combine the path and the filename
                ResultFile = PSEsPicoLib.CheckFileExistAndRename(ResultFile)     #Rename the file if it exists to a unique name by add the date+time 
                print("Resultfile: " + ResultFile)       
                f = open(ResultFile,"w+")    #Open file for writing
                f.write(datafile)            #write data to file
                f.close()                    #close file
            else:
                print("Unable to connected!")                  
        except Exception as e1:                         #catch exception 
                print("error communicating...: " + str(e1)) #print the exception
        finally:
            ser.close()                                  #close the comport
    else:
        print("cannot open serial port ")


    value_matrix = PSEsPicoLib.ParseResultFile(ResultFile)  #Parse result file to Value matrix
    nCurves = PSEsPicoLib.GetMatrixCount(value_matrix)
    enddata = value_matrix #makes hte array accsesible to safe with safedata function -b
    
    dfenddata= DAlib.createDataframes(nEle, enddata)
    
    
    
    
    #New plitting code for graphs in one window: 

    frameMonitor.destroy()
    frameMonitor = LabelFrame(root, text = "Monitor")
    frameMonitor.grid(row=frameMonitorPos["row"], column=frameMonitorPos["col"],pady=15)



    ResultColumn1 = [] #Potential or Frequency 
    ResultColumn2 = [] #Current or Zi
    ResultColumn3 = [] #Zr



#Get the inserted data and write it in an array
 
def getSettings(): 
    global lastload
    emptyfields=0
    #creating array for input Values 
    settingValues = []
    for i in range(nEle):
        settingValues.append([])

    #sampling the entries and putting them into the field 
    for n in range(nEle):
        for i in range(nFields):
            
            settingValues[n].append(allColummns[n][i].get())

    #check if all fields are filled
    for n in range(nEle):
        for i in range(nFields):
            
            if len(settingValues[n][i]) == 0:
                emptyfields = emptyfields+1
    if emptyfields !=0:
        messagebox.showwarning("Error", "Not all fields filled!")
        return
    
    
    #Open the blank file 
    with open(choiceofblank[usedmethod], 'r') as file: 
        filedata = file.read()
    print("Blank File Opened:")
    print(filedata)

    #replace the value of each field in each electrode
    for n in range(nEle):
        for i in range(nFields):
            fillInValue = '#e'+str(n+1)+'f'+str(i+1)
            filedata = filedata.replace(fillInValue, settingValues[n][i] )

    #safe as output file
    with open('used_methods/current_method.mscr', 'w') as file:
        file.write(filedata)

    lastload = None


def buttonPress():
    global frameStatus
    getSettings()
    runMethod(".\\used_methods", "current_method.mscr")
    #CheckFileExistAndRename()
    statusChange("Done", "green")
    winsound.MessageBeep()


    





root.mainloop()

