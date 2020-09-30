from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from printProgress import printProgress
import time
import os

def waitForElement(driver, modeinfo = "", mode = "id", timeout = 10):
	try:
		if mode=="id":
			check = EC.visibility_of_element_located((By.ID, modeinfo))
			WebDriverWait(driver, timeout).until(check)
		elif mode=="xpath":
			check = EC.visibility_of_element_located((By.XPATH, modeinfo))
			WebDriverWait(driver, timeout).until(check)
	except TimeoutException:
		print("Timeout exception while waiting for id: " + id)