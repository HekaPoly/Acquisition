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

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
kv = Builder.load_file("GUI_Acquisition.kv")

class InfoWindow(Screen):
    """Cette classe définit le contenu de la fenêtre d'information
    """
    number_of_electrodes = ObjectProperty(None)
    number_of_encoders = ObjectProperty(None)
    file_name = ObjectProperty(None)

    def submitBtn(self):
        """Définit ce qui se passe lorsque l'on appuie sur le bouton Submit
        """
        if int(self.number_of_electrodes.text) > 0 and \
           int(self.number_of_electrodes.text) < 9:
            if int(self.number_of_encoders.text) > 0 and \
               int(self.number_of_encoders.text) < 5:
                if self.file_name.text != "":
                    """On assigne l'item de la fenêtre d'acquisition
                        au nom du fichier text créé par la fenêtre d'information
                    """
                    AcquireWindow.current = self.file_name.text
                    self.saveSelf()
                    self.reset()
                    """Changer de fenêtre"""
                    sm.current = "acquisition"
                else:
                    return invalidFilename()
            else:
                return invalidNumberOfEncoders()
        else:
            return invalidNumberOfElectrodes()

    def saveSelf(self):
        """Définit la procédure de sauvegarde des données inscrites par l'utilisateur
        """
        with open(ROOT_DIR 
                    + '/ReceiveData_Prise_Donnees/config_files/' 
                    + self.file_name.text 
                    + '.txt', 'w') as f:
            f.write(self.file_name.text)
            f.write('\n')
            f.write(self.number_of_electrodes.text)
            f.write('\n')
            f.write(self.number_of_encoders.text)

    def reset(self):
        """Définit la procédure de 
        """
        self.number_of_electrodes.text = '8'
        self.number_of_encoders.text = '4'
        self.file_name.text = 'Essai_Classification_1'

    
###################################################################
# This class contains everything related to the data acquisition
###################################################################
class AcquireWindow(Screen):
    """Cette classe définit le contenu de la fenêtre d'acquisition
    """
    file_name = ObjectProperty(None)
    number_of_electrodes_info = ObjectProperty(None)
    number_of_encoders_info = ObjectProperty(None)
    acquisition = ObjectProperty(None)
    stop_thread = ObjectProperty(None)
    current = ""

    # Defines what happens when we enter the Acquire window 
    # - loads the user defined information from previous window
    def on_enter(self):
        """Définit ce qui se produit lorsque l'on entre dans la fenêtre d'acquisition
            Ce fait automatiquement à chaque création de fenêtre d'acquisition
        """
        self.loadSelf()

    def loadSelf(self):
        """Procédure de chargement de l'information retenue par la fenêtre précédente (fenêtre d'information)
        """
        with open(ROOT_DIR + '/ReceiveData_Prise_Donnees/config_files/' + self.current + '.txt', 'r') as f:
            lines = f.readlines()

        self.file_name.text = "File name is " + lines[0].rstrip() + " .npy"
        self.number_of_electrodes_info.text = "There are " + lines[1].rstrip() + " electrodes"
        self.number_of_encoders_info.text = "There are " + lines[2].rstrip() + " encoders"

        """Activation du bouton de prise de données"""
        self.startAcquisition.disabled = False

        """Le flag stop_thread est false par défaut"""
        stop_thread = Event()

        name_thread_acquire = random.get_name()
        name_thread_acquire = Thread(target=threadDataAcquisition.acquireData,
                                        args=(lines[0].rstrip(), 
                                                int(lines[1].rstrip()), 
                                                int(lines[2].rstrip()),
                                                stop_thread))

        self.thread_acquire = name_thread_acquire
        self.stop_thread = stop_thread

    def startAcquire(self):
        """Définit ce qui se produit lorsque l'on appuie sur le bouton Start/Stop
        """
        if (self.startAcquisition.text == 'Start data acquisition'):
            self.startAcquisition.text = 'Stop data acquisition'
            self.stop_thread.clear()
            self.thread_acquire.start()

        elif (self.startAcquisition.text == 'Stop data acquisition'):
            self.startAcquisition.text = 'Start data acquisition'
            self.startAcquisition.disabled = True
            self.stop_thread.set()

    def plotData(self):
        """Définit ce qui se produit lorsque l'on appuie sur le bouton de Plot Data
        """
        threadDataAcquisition.plotDataNpz(self.current)


class WindowManager(ScreenManager):
    """Cette classe définit un Window Manager qui permettra de naviguer entre les fenêtres définies
    """
    pass


def invalidNumberOfEncoders():
    """Définit le popup apparaissant au cas où un mauvais nombre d'encodeurs est entré par l'utilisateur
    """
    pop = Popup(title='Invalid Number Of Encoders',
                content=Label(
                    text='Invalid number of encoders. \
                        Please insert value between 1 and 4.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()

def invalidNumberOfElectrodes():
    """Définit le popup apparaissant au cas où un mauvais nombre d'électrodes est entré par l'utilisateur
    """
    pop = Popup(title='Invalid Number Of Electrodes',
                content=Label(
                    text='Invalid number of electrodes. \
                        Please insert value between 1 and 8.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()

def invalidFilename():
    """Définit le popup apparaissant au cas où un mauvais nom de fichier est entré par l'utilisateur
    """
    pop = Popup(title='Invalid Filename',
                content=Label(text='Invalid filename.'),
                size_hint=(None, None), size=(500, 400))
    pop.open()

def invalidForm():
    """Définit le popup apparaissant au cas où une case d'information est vide
    """
    pop = Popup(title='Invalid Form',
                content=Label(
                    text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()

class MyMainApp(App):
    """Cette classe définit l'objet gérant l'interface graphique
    """
    def build(self):
        return sm


if __name__ == "__main__":
    sm = WindowManager()

    """On associe les noms info et acquisition aux objets InfoWindow et AcquireWindow"""
    screens = [InfoWindow(name="info"), AcquireWindow(name="acquisition")]
    for screen in screens:
        sm.add_widget(screen)

    """Fenêtre initiale"""
    sm.current = "info"

    MyMainApp().run()
