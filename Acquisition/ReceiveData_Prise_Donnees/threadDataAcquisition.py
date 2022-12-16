import serial
import queue
import timeit
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import altair as alt
import pandas as pd
import math
import time

# Get relative path to folder
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

############################### START OF SCRIPT #############################################
###################################################################
# 
#
# @params: 
###################################################################
def sendSerialCommand(command_to_send, arduino):
    arduino.write(bytes(command_to_send, 'utf-8'))

###################################################################
# This function is called when the user wants to start data acquisition
# We use this function as a initializer to make sure everything is correctly set to collect data. This function creates
# generalList, a list of (nbElectrodes + nbEncodeurs) empty lists and each of these empty list will contain all the bytes that were sent over by the electrodes and encoders.
#
# @params: filename - Name of the .npy file the user wants to generate
#          numberOfElectrodes - Number of electrodes collecting data
#          numberOfEncoders - Number of encoders collecting data
#          stopEvent - Event to indicate to stop collecting data
###################################################################
def acquireData(filename, numberOfElectrodes, numberOfEncoders, stopEvent):
    # Generic sanity print 
    print("Thread has started.")
    print("Number of electrodes: ", numberOfElectrodes)
    print("Number of encoders: ", numberOfEncoders)
    
    # Create a general list to contain all the lists of values of data collected
    generalList=[]

    # Create empty lists to store all data
    for i in range(0, 8):
        electrode=[]
        generalList.append(electrode)

    for i in range(0, 4):
        encodeur=[]
        generalList.append(encodeur)

    print("General list created.")
    print(generalList)

    # Call the collectData function to start collecting data
    collectData(filename, generalList, numberOfElectrodes, numberOfEncoders, stopEvent)


###################################################################
# This function is called after a general list has been correctly initialized
# It initializes a FIFO queue meaning the first value that got in will be the first one out. Data coming from
# the uC will be stored in this queue until post-processing.
#
# @params: filename - Name of the .npy file the user wants to generate
#          generalList - List of lists to contain collected data
#          numberOfElectrodes - Number of electrodes collecting data
#          numberOfEncoders - Number of encoders collecting data
#          stopEvent - Event to indicate to stop collecting data
#
# TODO: Implement automatic way to find correct COM port
###################################################################
def collectData(filename, generalList, numberOfElectrodes, numberOfEncoders, stopEvent):
    # Check if serial port is open
        # Sets the parameters if not open
    portOpen = False
    while not portOpen:
        try:
            # Make sure COM port is correct (see in Gestionnaire de périphériques)
            arduino = serial.Serial(port='COM6', baudrate=1000000, timeout=None, xonxoff=False, rtscts=False,
                                    dsrdtr=False)
            # Clear the serial buffer (input and output)
            arduino.flushInput()
            arduino.flushOutput()
            portOpen = True
            print("Found serial port")
        except:
            pass
    que = queue.Queue()   
    print('Queue created, starting acquisition')

    # Reset encoder reference values
    sendSerialCommand('A', arduino)
    print('Encoder reference values have been reset')

    print('Acquisition started!')

    # Start a timer to determine amount of time passed between beggining and end of acquisition
    start = timeit.default_timer()
    byte_array = bytearray()

    while not stopEvent.is_set(): # While the event flag to stop the thread is false
        # Determine if any values are waiting in read buffer
        bytesToRead = arduino.in_waiting

        if bytesToRead != 0:
            byte_array = arduino.read(bytesToRead)
            # Insert the bytes read in the queue
            for i in range(len(byte_array)):
                que.put(byte_array[i])
                
    else: # Flag is set to true - user wants to stop the data acquisition
        # Reset all values
        arduino.flushInput()
        arduino.flushOutput()

        stopAcquisition(filename, generalList, numberOfElectrodes, numberOfEncoders, start, que)

