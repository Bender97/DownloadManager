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
#courseURL = "https://elearning.dei.unipd.it/course/view.php?id=4476"
courseURL = "https://elearning.unipd.it/chimica/course/view.php?id=603"

elements = None

if useDriver:
	driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)
	ssologin = SSOLogin(driver)
	ssologin.login(courseURL)

if (not os.path.isfile("elements.pkl")):
	elements = parsePage(driver, courseURL)
	with open("elements.pkl", "wb") as f:
		pickle.dump(elements, f)
else:
	with open("elements.pkl", "rb") as f:
		elements = pickle.load(f)

ui = UI(elements, mode = MODE)
#ui = UI(elements, mode = MOODLESIMULATOR)

selection = ui.performSelection()

download = Download(driver, selection)
download.download(selection)

if useDriver:
	#updateCookies
	cookies = driver.get_cookies()
	with open("driver.pkl", "wb") as f:
			pickle.dump([time.time(), cookies], f)
	driver.quit()