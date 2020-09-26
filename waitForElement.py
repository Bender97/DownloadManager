from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from printProgress import printProgress
import time
import os

def waitForElement(driver, id):
	timeout = 10
	try:
		check = EC.presence_of_element_located((By.ID, id))
		WebDriverWait(driver, timeout).until(check)
		#print("Page Loaded!")
	except TimeoutException:
		print("Timeout exception while waiting for id: " + id)