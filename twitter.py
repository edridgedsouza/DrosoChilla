import json
import tweepy
from datetime import datetime

def setupAPI(apikey, apisecret, token, tokensecret):
	auth = tweepy.OAuthHandler(apikey, apisecret)
	auth.set_access_token(token, tokensecret)
	api = tweepy.API(auth)
	return api

def generateTweets(validline, errorline):
	pass # Use see whether error or valid is most recent. If error, only update status with error.
	# If valid is most recent, first make update status with time, temp, hum.
	# Then use getPart() and isInRange() to tell whether anything is out of range.
	# If so, construct an additional status. Post that after.
	# Return an array of either 1 or 2 strings.

def getLastLine(filename):
	with open(filename, 'r') as file:
		lines = file.readlines()
	return lines[-1]

def getPart(line, part):
	parts = line.split('\t')
	if part == 'time':
		return parts[0]
	elif part == 'temp':
		return float(parts[1])
	elif part == 'hum':
		return float(parts[2])

def isInRange(reading, rangeArray):
	reading = float(reading)
	if any(rangeArray):
		return rangeArray[0] < reading < rangeArray[1]
	else:
		return True # For our purposes, a temperature is in range if we don't specify a range

def main():
	with open('twitter.json') as datafile:
		config = json.load(datafile)	

	lastValidLine = getLastLine('datalog.txt')
	lastErrorLine = getLastLine('errorlog.txt')

	if config['UseTwitter']:
		auth = config['TwitterAuthInfo']
		api = setupAPI(auth['ConsumerAPIkey'], auth['ConsumerAPIsecret'], auth['AccessToken'], auth['AccessTokenSecret'])

		# Make first tweet displaying time, temp, hum, every time called
		# Make another tweet if out of temperature range
		# Make another tweet if out of humidity range
		# api.update_status(statusstring)

if __name__ == '__main__':
	main()