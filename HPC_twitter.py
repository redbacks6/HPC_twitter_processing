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

	t0 = time.time()

	mentions = {}
	hashtags = {}
	term = 'market'
	termcounter = 0

	with open(sys.argv[1]) as csvfile:
		
		tweetsreader = csv.DictReader(csvfile)

		for row in tweetsreader:
			rawtweet = json.loads(row['value'])
			
			#casefold to lowercase
			tweettext = rawtweet['text'].lower()

			#update term count
			termcounter += termcount(term, tweettext)

			#update mentions
			mentioncount(mentions, tweettext)
			
			#update hashtags
			hashtagcount(hashtags, tweettext)

	topmentions = [[doc, mentions[doc]] for doc in sorted(mentions, key = mentions.get, reverse = True)]
	tophashtags = [[doc, hashtags[doc]] for doc in sorted(hashtags, key = hashtags.get, reverse = True)]

	t1 = time.time()
	runtime = t1 - t0

	print '\nRuntime is %s seconds' %(runtime)

	with open(sys.argv[2], 'wb') as outputfile:
		
		outputfile.write('Top hashtags')
		for hashtag in tophashtags[:10]:
			outputfile.write('\n'+str(hashtag))

		outputfile.write('\n\nMost mentions')
		for mention in topmentions[:10]:
			outputfile.write('\n'+str(mention))
		
		outputfile.write('\n\ncount of %s is %s' %(term, termcounter))

	print 'Top hashtags'
	print pp(tophashtags[:10])
	print '\nMost mentions'	
	print pp(topmentions[:10])	
	print '\ncount of %s is %s' %(term, termcounter)





"""
Count the number of times a given term (word/string) appears. 
Input: str(term), document represented as [term1, term2, term3]
Output: int(count of term)
"""
def termcount(term, document):
	
	count = 0

	words = document.split()

	for word in words:
		if word == term:
			count += 1

	return count		


"""
Count the mentions for each Twitter user
Input: dictionary of mentions {username: int(countmentions)}
Output: Nil - modifies the mentions dictionary
"""
def mentioncount(mentions, document):
	# Rules on legal twitter names as per the link
	# https://support.twitter.com/articles/101299-why-can-t-i-register-certain-usernames
	re_mention = re.compile(ur'(?<=@)([\w\d_]{1,15})')

	mention_list = re_mention.findall(document)

	countitems(mentions, mention_list)

	pass	


"""
Count the Hashtags
Input: dictionary of hashtags {hashtag: int(counttags)}
Output: Nil - modifies the hashtags dictionary
"""
def hashtagcount(hashtags, document):
	# Rules on legal twitter names as per the link
	# https://support.twitter.com/articles/101299-why-can-t-i-register-certain-usernames
	re_hashtag = re.compile(ur'(?<=#)([\w\d_]+)')

	hashtag_list = re_hashtag.findall(document)

	countitems(hashtags, hashtag_list)

	pass	

"""
Ammends count values in dictionary based on words in array
"""
def countitems(dictionary, array):	

	for word in array:
		if word in dictionary:
			dictionary[word] += 1
		else:
			dictionary[word] = 1


# Run the Main Method
if __name__ == '__main__':
    main()