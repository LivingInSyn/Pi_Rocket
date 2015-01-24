import serial
import io
import py_acc
import time as Timer

port = "/dev/ttyAMA0"
baud = 9600
time_out = 5

xbee = serial.Serial(port,baudrate=baud,timeout=time_out)

xbee.write(unicode("ping\n"))
