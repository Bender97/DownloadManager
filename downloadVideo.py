from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import os

def downloadVideo(driver, video):
	
	for video_cont in range(len(video)):

		driver.get(video[video_cont])
		time.sleep(10)

		driver.switch_to.frame(driver.find_element_by_id("contentframe"))
		driver.switch_to.frame(driver.find_element_by_id("kplayer_ifp"))

		elem = driver.find_element_by_id("pid_kplayer")

		url = elem.get_attribute("src")

		driver.switch_to.default_content()


		os.system("ffmpeg -i \"" + url + "\" -codec copy video/" + str(video_cont).zfill(2) + "-" + driver.title.replace(" ", "_") + ".mp4")
