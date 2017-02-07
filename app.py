#! /usr/bin/env python3
# Flask web app

from flask import Flask, render_template, request
import re
from datetime import date


app = Flask(__name__)


@app.route('/log')
def makelog():
	# Placeholder for smart date selection
	startdate = request.args.get("start")
	enddate = request.args.get("end")
	if (startdate is None) or (enddate is None):
		today = date.today()
		yesterday = date(startdate.year, startdate.month, startdate.day - 1)
		(startdate, enddate) = (yesterday, today)



	header = 'time\ttemp\thum\n'
	LINES = 500
	with open('./datalog.txt','r') as file:
		data = file.readlines()
	# Ignore error outputs to log, just in case
	def isTrueLine(line):
		pattern = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\t(?!-999)[\d\.]{0,5}(?!-999)\t[\d\.]{0,5}')
		return bool(pattern.search(line))
	truelines = [line for line in data if isTrueLine(line)]
	finaldata = ''.join(truelines)
	return header + finaldata


@app.route('/errlog')
def makeErrlog():
	# Placeholder for smart date selection
	# When finished doing for regular log, copy over here.


	header = 'time\ttemp\thum\n'
	LINES = 500
	with open('./errorlog.txt') as file:
		data = file.readlines()
	lines = [line for line in data]
	finaldata = ''.join(lines)
	return header + finaldata


@app.route('/')
def index():
	return render_template('./index.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

