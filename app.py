#! /usr/bin/env python3
# Flask web app

from flask import Flask, render_template, request
import re
from datetime import datetime


app = Flask(__name__)

today = datetime.today()
todayString = datetime.strftime(today, "%Y-%m-%d")
yesterday = datetime(today.year, today.month, today.day-1)
yesterdayString = datetime.strftime(yesterday, "%Y-%m-%d")

def filterDates(rawlines, start = todayString, end = yesterdayString):
	endDate = datetime.strptime(start, "%Y-%m-%d")
	startDate = datetime.strptime(end, "%Y-%m-%d")
	endDate = datetime(endDate.year, endDate.month, endDate.day + 1) # Because you want until 23:59 on the end date
	
	dates = [i.split('\t')[0] for i in rawlines]
	parsedDates = parsedDates = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in dates]

	truth = [startDate <= day <= endDate for day in parsedDates]

	matchingLines = [rawlines[i] for i in range(len(truth)) if truth[i]]
	return matchingLines


@app.route('/log')
def makelog():
	with open('./datalog.txt','r') as file:
		data = file.readlines()
	# Ignore error outputs to log, just in case
	def isTrueLine(line):
		pattern = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\t(?!-999)[\d\.]{0,5}(?!-999)\t[\d\.]{0,5}')
		return bool(pattern.search(line))
	truelines = [line for line in data if isTrueLine(line)]
	finaldata = ''.join(truelines)
	header = 'time\ttemp\thum\n'
	return header + finaldata


@app.route('/errlog')
def makeErrlog():
	# Placeholder for smart date selection
	# When finished doing for regular log, copy over here.


	header = 'time\ttemp\thum\n'
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

