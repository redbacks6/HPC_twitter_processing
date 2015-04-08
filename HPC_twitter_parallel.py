#!/usr/bin/env python
"""
Twitter processing scripts
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 8 April 2015
"""
import sys, csv, json, re, time
import numpy as np
from pprint import pprint as pp
from mpi4py import MPI

url = '/Users/lukejones/Desktop/University/cloud_computing/Twitter.csv'
urlout = '/Users/lukejones/Desktop/Twitter_out.txt'
edward_directory = '/home/projects/pMelb0243/data/Twitter.csv'

data = sys.argv[1]
output = sys.argv[2]
term = sys.argv[3]

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def main():
	t0 = time.time()

	fieldnames = ['id','flags','expiration','cas','value']

	mentions = {}
	hashtags = {}
	localcounter = 0

	with open(data, 'r') as csvfile:

		if rank == 0:
			tweetsreader = csv.DictReader(file_block(csvfile, size, rank))

		else:
			tweetsreader = csv.DictReader(file_block(csvfile, size, rank), fieldnames = fieldnames)

		for row in tweetsreader:
			rawtweet = json.loads(row['value'])
			#casefold to lowercase
			tweettext = rawtweet['text'].lower()
			#update term count
			localcounter += termcount(term, tweettext)
			#update mentions
			mentioncount(mentions, tweettext)
			#update hashtags
			hashtagcount(hashtags, tweettext)


	mentions_array = comm.gather(mentions, root = 0)
	hashtags_array = comm.gather(hashtags, root = 0)
	count_array = comm.gather(localcounter, root = 0)

	if rank == 0:

		mentions = merge_dictionaries(mentions_array)
		hashtags = merge_dictionaries(hashtags_array)
		total_count = merge_termcount(count_array)

		topmentions = [[mention, mentions[mention]] for mention in sorted(mentions, key = mentions.get, reverse = True)]
		tophashtags = [[hashtag, hashtags[hashtag]] for hashtag in sorted(hashtags, key = hashtags.get, reverse = True)]

		t1 = time.time()
		runtime = t1 - t0

		### Write to output file
		with open(output, 'w') as outputfile:
			
			outputfile.write('\nTop hashtags')
			for hashtag in tophashtags[:10]:
				outputfile.write('\n'+str(hashtag))

			outputfile.write('\n\nMost mentions')
			for mention in topmentions[:10]:
				outputfile.write('\n'+str(mention))
			
			outputfile.write('\n\ncount of %s is %s' %(term, total_count))

			outputfile.write('\nRuntime was %s seconds\n\n' %(runtime))

"""
Takes a list of dictionaries and merges into a master dictionary
Input: [dict1, dict2, etc]
		where dict1 is a dictionary of token counts, i.e.
		{'token': int(count)}

Output: Master dictionary of token counts {'token': int(total_count)}
"""
def merge_dictionaries(dictonaries):

	master_dict = {}
	for dictionary in dictonaries:
		for token in dictionary:
			if token in master_dict:
				master_dict[token] += dictionary[token]
			else: master_dict[token] = dictionary[token]
			
	return master_dict			

def merge_termcount(terms_array):
	total = 0
	for term in terms_array:
		total += term
	return total

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

"""
count lines in a csv file
Input: link to csv file
Output: int(number of lines)
"""
def count_lines(csvfile):
	
	no_lines = 0

	with open(csvfile, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			no_lines += 1

	return no_lines

def file_block(fp, number_of_blocks, block):
    '''
    A generator that splits a file into blocks and iterates
    over the lines of one of the blocks.
    Borrowed from:
    https://xor0110.wordpress.com/2013/04/13/how-to-read-a-chunk-of-lines-from-a-file-in-python/
    '''
 
    assert 0 <= block and block < number_of_blocks
    assert 0 < number_of_blocks
 
    fp.seek(0,2)
    file_size = fp.tell()
 
    ini = file_size * block / number_of_blocks
    end = file_size * (1 + block) / number_of_blocks
 
    if ini <= 0:
        fp.seek(0)
    else:
        fp.seek(ini-1)
        fp.readline()
 
    while fp.tell() < end:
        yield fp.readline()

# Run the Main Method
if __name__ == '__main__':
    main()