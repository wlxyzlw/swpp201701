#!/usr/bin/python3
import time
import sys
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

if len(sys.argv) != 2:
	print("checker2.py <url>")
	exit(1)

pane = None

def init_pane():
	global pane
	pane = []
	for i in range(0, 19):
		pane.append([0] * 19)	

def is_end_check(begi, begj, di, dj):
	if begi < 0 or begj < 0:
		return False
	v = pane[begi][begj]
	if v == 0:
		return False
	for k in range(0, 4):
		begi = begi + di
		begj = begj + dj
		if 19 <= begi or 19 <= begj:
			return False
		if pane[begi][begj] != v:
			return False
	return True

def is_end():
	for i in range(0, 19):
		for j in range(0, 19):
			if pane[i][j] == 0:
				continue
			if is_end_check(i, j, 1, 0) or is_end_check(i, j, 0, 1) or is_end_check(i, j, 1, 1) or is_end_check(i, j, 1, -1) :
				return pane[i][j]
	return 0

def place(isO, i, j):
	if isO:
		pane[i][j] = 1
	else:
		pane[i][j] = 2

def get_char(i, j):
	if pane[i][j] == 0:
		return '-'
	elif pane[i][j] == 1:
		return 'O'
	return 'X'

def check_value(driver, name, val):
	try:
		itm = driver.find_element_by_id(name)
		if itm.text.lower() != val.lower():
			print("{0}'s value must be {1}, not {2}".format(name, val, itm.text))
			exit(1)
	except NoSuchElementException:
		print("Cannot find %s" % name)
		exit(1)

def click(driver, name):
	print("Click {0}".format(name))
	driver.find_element_by_id(name).click()

def check_pane(driver):
	for i in range(0, 19):
		for j in range(0, 19):
			check_value(driver, "{0}_{1}".format(i, j), get_char(i, j))

def play_game(schedule):
	print("============ Start simulation ===========")
	click(driver, 'restart')
	init_pane()
	check_pane(driver)
	isO = True
	step = 0
	while is_end() == 0:
		if isO:
			check_value(driver, 'status_label', 'Next O')
		else:
			check_value(driver, 'status_label', 'Next X')

		(i, j) = schedule[step]
		place(isO, i, j)
		if isO:
			print("Placing O to ({0}, {1})..".format(i, j))
		else:
			print("Placing X to ({0}, {1})..".format(i, j))
		click(driver, "{0}_{1}".format(i, j))
		check_pane(driver)
		isO = not isO
		step = step + 1

	# Who's won?
	if is_end() == 1:
		# O won
		check_value(driver, 'status_label', 'O win')
	else:
		# X won
		check_value(driver, 'status_label', 'X win')

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
driver.get(sys.argv[1])

schedules = [
# horizontal, O win / X win
[], [],
# vertical, O win / X win
[], [],
# (+1, +1), O win / X win
[], [],
# (+1, -1), O win / X win
[], []
]

for i in range(0, 5):
	schedules[0].append((18, 18 - i))
	schedules[0].append((17, 18 - i))
	schedules[2].append((18 - i, 18))
	schedules[2].append((18 - i, 17))
	schedules[4].append((18 - i, 18 - i))
	schedules[4].append((17 - i, 18 - i))
	schedules[6].append((18 - i, 14 + i))
	schedules[6].append((18 - i, 13 + i))
schedules[1] = [(0, 0)] + schedules[0]
schedules[3] = [(0, 0)] + schedules[2]
schedules[5] = [(0, 0)] + schedules[4]
schedules[7] = [(0, 0)] + schedules[6]

for schedule in schedules:
	play_game(schedule)

driver.quit()
print("Successful!")
