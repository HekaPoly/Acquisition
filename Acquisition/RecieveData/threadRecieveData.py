from json import encoder
import serial
import queue
import timeit
import matplotlib.pyplot as plt
import numpy as np
import os

# Get relative path
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

###################################################################
# This function is called when the user wants to start data acquisition
# We use this function as a initializer to make sure everything is correctly set to collect data
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

    # Create 8 lists for the maximal 8 electrodes
        # Some lists will be empty if less than 8 electrodes are specified
    for i in range(0, 8):
        electrode=[]
        generalList.append(electrode)

    # Create 4 lists for the maximal 4 encoders
        # Some lists will be empty if less than 4 encoders are specified
    for i in range(0, 4):
        encodeur=[]
        generalList.append(encodeur)

    # Sanity print - checks if generalList was created correctly
    print("General list created.")
    print(generalList)

    # Call the collectData function to start collecting data
    collectData(filename, generalList, numberOfElectrodes, numberOfEncoders, stopEvent)


###################################################################
# This function is called after a general list has been correctly initialized
# @params: filename - Name of the .npy file the user wants to generate
#          generalList - List of lists to contain collected data
#          numberOfElectrodes - Number of electrodes collecting data
#          numberOfEncoders - Number of encoders collecting data
#          stopEvent - Event to indicate to stop collecting data
###################################################################
def collectData(filename, generalList, numberOfElectrodes, numberOfEncoders, stopEvent):
    # Check if serial port is open
        # Sets the parameters if not open
    portOpen = False
    while not portOpen:
        try:
            # Make sure COM port is correct (see in Gestionnaire de périphériques)
            arduino = serial.Serial(port='COM4', baudrate=1000000, timeout=None, xonxoff=False, rtscts=False,
                                    dsrdtr=False)
            # Clear the serial buffer (input and output)
            arduino.flushInput()
            arduino.flushOutput()
            portOpen = True
            print("Found serial port")
        except:
            pass

    # Create a queue to hold in all the bytes sent over the serial port
    que = queue.Queue()
    print('Queue created, starting acquisition')

    # Start a timer to determine amount of time passed between beggining and end of acquisition
    start = timeit.default_timer()

    while not stopEvent.is_set(): # While the event flag to stop the thread is false
        # Get the number of bytes in the input buffer of the serial port
        bytesToRead = arduino.in_waiting
        if bytesToRead != 0:
            # Read the number of bytes in the input buffer
            data = arduino.read(bytesToRead)
            # Insert the bytes read in the que
            for i in range(len(data)):
                que.put(data[i])

    else: # Flag is set to true - user wants to stop the data acquisition
        stopAcquisition(filename, generalList, numberOfElectrodes, numberOfEncoders, start, que)


###################################################################
# This function is called after user has indicated it wants to stop the data acquisition
# @params: filename - Name of the .npy file the user wants to generate
#          generalList - List of lists to contain collected data
#          numberOfElectrodes - Number of electrodes collecting data
#          numberOfEncoders - Number of encoders collecting data
#          start - Timer indication of when data acquisition began
#          que - The queue where all the bytes are stored
###################################################################
def stopAcquisition(filename, generalList, numberOfElectrodes, numberOfEncoders, timerStart, que):
    # Stop timer recording the acquisition time
    stop = timeit.default_timer()
    print(stop - timerStart)

    # Print the number of packs (of 32 bytes) of data sent 
    print(que.qsize() / (numberOfElectrodes*2 + numberOfEncoders*4))

    # Transform the queue into a list to simplify data recomposition
    listData = list(que.queue)

    # Create list to contain all recomposed values
    values = []
    
    counter = 0
    # Loops to recompose values
    for i in range(0, int(len(listData) / (numberOfElectrodes*2 + numberOfEncoders*4))):
        # First loop recomposes electrode values
            # Append two bytes and left shift the second one (as it is the MSB)
            # Do this for the specified number of electrodes
        for j in range(numberOfElectrodes):
            values.append(listData[counter] + (listData[counter + 1] << 8))
            # Counter is incremented of 2 as every electrode value is 2 bytes
            counter += 2

        # Second loop recomposes encoders values
            # Append two bytes and left shift the second, third and fourth bytes
            # Do this for the specified number of encoders
        for k in range(numberOfEncoders):
            values.append((listData[counter]) + (listData[counter + 1] << 8) + (listData[counter + 2] << 16) + (
                            listData[counter + 3] << 24))
            # Counter is incremented of 4 as every encoder value is 4 bytes
            counter += 4

    # Plot all values obtained
    for i in range(0, len(values) - (len(generalList)-1), len(generalList)):
        for j in range(0, len(generalList)):
            generalList[j].append(values[i + j])
    print('Acquisition done')

    # Call the generateNpyFile function 
    generateNpyFile(filename, generalList)


def generateNpyFile(filename, listOfValues):
    # Transfer all lists into .npy file
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

    np.savez(ROOT_DIR + '/RecieveData/savedData/' + filename, 
                electrode1=electrode1, electrode2=electrode2, electrode3=electrode3, electrode4=electrode4,
                electrode5=electrode5, electrode6=electrode6, electrode7=electrode7, electrode8=electrode8,
                encoder1=encoder1, encoder2=encoder2, encoder3=encoder3, encoder4=encoder4)


# Plots data coming from an npz
def plotDataNpz(nameOfNpzFile):
    generalPlotList = []
    # Create 8 lists for the maximal 8 electrodes
        # Some lists will be empty if less than 8 electrodes are specified
    for i in range(0, 8):
        electrode=[]
        generalPlotList.append(electrode)

    # Create 4 lists for the maximal 4 encoders
        # Some lists will be empty if less than 4 encoders are specified
    for i in range(0, 4):
        encoder=[]
        generalPlotList.append(encoder)

    # Load all the npy files contained in the npz
    dataNpz = np.load(ROOT_DIR + '/RecieveData/savedData/' + nameOfNpzFile + '.npz')
    
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

    # There are 8 electrodes max
    fig, axs = plt.subplots(8)
    fig.suptitle('Resultats obtenus Electrodes')
    numeroElectrode = 0
    for i in range(0, 8):
        axs[numeroElectrode].plot(generalPlotList[i])
        axs[numeroElectrode].set_title(f'Electrode {numeroElectrode}')
        numeroElectrode+=1
    plt.show()
    
    # There are 4 encoders max
    fig, axs = plt.subplots(4)
    fig.suptitle('Resultats obtenus Encodeurs')
    numeroEncodeur = 0
    for i in range(8, 12):
        axs[numeroEncodeur].plot(generalPlotList[i])
        axs[numeroEncodeur].set_title(f'Encodeur {numeroEncodeur}')
        numeroEncodeur += 1
    plt.show()
