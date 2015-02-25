'''
This will be the python serial communications peice for the Py_Rocket Project
By Jeremy Mill <jeremymill@gmail.com>
'''

'''
This is the rocket side
'''

import serial
import io
import py_acc
import time as Timer
import RPi.GPIO as GPIO

#this is the port that the self.xbee is on on the RPi
#this isn't  correct if it's on USB
#port = '/dev/ttyAMA0'
#baud = 9600
#t_out = 5


class DataFeed:
    def __init__(self):
        #set variables
        self.port = '/dev/ttyAMA0'
        self.baud = 9600
        self.t_out = 5
        #make an instance of our accelerometer
        self.acc = py_acc.Accelerometer()
        #start our serial connection to the self.xbee
        self.xbee = serial.Serial(self.port,baudrate=self.baud,timeout=self.t_out)
        #self.xbee.timeout = self.t_out
        
        #flow control
        self.enabled = 0
        self.fired = 0
        self.send_acc = 0
        self.send_alive = 1
        
        #GPIO control
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
        
        
        
        
    def ping_till_enabled(self):
        while self.enabled == 0:
            Timer.sleep(.5)
            self.xbee.write(unicode('ping\n'))
            if self.xbee.inWaiting() > 0:
                if self.xbee.readline() == unicode('pong\n'):
                    self.enabled = 1
                    self.xbee.write(unicode('firing enabled\n'))
                    
                    #get the initial values and send them to the host
                    #the accelerometer values
                    ax = str(self.acc.get_x_value())
                    ay = str(self.acc.get_y_value())
                    az = str(self.acc.get_z_value())
                    #the gyro values
                    gx = str(self.acc.get_GX_value())
                    gy = str(self.acc.get_GY_value())
                    gz = str(self.acc.get_GZ_value())
                    #time
                    time = strftime("%H:%M:%S")
                    #temp
                    temp = str(self.acc.get_TEMP_value())
                    #format it into a string
                    data_string = unicode('AX*'+ax+'AY*'+ay+'AZ*'+az+'GX*'+gx+'GY*'+gy+'GZ*'+gz+'TE*'+temp+'T*'+time+'\n')
                    self.xbee.write(data_string)
                    
                    
                    #wait for fire and send I'm alive messages
                    self.wait_for_fire()
                    self.ping_alive()
                else:
                    pass
            else:
                pass
                    
    def wait_for_fire(self):
        while self.fired == 0:
            if self.xbee.inWaiting() > 0:
                if self.xbee.readline() == unicode('FIRE\n'):
                    self.fired = 1
                    self.xbee.write(unicode('FIRING!!\n'))
                    self.fire_rocket()
                else:
                    pass
            else:
                pass
                
    def fire_rocket(self):
        GPIO.output(7, GPIO.HIGH)
        self.send_alive = 0
        self.send_data()
        
    def send_data(self):
        while 1:
            #the accelerometer values
            ax = str(self.acc.get_x_value())
            ay = str(self.acc.get_y_value())
            az = str(self.acc.get_z_value())
            #the gyro values
            gx = str(self.acc.get_GX_value())
            gy = str(self.acc.get_GY_value())
            gz = str(self.acc.get_GZ_value())
            #time
            time = strftime("%H:%M:%S")
            #temp
            temp = str(self.acc.get_TEMP_value())
            #format it into a string
            data_string = unicode('AX*'+ax+'AY*'+ay+'AZ*'+az+'GX*'+gx+'GY*'+gy+'GZ*'+gz+'TE*'+temp+'T*'+time+'\n')
            self.xbee.write(data_string)
        
    def ping_alive(self):
        while self.send_alive == 1:
            time = strftime("%H:%M:%S")
            self.xbee.write(unicode('alive '+time+'\n'))
            time.sleep(1)
                    
            
        
    
    def run(self):
        self.ping_till_enabled()
        
    
    
        



if __name__ == "__main__":
        DataFeed().run()
