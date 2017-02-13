import json
import tweepy
from datetime import datetime
from time import sleep

def setupAPI(apikey, apisecret, token, tokensecret):
	auth = tweepy.OAuthHandler(apikey, apisecret)
	auth.set_access_token(token, tokensecret)
	api = tweepy.API(auth)
	return api

def generateTweets(validline, errorline, temprange, humrange, userlist):
	statuses = []
	pass # Use see whether error or valid is most recent. If error, only append error status
	# If valid is most recent, first append status with time, temp, hum.
	# Then use getPart() and isInRange() to tell whether anything is out of range.
	# If so, append an additional status.
	# If userlist is not blank, then @ all of them. Ensure not over 140 characters
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
		api = setupAPI(
			auth['ConsumerAPIkey'], 
			auth['ConsumerAPIsecret'], 
			auth['AccessToken'], 
			auth['AccessTokenSecret'])

		tweets = generateTweets(
			lastValidLine, 
			lastErrorLine, 
			config['TemperatureRange'], 
			config['HumidityRange'], 
			config['UserList'])

		if len(tweets) == 1:
			api.update_status(tweets[0])
		elif len(tweets) == 2:
			api.update_status(tweets[0])
			sleep(10)
			api.update_status(tweets[1])

if __name__ == '__main__':
	main()