'''
This will be the python serial communications peice for the Py_Rocket Project
By Jeremy Mill <jeremymill@gmail.com>
'''

import serial
import io
import py_acc
import time

#this is the port that the xbee is on on the RPi
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
		#start our serial connection to the XBee
		xbee = serial.Serial(port,baudrate=baud,timeout=t_out)
		xbee.timeout = self.t_out
		
		#flow control
		self.enabled = 0
		self.fired = 0
		self.send_acc = 0
		self.send_alive = 1
		
		
		
	def ping_till_enabled(self):
		while self.enabled == 0:
			time.sleep(.5)
			xbee.write(unicode('ping\n'))
			if xbee.inWaiting() > 0:
				if xbee.readline() == unicode('pong\n'):
					self.enabled = 1
					xbee.write(unicode('firing enabled\n'))
					
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
					xbee.write(data_string)
					
					
					#wait for fire and send I'm alive messages
					self.wait_for_fire()
					self.ping_alive()
				else:
					pass
			else:
				pass
					
	def wait_for_fire(self):
		while self.fired == 0:
			if xbee.inWaiting() > 0:
				if xbee.readline() == unicode('FIRE\n'):
					self.fired = 1
					xbee.write(unicode('FIRING!!\n'))
					self.fire_rocket()
				else:
					pass
			else:
				pass
				
	def fire_rocket(self):
		#this will be GPIO code to trigger the transistor and fire the rocket
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
			xbee.write(data_string)
		
	def ping_alive(self):
		while self.send_alive == 1:
			time = strftime("%H:%M:%S")
			xbee.write(unicode('alive '+time+'\n'))
			time.sleep(1)
					
			
		
	
	def run(self):
		self.ping_till_enabled()
		
	
	
		



if __name__ == "__main__":
		DataFeed().run()
