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
from setAndCreateFirefoxProfile import setAndCreateFirefoxProfile

path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"

fp = setAndCreateFirefoxProfile()
driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)

courseURL = "https://elearning.dei.unipd.it/course/view.php?id=4476"

SSOLogin(driver, courseURL)

elements = parsePage(driver, courseURL)

#downloadVideo(driver, elements.video)
downloadpdf(driver, elements.resource)

driver.quit()