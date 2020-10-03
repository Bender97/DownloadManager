from selenium import webdriver

from ssologin import SSOLogin
from Download import Download
from parsePage import parsePage
from setAndCreateFirefoxProfile import setAndCreateFirefoxProfile
#from UI import UI
from UI import UI

from config import *

import os
import pickle
import time
path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"
fp = setAndCreateFirefoxProfile()

driver = None
#courseURL = "https://elearning.dei.unipd.it/course/view.php?id=4476"	#
#courseURL = "https://elearning.unipd.it/chimica/course/view.php?id=603" #chimica
#courseURL = "https://elearning.unipd.it/dii/course/view.php?id=2189" #azionamenti
#courseURL = "https://elearning.dei.unipd.it/course/view.php?id=6808" # sistemi distribuiti
courseURL = "https://elearning.dei.unipd.it/course/view.php?id=6465" # game theory
#courseURL = "https://elearning.unipd.it/math/course/view.php?id=649" # cryptography
elements = None

if useDriver:
	driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)
	ssologin = SSOLogin(driver)
	ssologin.login(courseURL)

if (not os.path.isfile("elements.pkl")):
	elements = parsePage(driver, courseURL)
	with open("elements.pkl", "wb") as f:
		pickle.dump([courseURL, elements], f)
else:
	with open("elements.pkl", "rb") as f:
		url, elements = pickle.load(f)
		if (url!=courseURL):
			elements = parsePage(driver, courseURL)

ui = UI(elements, mode = MODE)


selection = ui.performSelection()
#page-header
#download = Download(driver, selection, target_folder_name="DINAMICA DEGLI AZIONAMENTI 2020-2021 - INP8085220")
download = Download(driver, selection, target_folder_name="/GAME THEORY/")
download.download(selection)

if useDriver:
	#updateCookies
	cookies = driver.get_cookies()
	with open("driver.pkl", "wb") as f:
			pickle.dump([time.time(), cookies], f)
	driver.quit()