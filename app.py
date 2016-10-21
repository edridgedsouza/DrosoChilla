#! /usr/bin/env python3
# Flask web app

from flask import Flask, render_template
import re


app = Flask(__name__)


@app.route('/log')
def makelog():
	header = 'time\ttemp\thum\n'
	LINES = 500
	with open('./templog.txt','r') as file:
		data = file.readlines()
	# Ignore error outputs to log
	def isTrueLine(line):
		pattern = re.compile('.*\\t.*\\t.*')
		return bool(pattern.search(line))
	truelines = [line for line in data if isTrueLine(line)]
	finaldata = ''.join(truelines)
	return header + finaldata

@app.route('/')
def index():
	return render_template('./index.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

