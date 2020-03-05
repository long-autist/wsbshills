"""
wsbshills.py

Analyze hot posts from WSB over the last 24 hours and their top-level
comments to try to determine the most-shilled ticker symbols and their
overall sentiment.

Requires praw, numpy, configparser

Joshua Moore 2020
"""

import praw
import numpy
import configparser

import sys
import os
import time

# bot config file
CONFIGFILE = "config.ini"

username = None
password = None
clientid = None
clientsecret = None

# subreddit to analyze
SUB = "wallstreetbets"

# number of hot threads to query
NUM_THREADS = 20

# ticker CSV
TICKERFILE = "SP500.csv"
# additional symbols (like ETFs, etc) - one per line
ADDL_SYMS = "ADDL_SYMS.txt"

# positive sentiment keywords
POS_SENT = ["buy", "call", "bull", "moon"]
# negative sentiment keywords
NEG_SENT = ["sell", "put", "bear", "drill"]

# dictionary that will contain tickers and their calculated results
tickers = {}

# name of output file for analysis
OFILE = "result"

def analyze_comment(comment):
	"""
	Analyze a single comment to determine which stocks it shills, as well as
	its overall sentiment.
	"""
	for symbol in tickers:
		# get symbol mentions
		clower = comment.lower()
		if (" " + symbol.lower() + " ") in clower or\
		  ("$" + symbol.lower()) in clower:
			poscount = 0
			negcount = 0

			for s in POS_SENT:
				if s in comment:
					poscount = poscount + 1

			for s in NEG_SENT:
				if s in comment:
					negcount = negcount + 1

			tickers[symbol] = tuple(numpy.add(tickers[symbol], (1, poscount, negcount)))

def analyze_thread(thread):
	"""
	Analyze the OP as well as all top-level comments from a thread.
	"""
	print(thread.title)
	analyze_comment(thread.selftext)
	thread.comments.replace_more(limit = 0)
	for comment in thread.comments.list():
		analyze_comment(comment.body)

if __name__ == "__main__":
	# parse bot config file
	configp = configparser.ConfigParser()
	configp.read(CONFIGFILE)

	if 'auth' not in configp.sections():
		print("ERROR: auth section not found in " + CONFIGFILE)
		sys.exit(1)

	username = configp['auth']['username']
	password = configp['auth']['password']
	clientid = configp['auth']['clientid']
	clientsecret = configp['auth']['clientsecret']

	# load tickers
	with open(TICKERFILE) as f:
		for line in f.readlines():
			t = line.split(',')[0]
			# mentions, positive, negative
			tickers[t] = (0, 0, 0)

	# load additional symbols (like ETFs, etc)
	with open(ADDL_SYMS) as f:
		for line in f.readlines():
			tickers[line.rstrip()] = (0, 0, 0)

	reddit = praw.Reddit(client_id=clientid,
		     client_secret=clientsecret,
		     username=username,
		     password=password,
		     user_agent='wsb shills')

	print("Authenticated " + str(reddit.user.me()))

	for submission in reddit.subreddit(SUB).hot(limit=NUM_THREADS):
		if time.time() - submission.created_utc < 24*60*60:
			analyze_thread(submission)
			# keep in mind API rate limits
			time.sleep(4)

	# sort tickers, dropping tickers not mentioned
	results = []
	for sym in tickers:
		vals = tickers[sym]
		if vals[0] == 0:
			continue
		results.append((sym, vals[0], vals[1], vals[2]))

	results = sorted(results, key=lambda x: x[1])
	
	print("\nWriting results to '" + OFILE + "'...")

	if os.path.isfile(OFILE):
		os.remove(OFILE)
	with open(OFILE, "w") as f:
		for r in reversed(results):
			f.write(str(r) + "\n")
