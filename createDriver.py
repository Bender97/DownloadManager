from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from config import *

def setAndCreateFirefoxProfile():
	fp = webdriver.FirefoxProfile()

	mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
	fp.set_preference("browser.download.manager.showWhenStarting", False)
	fp.set_preference("plugin.scan.plid.all", False)
	fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
	fp.set_preference("pdfjs.disabled", True)
	return fp

def setAndCreateChromeProfile():
	fp = webdriver.ChromeOptions() 

	mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
	fp.add_experimental_option("prefs", {
		"browser.helperApps.neverAsk.saveToDisk": mime_types,
		"browser.download.manager.showWhenStarting": False,
		"plugin.scan.plid.all": False,
		"plugin.disable_full_page_plugin_for_types": mime_types,
		"pdfjs.disabled": True
		})
	return fp

def createDriver():

	driver = None

	if PLATFORM=="Linux":
		path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"
		fp = setAndCreateFirefoxProfile()
		driver = driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)

	elif PLATFORM=="Windows":
		path_to_chromewebdriver = "C://Users//Daniel//Downloads//chromedriver.exe"
		driver = webdriver.Chrome(executable_path = path_to_chromewebdriver, chrome_options = fp)

	else:
		print("platform not supported")
		exit()

	return driver
