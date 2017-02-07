#! /usr/bin/env python3
# Program to take temperature and humidity measurements

import pigpio, DHT22
import time, datetime
import re

# https://stackoverflow.com/a/4943474
import os
import sys
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def initializeIO(pin):
	pi = pigpio.pi()
	sensor = DHT22.sensor(pi, pin)
	return pi, sensor

def measure(s):
	#pi = pigpio.pi()
	#sensor = DHT22.sensor(pi, 4) # I believe this number depends on what GPIO pin you use
	t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Need Plotly-compatible format
	
	s.trigger()
	time.sleep(1) 
	# Need to let it sleep so the trigger can finish before printing.
	# This doesn't cause an issue because the measurement is already taken at this point.

	return t, round(s.temperature(),3), round(s.humidity(),3)


if __name__ == '__main__':
	pi, sensor = initializeIO(4) # GPIO pin 4 
	date, temp, hum = measure(sensor)
	output = '{datetime}\t{temperature}\t{humidity}'.format(datetime=date, temperature=temp, humidity=hum)
	
	print(output) # Show to stdout for debugging

	pwd = get_script_path() + '/'

	# Then write to appropriate log
	if (bool(re.search("-999", output))): 
		with open(pwd + 'errorlog.txt', 'a') as f:
			f.write(output)
			f.write('\n')
	else:
		with open(pwd + 'datalog.txt', 'a') as f:
			f.write(output)
			f.write('\n')
		
