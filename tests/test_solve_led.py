#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `solve_led` package."""


import pytest

from solve_led import solve_led


def test_get_local_data():

	path = './tests/no_file'
	assert solve_led.get_local_data(path) == False
	path = './tests/test_file.txt'
	content = 'switch 109,360 through 331,987'
	assert solve_led.get_local_data(path) == content


def test_get_net_data():
	url = 'http://claritytrec.ucd.ie/~alawlor/comp30670/input_assign3_d.txt'
	assert solve_led.get_net_data(url).replace('\n',';').split(';')[0] == '1000'
	assert solve_led.get_net_data(url).replace('\n',';').split(';')[1] == 'switch 109,360 through 331,987'
	assert solve_led.get_net_data(url).replace('\n',';').split(';')[-2] == 'turn off 81,52 through 255,768'

def test_valid():
	# This is corrct input 
	input = 'turn on 5,5 through 10,10'
	assert solve_led.valid(input) == ('turn on', '5', '5', '10', '10')

	input = 'switch 5,5 through 10,10'
	assert solve_led.valid(input) == ('switch', '5', '5', '10', '10')

	input = 'turn off 5,5 through 10,10'
	assert solve_led.valid(input) == ('turn off', '5', '5', '10', '10')