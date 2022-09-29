from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from threading import Event
from threading import Thread
from kivy.core.window import Window
import randomname as random
import os
import threadDataAcquisition # Import main.py in the same directory

# Get relative path
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


###################################################################
# This class defines the content of the Info window - it contains all user input boxes, the possibility to reset and submit information
###################################################################
class InfoWindow(Screen):
    # Define objects used throughout the window
    numberOfElectrodes = ObjectProperty(None)
    numberOfEncoders = ObjectProperty(None)
    filename = ObjectProperty(None)

    # Click on submit button
    def submitBtn(self):
        if int(self.numberOfElectrodes.text) > 0 and int(self.numberOfElectrodes.text) < 9:
            if int(self.numberOfEncoders.text) > 0 and int(self.numberOfEncoders.text) < 5:
                if self.filename.text != "":
                    # Set the current object of the Acquire window to be the filename
                    AcquireWindow.current = self.filename.text
                    # Save the information entered in a .txt file
                    self.saveSelf()
                    # Reset information in Info Window
                    self.reset()
                    # Change screens
                    sm.current = "acquisition"
                else:
                    return invalidFilename()
            else:
                return invalidNumberOfEncoders()
        else:
            return invalidNumberOfElectrodes()

    # Click on reset button
    def reset(self):
        self.numberOfElectrodes.text = '8'
        self.numberOfEncoders.text = '4'
        self.filename.text = 'Essai_Classification_1'

    # Click on save button
    # All info is sent in a .txt file to be read afterwards by acquiring thread
    def saveSelf(self):
        with open(ROOT_DIR + '/ReceiveData_Prise_Donnees/config_files/' + self.filename.text + '.txt', 'w') as f:
            f.write(self.filename.text)
            f.write('\n')
            f.write(self.numberOfElectrodes.text)
            f.write('\n')
            f.write(self.numberOfEncoders.text)


###################################################################
# This class contains everything related to the data acquisition
###################################################################
class AcquireWindow(Screen):
    # Define objects used throughout the window
    fileName = ObjectProperty(None)
    numberOfElectrodesInfo = ObjectProperty(None)
    numberOfEncodersInfo = ObjectProperty(None)
    acquisition = ObjectProperty(None)
    threadAcquisition = ObjectProperty(None)
    #threadGenerate = ObjectProperty(None)
    stopThread = ObjectProperty(None)
    current = ""

    # Defines what happens when we enter the Acquire window - loads the user defined information from previous window
    def on_enter(self):
        self.loadSelf()


    # Defines what happens when a load is required upon entering the Acquire window
    def loadSelf(self):
        # The .txt file created when the submit button is clicked is used here
        with open(ROOT_DIR + '/ReceiveData_Prise_Donnees/config_files/' + self.current + '.txt', 'r') as f:
            lines = f.readlines()
        self.fileName.text                  = "File name is " + lines[0].rstrip() + " .npy"
        self.numberOfElectrodesInfo.text    = "There are " + lines[1].rstrip() + " electrodes"
        self.numberOfEncodersInfo.text      = "There are " + lines[2].rstrip() + " encoders"

        # Enable or disable buttons
        self.startAcquisition.disabled = False

        # Create thread and create a threading event 
            # To stop the thread we will need a stopThread event
            # Name of thread has to be random if the program is meant to run multiple times in a row
        stopThread = Event()  # Set flag is false by default - will stop the acquiring thread
        nameThreadAcquire = random.get_name() 
        nameThreadAcquire = Thread(target=threadDataAcquisition.acquireData, args=(lines[0].rstrip(), int(lines[1].rstrip()), int(lines[2].rstrip()), stopThread))

        # Assign the objects to their objects in the window objects
        self.threadAcquire = nameThreadAcquire
        self.stopThread = stopThread


    # Defines what happens when we press the start/stop acquisition button 
    def startAcquire(self):
        # If we want to start data acquisition
        if(self.startAcquisition.text == 'Start data acquisition'):
            # Update buttons
            self.startAcquisition.text = 'Stop data acquisition'

            # Clear the stopThread flag to make sure recording will ensue
            self.stopThread.clear()
            # Start the thread (call function main.acquireData)
            self.threadAcquire.start()

        # If we want to stop a data acquisition
        elif(self.startAcquisition.text == 'Stop data acquisition'):
            # Update buttons
            self.startAcquisition.text = 'Start data acquisition'
            self.startAcquisition.disabled = True

            # Set the flag to true and make the recording stop
            self.stopThread.set()
    
    # Defines what happens when we press the plot data button
    def plotData(self):
        threadDataAcquisition.plotDataNpz(self.current)



###################################################################
# Indicate to screen manager that all is good - Still don't know why this needs to be before main
###################################################################
class WindowManager(ScreenManager):
    pass


###################################################################
# Define error messages
###################################################################
def invalidNumberOfEncoders():
    pop = Popup(title='Invalid Number Of Encoders',
                  content=Label(text='Invalid number of encoders. Please insert value between 1 and 4.'),
                  size_hint=(None, None), size=(500, 400))
    pop.open()


def invalidNumberOfElectrodes():
    pop = Popup(title='Invalid Number Of Electrodes',
                content=Label(text='Invalid number of electrodes. Please insert value between 1 and 8.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()


def invalidFilename():
    pop = Popup(title='Invalid Filename',
                content=Label(text='Invalid filename.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


###################################################################
# Main build for application
###################################################################
kv = Builder.load_file("GUI_Acquisition.kv")

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    sm = WindowManager()
    # Screen names are defined here
    screens = [InfoWindow(name="info"), AcquireWindow(name="acquisition")]
    for screen in screens:
        sm.add_widget(screen)

    # Initial screen is indicated here
    sm.current = "info"

    MyMainApp().run()