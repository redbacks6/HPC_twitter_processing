#!/usr/bin/env python
"""
Twitter processing scripts
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 3 April 2015
"""
import sys, csv, json, re, time
from pprint import pprint as pp

url = '/Users/lukejones/Desktop/University/cloud_computing/Twitter.csv'
edward_directory = '/home/projects/pMelb0243/data/Twitter.csv'

def main():

	with open(url) as csvfile:
		
		tweetsreader = csv.DictReader(csvfile)

		for row in tweetsreader:
			print pp(json.loads(row['value']))
			
			# #casefold to lowercase
			# tweettext = rawtweet['text'].lower()


# Run the Main Method
if __name__ == '__main__':
    main()