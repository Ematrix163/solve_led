#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
3rd Mar 2018
@author: Chen Yiming
'''

# import related package

# import time to count the running time
import time 
import os
# I use numpy package here because it was written in C and its operations on array is very fast
import numpy as np

import sys
import getopt
import requests
import re

def get_net_data(url):
	'''
	This function is to get network data and return it.
	'''
	try:
		content = requests.get(url).text
		return content
	except:
		print('Cannot find the url! Please check!')
		return False


def get_local_data(path):
	'''
	This file is to get the local file data and return it
	'''
	if (os.path.exists(path)):
		with open(path) as f:
			content = f.read()
			return content
	else:
		print('Cannot find the file! Please check!')
		return False

def execute(content):
	'''
	This is the main function of the program. 
	'''
	content = content.replace('\n',';').split(';')
	lines = int(content[0])

	#  initialise numpy array, the size is lines * lines, type is bool
	led = np.zeros((lines,lines),dtype = bool)

	# traverse each line of the instructions
	for each in content[1:-1]:

		# use valid function to check whether this instruction is valid
		results = valid(each)

		# if it is valid
		if results:
			x1 = int(results[1])
			y1 = int(results[2])
			x2 = int(results[3])
			y2 = int(results[4])

			# Here we have to consider about the the point may goes from higher to lower or lower to higher
			# so we have to judege the situation and handle it
			if (x1 > x2):
				x1, x2 = x2, x1
			if (y1 > y2):
				y1, y2 = y2, y1

			# sometiems there may be some negative numbers, we have to assign 0 to them
			if (x2 > 0 and y2 > 0 and (x1 < 0 or y1 < 0)):
				x1 = max(0, x1)
				y1 = max(0, y1)

			if (results[0] == 'turn on'):
				# The range of every point is [0,lines-1]
				led[x1:x2+1, y1:y2+1] = True

			elif (results[0] == 'turn off'):
				# turn_on(x1, y1, x2, y2)
				led[x1:x2+1, y1:y2+1] = False

			elif results[0] == 'switch':
				led[x1:x2+1, y1:y2+1] = np.invert(led[x1:x2+1, y1:y2+1])


	outcome = led.sum()
	# Print the outcome
	print('%d lights are on after executing the instructions.' % outcome)
	return outcome



def valid(input):
	'''
	This function is to valid the correct format of a single instruction.
	If correct, return a list otherwise return False.
	'''

	# regular expression
	compiled_pattern = re.compile('.*(turn on|turn off|switch)\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*through\s*([+-]?\d+)\s*,\s*([+-]?\d+).*')
	
	# check whether the input match regex and split it
	results = compiled_pattern.findall(input)
	if (results):
		return results[0]
	else:
		return False

def main():
	'''
	This is the main entrance of the program.
	'''
	start_time = time.time()
	
	try:
		options,args = getopt.getopt(sys.argv[1:],"in:", ["input="])
		for name,value in options:
			if name in ("-in","--input"):
				choose(value)
	except getopt.GetoptError:
		sys.exit()

	# print the running time
	print("----- The running time: %.2f seconds -----" % (time.time() - start_time))


def choose(path):
	'''
	The function is to judge whether a given path is a local path or network url
	'''

	if re.match(r'^http|ftp|https', path):
		# get network data
		content = get_net_data(path)
		if (content):
			execute(content)
	else:
		# get local file data
		content = get_local_data(path)
		if(content):
			execute(content)
	


if __name__ == "__main__":
	main()
