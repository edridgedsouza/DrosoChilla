import json
import tweepy
from datetime import datetime


def generateTweet(validline, errorline):
	pass

def getLastLine(filename):
	with open(filename, 'r') as file:
		lines = file.readlines()
	return lines[-1]

def isInRange(reading, rangeArray):
	pass

def main():
	with open('twitter.json') as datafile:
		config = json.load(datafile)	

	lastValidLine = getLastLine('datalog.txt')
	lastErrorLine = getLastLine('errorlog.txt')

	if config['UseTwitter']:
		if config['TweetBehavior'] == 'regular':
			pass # Do it every time script is called
		elif config['TweetBehavior'] == 'warnings':
			pass # Do it only if the temp and hum are not in range


if __name__ == '__main__':
	main()