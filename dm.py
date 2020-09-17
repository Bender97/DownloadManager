from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import os

from ssologin import SSOLogin
from downloadVideo import downloadVideo
from downloadpdf import downloadpdf
from Elements import Elements
from parsePage import parsePage

path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"

fp = webdriver.FirefoxProfile()
mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("plugin.scan.plid.all", False)
#fp.set_preference("plugin.scan.Acrobat", 99.0)
fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
fp.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)

SSOLogin(driver)

courseURL = ""
elements = parsePage(driver, courseURL)

'''
for link in elements.video:
	print(link)

print(len(elements.video))

for link in elements.resource:
	print(link)

print(len(elements.resource))'''

#downloadVideo(driver, elements.video)
downloadpdf(driver, elements.resource)

driver.quit()