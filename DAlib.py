
import pandas as pd 
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def createDataframes(nEle, enddata):

    #Find out how many different steps the measurement has so they can be seperated 
    #print(len(enddata))
    nMeasurementSteps = len(enddata) / nEle
    #print(nMeasurementSteps)
    nMeasurementSteps = int(nMeasurementSteps)
    #print(nMeasurementSteps)
    #sort the measurement steps into their own list inside the measurementsheets list

    MeasurementSheets = []

    for i in range(nMeasurementSteps):
        MeasurementSheets.append([]) #prepares n empty lists for each step of the measurement process eg. pretreatment, measuring against oc etc.


    stepcounter = 0

    for data in enddata:

        if stepcounter == nMeasurementSteps:  #Counts to the number of used Methods, then resets, to cycle through the data
            stepcounter = 0

        MeasurementSheets[stepcounter].append(data)

        stepcounter = stepcounter + 1

    #print(MeasurementSheets[0])

    #create list to host dataframes: 
    DataframeSheets = []

    for i in range(len(MeasurementSheets)):
        DataframeSheets.append([])
        for n in range(len(MeasurementSheets[i])):
            DataframeSheets[i].append([])

    #print(DataframeSheets)
        


    #Transplant the MeasurementSheet list into a Dataframe list and concat them into one Dataframe. 

    for i in range(len(MeasurementSheets)):
        
        for n in range(len(MeasurementSheets[i])):
                    
            DataframeSheets[i][n] = pd.DataFrame(MeasurementSheets[i][n])

    DfEndresults = []

    for i in range(len(DataframeSheets)):
        DfEndresults.append([])

    for i in range(len(DataframeSheets)):
        DfEndresults[i] = pd.concat(DataframeSheets[i], axis=1)





    #finding the number of results per sheet (eg, 2 for potentiometry, 3 for eis etc.)

    nResultColumns = []

    for i in range(len(MeasurementSheets)):
        n = len(MeasurementSheets[i][0][0]) #look at first entry of each sheet 
        nResultColumns.append(n) #append the list 

    #print(nResultColumns)
    for i in range(len(DfEndresults)):
        #print(i)
    #Change the columnname to represent the data 
        columnnames = [] #list for columnnames 


    #go through the sheets and then through each column, if the field gets over the number of fields its supposed to have , set to one and increase electrode count

    for i in range(len(DfEndresults)):  #create a columnname list for n of sheets
        columnnames.append([])
        #print(columnnames)
        electrodeCounter = 1
        fieldCounter = 1


        for n in range(len(DfEndresults[i].columns)):
            columnnames[i].append("Electrode " + str(electrodeCounter) + " Field " + str(fieldCounter))
            fieldCounter = fieldCounter+1
            
            if fieldCounter == nResultColumns[i]+1:
                fieldCounter = 1
                electrodeCounter = electrodeCounter+1


        

    columnnames
    #fill the columnnames list into the dataframe indices 

    for i in range(len(DfEndresults)):
        DfEndresults[i].columns = columnnames[i] 
  
    return DfEndresults
   

def plotResults(DfToPlot, method):

    if method == "eis":
        toPlot_x = DfToPlot[-1].iloc[:,1::3]
        toPlot_y = DfToPlot[-1].iloc[:,2::3]
        xLabel = "z '"
        yLabel = "z ''"


    else: 
        toPlot_x = DfToPlot[-1].iloc[:,0::2]
        toPlot_y= DfToPlot[-1].iloc[:,1::2]
        xLabel = "Voltage"
        yLabel = "Current"


    fig, ax = plt.subplots()

    labelnumber = 0
    for col1, col2 in zip(toPlot_x.columns, toPlot_y.columns):
        labelnumber = labelnumber + 1 
        ax.plot(toPlot_x[col1], toPlot_y[col2], label = "Electrode " + str(labelnumber))

    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.legend()


    plot_window = tk.Toplevel()
    plot_window.title('Results')
    plot_window.iconbitmap("ui_graphics/Elepreplogosmall.ico")

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack()




### .