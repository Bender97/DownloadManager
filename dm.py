from selenium import webdriver

from ssologin import SSOLogin
from Download import Download
from parsePage import parsePage

from createDriver import createDriver
from UI import UI
from CourseChoice import CourseChoice

from config import *

import os
import pickle
import time

driver = None

elements = None

courseURL = CourseChoice().getCourseURL()
#courseURL = "https://elearning.unipd.it/chimica/course/view.php?id=603"

if useDriver:
	driver = createDriver()
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
			with open("elements.pkl", "wb") as f:
				pickle.dump([courseURL, elements], f)

ui = UI(elements, mode = MODE)

selection = ui.performSelection()

download = Download(driver, selection, target_folder_name="/" + elements[0].title + "/")
download.download(selection)

if useDriver:
	#updateCookies
	cookies = driver.get_cookies()
	with open("driver.pkl", "wb") as f:
			pickle.dump([time.time(), cookies], f)
	driver.quit()