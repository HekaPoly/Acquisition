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
import threadDataAcquisition  # Import main.py in the same directory

# Get relative path
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


###################################################################
# This class defines the content of the Info window - it contains all 
# user input boxes, the possibility to reset and submit information
###################################################################
class InfoWindow(Screen):
    # Define objects used throughout the window
    number_of_electrodes = ObjectProperty(None)
    number_of_encoders = ObjectProperty(None)
    filename = ObjectProperty(None)

    # Click on submit button
    def submitBtn(self):
        if int(self.number_of_electrodes.text) > 0 \
        and int(self.number_of_electrodes.text) < 9:
            if int(self.number_of_encoders.text) > 0 \
            and int(self.number_of_encoders.text) < 5:
                if self.filename.text != "":
                    # Set the current object of the Acquire 
                    # window to be the filename
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
        self.number_of_electrodes.text = '8'
        self.number_of_encoders.text = '4'
        self.filename.text = 'Essai_Classification_1'

    # Click on save button
    # All info is sent in a .txt file to be read afterwards 
    # by acquiring thread
    def saveSelf(self):
        with open(ROOT_DIR 
        + '/ReceiveData_Prise_Donnees/config_files/' 
        + self.filename.text 
        + '.txt', 'w') as f:
            f.write(self.filename.text)
            f.write('\n')
            f.write(self.number_of_electrodes.text)
            f.write('\n')
            f.write(self.number_of_encoders.text)


###################################################################
# This class contains everything related to the data acquisition
###################################################################
class AcquireWindow(Screen):
    # Define objects used throughout the window
    file_name = ObjectProperty(None)
    number_of_electrodes_info = ObjectProperty(None)
    number_of_encoders_info = ObjectProperty(None)
    acquisition = ObjectProperty(None)
    thread_acquisition = ObjectProperty(None)
    #threadGenerate = ObjectProperty(None)
    stop_thread = ObjectProperty(None)
    current = ""

    # Defines what happens when we enter the Acquire window 
    # - loads the user defined information from previous window
    def on_enter(self):
        self.loadSelf()

    # Defines what happens when a load is 
    # required upon entering the Acquire window
    def loadSelf(self):
        # The .txt file created when the submit button is clicked 
        # is used here
        with open(ROOT_DIR 
        + '/ReceiveData_Prise_Donnees/config_files/' 
        + self.current 
        + '.txt', 'r') as f:
            lines = f.readlines()
        self.file_name.text = "File name is " + lines[0].rstrip() + " .npy"
        self.number_of_electrodes_info.text = "There are " + \
            lines[1].rstrip() + " electrodes"
        self.number_of_encoders_info.text = "There are " + \
            lines[2].rstrip() + " encoders"

        # Enable or disable buttons
        self.startAcquisition.disabled = False

        # Create thread and create a threading event
        # To stop the thread we will need a stopThread event
        # Name of thread has to be random if the program is meant to 
        # run multiple times in a row
        stop_thread = Event()  # Set flag is false by default - will stop the acquiring thread
        name_thread_acquire = random.get_name()
        name_thread_acquire = Thread(target=threadDataAcquisition.acquireData,
        args=(lines[0].rstrip(), 
        int(lines[1].rstrip()), 
        int(lines[2].rstrip()),
        stop_thread))

        # Assign the objects to their objects in the window objects
        self.thread_acquire = name_thread_acquire
        self.stop_thread = stop_thread

    # Defines what happens when we press the start/stop acquisition button
    def startAcquire(self):
        # If we want to start data acquisition
        if (self.startAcquisition.text == 'Start data acquisition'):
            # Update buttons
            self.startAcquisition.text = 'Stop data acquisition'

            # Clear the stopThread flag to make sure recording will ensue
            self.stop_thread.clear()
            # Start the thread (call function main.acquireData)
            self.thread_acquire.start()

        # If we want to stop a data acquisition
        elif (self.startAcquisition.text == 'Stop data acquisition'):
            # Update buttons
            self.startAcquisition.text = 'Start data acquisition'
            self.startAcquisition.disabled = True

            # Set the flag to true and make the recording stop
            self.stop_thread.set()

    # Defines what happens when we press the plot data button
    def plotData(self):
        threadDataAcquisition.plotDataNpz(self.current)


###################################################################
# Indicate to screen manager that all is good 
# - Still don't know why this needs to be before main
###################################################################
class WindowManager(ScreenManager):
    pass


###################################################################
# Define error messages
###################################################################
def invalidNumberOfEncoders():
    pop = Popup(title='Invalid Number Of Encoders',
                content=Label(
                    text='Invalid number of encoders. \
                        Please insert value between 1 and 4.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()

def invalidNumberOfElectrodes():
    pop = Popup(title='Invalid Number Of Electrodes',
                content=Label(
                    text='Invalid number of electrodes. \
                        Please insert value between 1 and 8.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()

def invalidFilename():
    pop = Popup(title='Invalid Filename',
                content=Label(text='Invalid filename.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(
                    text='Please fill in all inputs with valid information.'),
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
