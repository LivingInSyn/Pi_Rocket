'''
This is the computer side of the Pi-Rocket Project

by Jeremy Mill <jeremymill@gmail.com>
'''

from kivy.config import Config
Config.set('graphics','height',480)
Config.set('graphics','width',800)
Config.write()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
import subprocess
import time

class Gui_Screen(Screen):
    def ping_detected(self,detected):
        if detected == True:
            self.ids.ping_det_image.source = "green_light.png"
        

class Laptop_Gui_App(App):
    def build(self):
        #self.icon = 'myicon.ico'
        self.title = 'Rocket Launch GUI'
        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        self.gui_screen = Gui_Screen(name='gui_screen')
        root.add_widget(self.gui_screen)
        #I will uncomment the next line if I need the window close method
        #root.add_widget(self.logout_times)
        return root
        
    def click_fire(self):
        pass
        #stub right now will call to fire rocket
        
    def watch_pings(self):
        pass
        #stub
        #will watch the pings from the pi and change a light color
        
    def write_data(self):
        pass
        #stub
        #will gather up the data sent and write it to a file

if __name__ == '__main__':
    Laptop_Gui_App().run()
    
