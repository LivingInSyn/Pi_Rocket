'''
This is the rocket side of the communications

written by Jeremy Mill
'''

import serial
import io
import time as Timer
import py_acc

class DataFeed:
    def __init__(self):
        #set vars
        self.port = '/dev/ttyAMA0'
        self.baud = 9600
        self.time_out = 5
        #make accelerometer instance
        self.acc = py_acc.Accelerometer()
        #make xbee, an instance of serial
        self.xbee = serial.Serial(self.port,baudrate=self.baud,timeout=self.time_out)
        #flow control
        self.enabled = 0
        
    def ping_till_alive(self):
        while self.enabled == 0:
            if self.xbee.inWaiting() == 0:
                self.xbee.write("ping\n")
                Timer.sleep(.5)
            else:
                if self.xbeereadline() == 'pong\n':
                    self.enabled = 1
                    #next func
                else:
                    pass
                
    def enabled_not_fired(self):
        #more more more
    
    def run(self):
        #there will be something here in a few
