from selenium import webdriver

import time
import os

from printProgress import printProgress
from waitForElement import waitForElement


def downloadVideo(driver, video, path=""):

	# CHECK IF FOLDER EXISTS. IF NOT: MKDIR
	if not os.path.isdir(path + '/video'):
		os.mkdir(path + '/video')

	printProgress(0, len(video), msg="[vid]")

	for video_cont in range(len(video)):

		driver.get(video[video_cont].link)

		waitForElement(driver, 'contentframe')
		driver.switch_to.frame(driver.find_element_by_id("contentframe"))
		waitForElement(driver, 'kplayer_ifp')
		driver.switch_to.frame(driver.find_element_by_id("kplayer_ifp"))
		waitForElement(driver, 'pid_kplayer')
		elem = driver.find_element_by_id("pid_kplayer")

		url = elem.get_attribute("src")

		filename = path + "/video/" + str(video_cont).zfill(2) + "-" + driver.title.replace(" ", "_") + ".mp4"
		
		if (url==""): # IT'S YOUTUBE or DIFFERENT (blob)
			waitForElement(driver, 'player')
			flag = 1

			try:
				driver.switch_to.frame(driver.find_element_by_id("pid_kplayer"))
				flag = 0

				elem = driver.find_element_by_xpath("//a[@aria-label='Guarda su www.youtube.com']")
				link = elem.get_attribute("href")
				f = open(filename, "w")
				f.write(link)
				f.close()
			except:
				print("NO FRAME pid_kplayer")

			if (flag):
				src = driver.find_element_by_class_name('videoDisplay').get_attribute("innerHTML")
				print(src)
				flag = 0
			if (flag):
				print("I failed")
				driver.quit()
				exit()

		else:	 # IT's a classical hosted kaltura video (.m3u8)
			print("ffmpeg -i \"" + url + "\" -codec copy " + path + filename + " > /dev/null 2>&1")
			#os.system("ffmpeg -i \"" + url + "\" -codec copy " + path + filename + " > /dev/null 2>&1")
		
		printProgress(video_cont+1, len(video), msg="[vid]")

		driver.switch_to.default_content()