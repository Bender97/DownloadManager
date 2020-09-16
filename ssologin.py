from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import os

def SSOLogin(driver):

	sso_path = "https://elearning.unipd.it/math/auth/shibboleth/index.php"

	start = time.time()

	driver.get(sso_path)
'''
	print("insert username: ")
	username = input()

	print("insert password: ")
	psw = input()
'''
	end = time.time()

	if (end-start<10):
		time.sleep(10-(end-start))

	elem = driver.find_element_by_id('j_username_js')
	#elem.clear()
	elem.send_keys('daniel.fusaro')
	#elem.send_keys(username)

	elem = driver.find_element_by_id('password')
	#elem.clear()
	elem.send_keys('Ilcielo3blu')
	#elem.send_keys(psw)

	elem = driver.find_element_by_id('radio2')
	elem.click()

	time.sleep(1)

	elem = driver.find_element_by_id('login_button_js')
	elem.click()

	time.sleep(2)
