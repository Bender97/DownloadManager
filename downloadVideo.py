from printProgress import printProgress
from waitForElement import waitForElement
from OSUtilities import checkAndMkDir

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

def handleKalturaVideo(url, path, filename):
	print("ffmpeg -i \"" + url + "\" -codec copy " + filename + " > /dev/null 2>&1")
	f = open(filename, "w")
	f.write(url)
	f.close()
	# TODO sopprimere output di ffmpeg
	#os.system("ffmpeg -i \"" + url + "\" -codec copy " + path + filename + " > /dev/null 2>&1")

def getVideoElementURL(driver):
	waitForElement(driver, 'contentframe')
	driver.switch_to.frame(driver.find_element_by_id("contentframe"))
	waitForElement(driver, 'kplayer_ifp')
	driver.switch_to.frame(driver.find_element_by_id("kplayer_ifp"))
	waitForElement(driver, 'pid_kplayer')
	elem = driver.find_element_by_id("pid_kplayer")

	url = elem.get_attribute("src")

def downloadVideo(driver, video, path=""):

	checkAndMkDir(path, '/video')

	printProgress(0, len(video), msg="[vid]")

	for video_cont, vid in enumerate(video):

		driver.get(vid.link)
		filename = path + "/video/" + str(video_cont).zfill(2) + "-" + driver.title.replace(" ", "_") + ".mp4"

		url = getVideoElementURL(driver)

		if (url==""):
			handleYoutubeVideo(driver, filename)#.blob
		else:
			handleKalturaVideo(url, filename)	#.m3u8

		printProgress(video_cont+1, len(video), msg="[vid]")

		driver.switch_to.default_content()