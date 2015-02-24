import serial
import io
import py_acc
import time as Timer

port = "/dev/ttyAMA0"
baud = 9600
time_out = 5

xbee = serial.Serial(port,baudrate=baud,timeout=time_out)

while 1:
    if xbee.inWaiting() > 0:
        print(xbee.readline())
    xbee.write("ping\n")
    Timer.sleep(1)
