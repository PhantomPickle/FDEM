#!/usr/bin/env python
import os
import time
import serial
from time import sleep
from time import gmtime
from time import strftime
from datetime import datetime

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

actual_time = strftime("%Y-%m-%d %H-%M-%S",gmtime())

input("Press enter to start recording\n")
print("Beginning data collection!"+"\n")
with open ("MagData-"+ str(actual_time)+".txt.","w") as file:
	while 1:
		try:
			x=ser.readline()
			file.write(str(x)),
			print(x),
		except KeyboardInterrupt:
			print("\nStopping!")
			file.close(),
			break