###################################################################
# This function is called after user has indicated it wants to stop the data acquisition
# The main for loop in this function takes into account the electrode bytes (which come in first in the pack) and then the 
# encoder bytes (which come last in the pack), hence the order of recomposition.
# @params: filename - Name of the .npy file the user wants to generate
#          generalList - List of lists to contain collected data
#          numberOfElectrodes - Number of electrodes collecting data
#          numberOfEncoders - Number of encoders collecting data
#          start - Timer indication of when data acquisition began
#          que - The queue where all the bytes are stored
###################################################################
def stopAcquisition(filename, generalList, numberOfElectrodes, numberOfEncoders, timerStart, que):
    stop = timeit.default_timer()
    print(stop - timerStart)

    # Print the number of packs (of 32 bytes) of data sent (electrodes: 2 bytes ; encodeurs: 4 bytes)
    nbPacks = int(que.qsize() / (numberOfElectrodes * 2 + numberOfEncoders * 4))

    # Transform the queue into a list to simplify data recomposition
    listData = list(que.queue)
    recomposedValues = []

    # Offset value comes from the setup() function in main.cpp of the SendData_Prise_Donnees folder
    OFFSET_FROM_TEENSY = 0

    counter = 0
    # Loops to recompose values
    for i in range(0, nbPacks):
        # First loop recomposes electrode values - Left shift the second byte of the decomposed value (as it is the MSB)
        # Counter is incremented of 2 as every electrode value is 2 bytes
        for j in range(numberOfElectrodes):
            recomposedValues.append(listData[counter] + (listData[counter + 1] << 8))
            counter += 2

        # Second loop recomposes encoders values - Left shift the second, third and fourth bytes of the decomposed values
        # Counter is incremented of 4 as every encoder value is 4 bytes
        for k in range(numberOfEncoders):
            recomposedValues.append((listData[counter]) + (listData[counter + 1] << 8) + (listData[counter + 2] << 16) + (
                            listData[counter + 3] << 24))
            recomposedValues[-1] = recomposedValues[-1] - OFFSET_FROM_TEENSY
            counter += 4

    # generalList is a list of lists and each list represent a measuring instrument
    # Inside those lists are packs of length of 2 bytes for an electrode and 4 bytes for an encodeur
    for i in range(0, len(recomposedValues) - ((len(generalList) - 1)), len(generalList)): # generalList is the step of the range and is equal to the number of measuring instruments
        # each i iteration represent a sampled moment of all the measuring instruments
        for j in range(0, len(generalList)):
            generalList[j].append(recomposedValues[i + j])
    print('Acquisition done')

    generateNpyFile(filename, generalList)


##################################################################
# This function is called to transfer all the data collected into a file with the extennsion npy
# @params: filename - Name of the .npy file the user wants to generate
#          listOfValues - List that containts data previously collected that we want to transfer  
##################################################################
def generateNpyFile(filename, listOfValues):
    # Transfer all lists into .npy file
    # By properly organizing the generalList, we can easily extract the information for each measuring instrument
    electrode1 = np.array(listOfValues[0])
    electrode2 = np.array(listOfValues[1])
    electrode3 = np.array(listOfValues[2])
    electrode4 = np.array(listOfValues[3])
    electrode5 = np.array(listOfValues[4])
    electrode6 = np.array(listOfValues[5])
    electrode7 = np.array(listOfValues[6])
    electrode8 = np.array(listOfValues[7])

    encoder1 = np.array(listOfValues[8])
    encoder2 = np.array(listOfValues[9])
    encoder3 = np.array(listOfValues[10])
    encoder4 = np.array(listOfValues[11])

    np.savez(ROOT_DIR + '/ReceiveData_Prise_Donnees/saved_data/' + filename, 
                electrode1=electrode1, electrode2=electrode2, electrode3=electrode3, electrode4=electrode4,
                electrode5=electrode5, electrode6=electrode6, electrode7=electrode7, electrode8=electrode8,
                encoder1=encoder1, encoder2=encoder2, encoder3=encoder3, encoder4=encoder4)


