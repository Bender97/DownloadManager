from waitForElement import waitForElement
from OSUtilities import checkAndMkDir

import time
import os

def handleYoutubeVideo(driver, filename):
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
	else:
		print("VideodDownload failed for filename: " + filename)
		driver.quit()
		exit()

def handleKalturaVideo(url, filename):
	
	print(url)
	print(filename)
	print("ffmpeg -i \"" + url + "\" -codec copy \"" + filename + "\" > /dev/null 2>&1")
	#f = open(filename, "w")
	#f.write(url)
	#f.close()
	# TODO sopprimere output di ffmpeg
	os.system("ffmpeg -i \"" + url + "\" -codec copy \"" + filename + "\"")

def getMoodleVideoElementURL(driver):
	waitForElement(driver, 'contentframe', timeout = 2)
	driver.switch_to.frame(driver.find_element_by_id("contentframe"))
	waitForElement(driver, 'kplayer_ifp')
	driver.switch_to.frame(driver.find_element_by_id("kplayer_ifp"))
	waitForElement(driver, 'pid_kplayer')
	elem = driver.find_element_by_id("pid_kplayer")
	url = elem.get_attribute("src")
	return url

def getMediaSpaceVideoElementURL(driver):
	waitForElement(driver, 'kplayer_ifp')
	driver.switch_to.frame(driver.find_element_by_id("kplayer_ifp"))
	waitForElement(driver, 'pid_kplayer')
	elem = driver.find_element_by_id("pid_kplayer")
	url = elem.get_attribute("src")
	return url

def downloadAVideo(driver, video, path="", fileindex = ""):

	driver.get(video.link)
	filename = path + ((fileindex.zfill(2) + " - ") if fileindex!="" else "") + driver.title + ".mp4"
	#print(filename)
	#driver.quit()
	#exit()
	if '/url/' in video.link:
		url = getMediaSpaceVideoElementURL(driver)
	else:
		url = getMoodleVideoElementURL(driver)

	if (url==""):
		handleYoutubeVideo(driver, filename)#.blob
	else:
		handleKalturaVideo(url, filename)	#.m3u8

	driver.switch_to.default_content()