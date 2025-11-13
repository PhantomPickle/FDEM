#!/usr/bin/env python
import os
import time
import serial
import re
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

with open ("data/MagData-"+ str(string_time)+".csv","w") as file:
	while current_time - start_time < scan_duration:
		try:
			mag_data_raw=ser.readline().decode('ascii')
			current_time = get_seconds()
			mag_data_parsed = re.findall(r'[+-]\d{6}', mag_data_raw)
			print(mag_data_parsed[0])
			file.write(f"{current_time}, {mag_data_parsed[0]}, {mag_data_parsed[1]}, {mag_data_parsed[2]}\n"),
			print(mag_data_raw),
		except KeyboardInterrupt:
			print("\nStopping!")
			file.close(),
			break

print("Writing mag data to log file.")