##################################################################
# This function is called to plot all the values obtained during the acquisition period
# @params: nameOfNpzFile - Name of the .npz file the user wants to plot
##################################################################
def plotDataNpz(nameOfNpzFile):
    generalPlotList = []
    MAX_NUMBER_ELECTRODES = 8
    MAX_NUMBER_ENCODERS = 4

    # Create 8 lists for the maximal 8 electrodes
        # Some lists will be empty if less than 8 electrodes are specified
    for i in range(0, MAX_NUMBER_ELECTRODES):
        electrode=[]
        generalPlotList.append(electrode)

    # Create 4 lists for the maximal 4 encoders
        # Some lists will be empty if less than 4 encoders are specified
    for i in range(0, MAX_NUMBER_ENCODERS):
        encoder=[]
        generalPlotList.append(encoder)

    # Load all the npy files contained in the npz
    dataNpz = np.load(ROOT_DIR + '/ReceiveData_Prise_Donnees/saved_data/' + nameOfNpzFile + '.npz')
    
    # Store all the data from the npy files
    dataElectrode = []
    generalPlotList[0] = dataNpz['electrode1']
    generalPlotList[1] = dataNpz['electrode2']
    generalPlotList[2] = dataNpz['electrode3']
    generalPlotList[3] = dataNpz['electrode4']
    generalPlotList[4] = dataNpz['electrode5']
    generalPlotList[5] = dataNpz['electrode6']
    generalPlotList[6] = dataNpz['electrode7']
    generalPlotList[7] = dataNpz['electrode8']

    dataEncoder = []
    generalPlotList[8] = dataNpz['encoder1']
    generalPlotList[9] = dataNpz['encoder2']
    generalPlotList[10] = dataNpz['encoder3']
    generalPlotList[11] = dataNpz['encoder4']

    x = [None] * (len(generalPlotList))
    dataframe = [None] * (len(generalPlotList))
    list_color= ["pink", "blue", "green", "yellow", "red", "turquoise", "black",
                    "purple", "marine", "brown", "grey", "orange", "light blue", "darkgreen", "white"]
    
    fonction_graphiques(generalPlotList, x, dataframe, 
                            list_color, MAX_NUMBER_ELECTRODES, MAX_NUMBER_ENCODERS)



###################################################################
# @brief: This function plots all values obtained from electrodes in a single graph. It also plots
#           all values obtained from encoder values in a single graph.
# @params: list_Values - List of lists to contain collected data
#          x_values - List of lists to contain x values of the graph
#          source - List to contain x values and f(x)
#          color_list - List ton contain colors for the graph
#          max_electrodes - Maximum number of electrodes
#          max_encoders - Maximum number of encoders
###################################################################
def fonction_graphiques(list_Values, x_values, source, color_list, max_electrodes, max_encoders):
    graph_electrodes = [None] * max_electrodes
    graph_encodeurs = [None] * max_encoders

    for i in range(0, max_electrodes):
        x_values[i] = np.arange(0, len(list_Values[i]), 1)

        source[i] = pd.DataFrame({
            'Time (s)' : x_values[i],
            'Electrode values' : list_Values[i]
        })

        graph_electrodes[i] = alt.Chart(source[i], title='Électrodes').mark_line().encode(
            x = 'Time (s)',
            y = 'Electrode values',
            color=alt.value(color_list[i])
        )

        graph_electrodes[0] += graph_electrodes[i]
    
    for i in range (max_electrodes ,len(list_Values)):        
        x_values[i] = np.arange(0, len(list_Values[i]), 1)

        source[i] = pd.DataFrame({
            'Time (s)' : x_values[i],
            'Encoder values' : list_Values[i]
        })

        graph_encodeurs[i - max_electrodes] = alt.Chart(source[i], title='Encodeurs').mark_line().encode(
            x = 'Time (s)',
            y = 'Encoder values',
            color=alt.value(color_list[i])
        )

        graph_encodeurs[0] += graph_encodeurs[i - max_electrodes]
    
    graph_encodeurs[0].save(ROOT_DIR + '/ReceiveData_Prise_Donnees/results/graphique_encodeurs.html')  
    graph_electrodes[0].save(ROOT_DIR + '/ReceiveData_Prise_Donnees/results/graphique_electrodes.html')


    
    

