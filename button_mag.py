#!/usr/bin/env python
import os
import time
import serial
from sys import argv
from time import sleep
from time import gmtime
from time import strftime
from datetime import datetime as dt

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
scan_duration = int(argv[1])

def get_seconds():
    return dt.now().hour*3600 + dt.now().minute*60 + dt.now().second

print("Recording Mag Data"+"\n")

start_time = get_seconds()
string_time = strftime("%Y-%m-%d %H-%M-%S",gmtime())
current_time = start_time

with open ("MagData-"+ str(string_time)+".txt.","w") as file:
	while current_time - start_time < scan_duration:
		try:
			x=ser.readline()
			current_time = get_seconds()
			file.write(str(current_time) + ',' + str(x)),
			print(x),
		except KeyboardInterrupt:
			print("\nStopping!")
			file.close(),
			break

print("Writing mag data to log file.")


