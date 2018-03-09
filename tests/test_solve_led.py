#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `solve_led` package."""

# import test module
import pytest

# import solve_led module
from solve_led import solve_led


def test_get_local_data():

	# This is to test when the file doesn't exsist, the function should return false
	path = './tests/no_file'
	assert solve_led.get_local_data(path) == False

	# This is to test when the file exsists, the function should return its content
	path = './tests/test_file.txt'
	content = 'switch 109,360 through 331,987'
	assert solve_led.get_local_data(path) == content


def test_get_net_data():

	# This is to test whether the corrcet url work
	url = 'http://claritytrec.ucd.ie/~alawlor/comp30670/input_assign3_d.txt'
	assert solve_led.get_net_data(url).replace('\n',';').split(';')[0] == '1000'
	assert solve_led.get_net_data(url).replace('\n',';').split(';')[1] == 'switch 109,360 through 331,987'
	assert solve_led.get_net_data(url).replace('\n',';').split(';')[-2] == 'turn off 81,52 through 255,768'

	# This is to test when input an fake url, the get_net_data should return false
	fake_url = 'http://www.claritytrfgfdfdsfdsd.txt'
	assert solve_led.get_net_data(fake_url) == False

def test_valid():
	# This is corrct input 

	# When the input starts with turn on 
	input = 'turn on 5,5 through 10,10'
	assert solve_led.valid(input) == ('turn on', '5', '5', '10', '10')

	# When the input starts with switch 
	input = 'switch 5,5 through 10,10'
	assert solve_led.valid(input) == ('switch', '5', '5', '10', '10')

	# When the input starts with turn off
	input = 'turn off 5,5 through 10,10'
	assert solve_led.valid(input) == ('turn off', '5', '5', '10', '10')


def test_execute():

	# This is to test when If a command affects a region outside the area of the grid, 
	# then it will still be executed, but only on the region of lights inside the boundary of the grid.
	content = '10 \n turn on 5,5 through 5,5 \n switch 100,100 through 1099,1990 \n'
	assert solve_led.execute(content) == 1


	# If there is some negative in the input, the function should handle correctly
	content = '10 \n switch 5,5 through 12,13 \n switch 12,15 through 18,19 \n switch -1,-100 through 3,5 \n switch 5,15 through 6,11 \n'
	assert solve_led.execute(content) == 49

