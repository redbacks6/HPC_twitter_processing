"""
Twitter processing scripts
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 28 March 2015
"""
import csv
import json
from pprint import pprint as pp

url = '/Users/lukejones/Desktop/University/cloud_computing/Twitter.csv'

def main():

	with open(url) as csvfile:
		
		tweetsreader = csv.DictReader(csvfile)

		for row in tweetsreader:
			print pp(json.loads(row['value']))


"""
Count the number of times a given term (word/string) appears. 
Input: str(term), document represented as [term1, term2, term3]
Output: int(count of term)
"""
def termcount(term, document):
	count = 0

	for word in document:
		if word == term:
			count += 1

	return count		


"""
Count the mentions for each Twitter user
Input: dictionary of tweeters {username: int(countmentions)}
Output: Nil - modifies the tweeters dictionary
"""
def tweetercount(tweeters, document):
	# Rules on legal twitter names as per the link
	# https://support.twitter.com/articles/101299-why-can-t-i-register-certain-usernames
	re_mention = re.compile(ur'(?<=^@| @)([\w\d_]{1,15})')

	mention_list = re_mention.findall(document)

	for mention in mention_list:
		if mention in tweeters:
			tweeters[mention] += 1
		else:
			tweeters[mention] = 1

	pass	


"""
Count the Hashtags
Input: dictionary of hashtags {hashtag: int(counttags)}
Output: Nil - modifies the hashtags dictionary
"""
def tweetercount(hastags, document):
	# Rules on legal twitter names as per the link
	# https://support.twitter.com/articles/101299-why-can-t-i-register-certain-usernames
	re_hashtag = re.compile(ur'(?<=#)([\w\d_]*)')

	hashtag_list = re_hashtag.findall(document)

	for hashtag in hashtag_list:
		if hashtag in hashtags:
			hashtags[mention] += 1
		else:
			hashtags[mention] = 1

	pass	


# Run the Main Method
if __name__ == '__main__':
    main()