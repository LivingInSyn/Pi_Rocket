'''
This will be the python serial communications peice for the Py_Rocket Project
By Jeremy Mill <jeremymill@gmail.com>
'''

import serial
import io
import py_acc

#this is the port that the xbee is on on the RPi
#this isn't  correct if it's on USB
port = '/dev/ttyAMA0'
baud = '9600'


class DataFeed:
	def __init__(self):
		#make an instance of our accelerometer
		acc = py_acc.Accelerometer()
		



if __name__ == "__main__":
		DataFeed().run()
