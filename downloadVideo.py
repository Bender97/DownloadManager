from selenium import webdriver

import time
import os

from printProgress import printProgress
from waitForElement import waitForElement


def downloadVideo(driver, video):
	# CHECK IF FOLDER EXISTS. IF NOT: MKDIR
	if not os.path.isdir('video'):
		os.mkdir('video')
	printProgress(0, len(video))


	video_cont = 2

	#for video_cont in range(len(video)):

	driver.get(video[video_cont])
	
	#WAIT FOR
	

	waitForElement(driver, 'contentframe')
	driver.switch_to.frame(driver.find_element_by_id("contentframe"))
	waitForElement(driver, 'kplayer_ifp')
	driver.switch_to.frame(driver.find_element_by_id("kplayer_ifp"))
	waitForElement(driver, 'pid_kplayer')
	elem = driver.find_element_by_id("pid_kplayer")

	#print("-------innerHTML-----------\n" + elem.get_attribute("innerHTML") + "\n------------------------------------")

	#print("-------pageSource-----------\n" + driver.page_source + "\n------------------------------------")

	#print("-------justToTry-----------\n" + driver.get_attribute("src") + "\n------------------------------------")

	url = elem.get_attribute("src")

	filename = "video/" + str(video_cont).zfill(2) + "-" + driver.title.replace(" ", "_") + ".mp4"
	
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

	else:	 # IT's classical kaltura video hosted (.m3u8)
		print("ffmpeg -i \"" + url + "\" -codec copy " + filename + " > /dev/null 2>&1")
	
	printProgress(video_cont+1, len(video))

	driver.switch_to.default_content()
	


	#os.system("ffmpeg -i \"" + url + "\" -codec copy video/" + str(video_cont).zfill(2) + "-" + driver.title.replace(" ", "_") + ".mp4 > /dev/null 2>&1")
	