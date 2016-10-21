#! /usr/bin/env python3
# Program to take temperature and humidity measurements

import pigpio, DHT22
import time, datetime

def initializeIO(pin):
	pi = pigpio.pi()
	sensor = DHT22.sensor(pi, pin)
	return pi, sensor

def measure(s):
	#pi = pigpio.pi()
	#sensor = DHT22.sensor(pi, 4) # I believe this number depends on what GPIO pin you use
	# Time in mdY, HMS format. Sorry, non-Americans
	t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Need Plotly-compatible format
	s.trigger()
	time.sleep(0.1) # Need to let it sleep so the trigger can finish before printing
	return t, round(s.temperature(),3), round(s.humidity(),3)


if __name__ == '__main__':
	pi, sensor = initializeIO(4) # GPIO pin 4 
	date, temp, hum = measure(sensor)

	print('{datetime}\t{temperature}\t{humidity}'.format(datetime=date, temperature=temp, humidity=hum))
	
