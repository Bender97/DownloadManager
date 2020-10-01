from selenium import webdriver

from ssologin import SSOLogin
from Download import Download
from parsePage import parsePage, printElements, parsePage_MoodleSimulator
from setAndCreateFirefoxProfile import setAndCreateFirefoxProfile
#from UI import UI
from UI_MoodleSimulator import UI

import os
import pickle

path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"
fp = setAndCreateFirefoxProfile()


driver = None
#courseURL = "https://elearning.dei.unipd.it/course/view.php?id=4476"
courseURL = "https://elearning.unipd.it/chimica/course/view.php?id=603"

#ssologin = SSOLogin(driver)
#ssologin.login(courseURL)
	
#elements = parsePage(driver, courseURL)

elements = None

if (not os.path.isfile("elements.pkl")):
	driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)
	ssologin = SSOLogin(driver)
	ssologin.login(courseURL)
	elements = parsePage_MoodleSimulator(driver, courseURL)
	with open("elements.pkl", "wb") as f:
		pickle.dump([elements], f)
else:
	with open("elements.pkl", "rb") as f:
		elements = pickle.load(f)[0]

ui = UI(elements)
#selection = ui.UI_CategorySorted()
selection = ui.UI_MoodleSimulator()

download = Download()
download.download(driver, selection)

driver.quit()