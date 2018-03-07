#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
3rd Mar 2018
@author: Chen Yiming
'''

# import related package

# import time to count the running time
import time 

# I use numpy package here because it was written in C and its operations on array is very fast
import numpy as np
import os
import sys
import getopt
import requests
import re

def get_net_data(url):
	'''
	This function is to get network data and return it.
	'''

	content = requests.get(url).text
	return content


def get_local_data(path):
	'''
	This file is to get the local file data and return it
	'''
	if os.path.exists(path):
		with open(path) as f:
			content = f.read()
			return content
	else:
		return False

