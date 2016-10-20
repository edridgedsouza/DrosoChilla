#! /usr/bin/env python3
# Flask web app

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/log')
def makelog():
	header = 'time\ttemp\thum\n'
	LINES = 500
	with open('./templog.txt','r') as file:
		data = file.read()
	return header + data

@app.route('/')
def index():
	return render_template('./index.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

