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
			if is_end_check(i, j, 1, 0) or is_end_check(i, j, 0, 1) or is_end_check(i, j, 1, 1):
				return pane[i][j]
	return 0

def findGoodPlace(isO, step):
	# Is there winning position?
	for i in range(0, 19):
		for j in range(0, 19):
			if pane[i][j] != 0:
				continue
			pane[i][j] = 1 if isO else 2
			for (diri, dirj) in [(1, 0), (0, 1), (1, 1)] :
				for t in range(0, 5) :
					if is_end_check(i - diri * t, j - dirj * t, diri, dirj):
						# found!
						pane[i][j] = 0
						return (i, j)
			pane[i][j] = 0
	# do randomly..
	while True:
		(i, j) = (randint(0, 18), randint(0, 18))
		if pane[i][j] != 0:
			continue
		# place stone nearby enemy's / my stone
		if step == 0:
			# the first stone! there's no such thing
			return (i, j)
		found = False
		for di in [-1, 0, 1] :
			if (i + di) < 0 or 19 <= (i + di):
				continue
			for dj in [-1, 0, 1]:
				if (j + dj) < 0 or 19 <= (j + dj):
					continue
				if pane[i + di][j + dj] != 0:
					found = True
					break
		if not found: continue
		return (i, j)

def place_randomly(isO, step, easyGame):
	(i, j) = (0, 0)
	if easyGame:
		(i, j) = (18 - int(step % 2), 18 - int(step / 2))
	else:
		(i, j) = findGoodPlace(isO, step)
	
	if isO:
		pane[i][j] = 1
	else:
		pane[i][j] = 2
	return (i, j)

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

# param easyGame : trivial game (total 9-turns, O wins)
def play_game(easyGame):
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

		(i, j) = place_randomly(isO, step, easyGame)
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

play_game(True)
play_game(True) # Run twice

driver.quit()
print("Successful!")
