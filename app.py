#! /usr/bin/env python3
# Flask web app

from flask import Flask, render_template, request
import re
from datetime import datetime, timedelta


app = Flask(__name__)

today = datetime.today()
todayString = datetime.strftime(today, "%Y-%m-%d")
yesterday = today - timedelta(days=1)
yesterdayString = datetime.strftime(yesterday, "%Y-%m-%d")

def filterDates(rawlines, start, end):
	startDate = datetime.strptime(start, "%Y-%m-%d")
	endDate = datetime.strptime(end, "%Y-%m-%d")
	endDate = endDate + timedelta(days=1) # Because you want until 23:59 on the end date

	dates = [i.split('\t')[0] for i in rawlines]
	parsedDates = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in dates]

	truth = [startDate <= day <= endDate for day in parsedDates]
	matchingLines = [rawlines[i] for i in range(len(truth)) if truth[i]]
	return matchingLines


@app.route('/log', methods=['GET'])
def makelog():
	startParam = request.args.get('start', yesterdayString)
	endParam = request.args.get('end', todayString)

	with open('./datalog.txt','r') as file:
		data = file.readlines()
	filteredLines = filterDates(data, startParam, endParam)
	# Ignore error outputs to log, just in case
	def isTrueLine(line):
		pattern = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\t(?!-999)[\d\.]{0,5}(?!-999)\t[\d\.]{0,5}')
		return bool(pattern.search(line))
	truelines = [line for line in filteredLines if isTrueLine(line)] # Is this even necessary?
	finaldata = ''.join(truelines)
	header = 'time\ttemp\thum\n'
	return header + finaldata


@app.route('/errlog', methods=['GET'])
def makeErrlog():
	startParam = request.args.get('start', yesterdayString)
	endParam = request.args.get('end', todayString)

	with open('./errorlog.txt') as file:
		data = file.readlines()
	filteredLines = filterDates(data, startParam, endParam)
	truelines = [line for line in filteredLines]
	finaldata = ''.join(truelines)
	header = 'time\ttemp\thum\n'
	return header + finaldata


@app.route('/')
def index():
	return render_template('./index.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

