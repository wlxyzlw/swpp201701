#!/usr/bin/python3
import time
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

if len(sys.argv) != 2:
	print("checker1.py <url>")
	exit(1)

def check(driver, name):
	try:
		itm = driver.find_element_by_id(name)
	except NoSuchElementException:
		print("Cannot find %s" % name)
		exit(1)

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
driver.get(sys.argv[1])

check(driver, 'status_label')
check(driver, 'restart')
for i in range(0, 19):
	for j in range(0, 18):
		check(driver, "{0}_{1}".format(i, j))
driver.quit()
print("Successful!")
