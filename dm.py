from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import os

from ssologin import SSOLogin

path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"

driver = webdriver.Firefox(executable_path = path_to_mozilladriver)

SSOLogin(driver)

f = open("src.txt", "r")

src = f.read()

'''sub = "Kaltura Video Resource"

res = [i for i in range(len(src)) if src.startswith(sub, i)] 

start = []
startsub = "onclick=\"\" href="

for pivot in res:
	for i in range(pivot, len(src)):
		if (src.startswith(startsub, i)):
			start.append(i+17)
			break
print(len(start))

#print(res)
#print(len(res))

end = []
endsub = "\"><img src"

for pivot in start:
	for i in range(pivot, len(src)):
		if (src.startswith(endsub, i)):
			end.append(i)
			break

#print(end)
#print(len(end))

for i in range(len(sub)):
	print(src[start[i]:end[i]])'''

sub = "href=\"https:"

res = [i+6 for i in range(len(src)) if src.startswith(sub, i)] 

print(len(res))

end = []
endsub = "\""

for pivot in res:
	for i in range(pivot, len(src)):
		if (src.startswith(endsub, i)):
			end.append(i)
			break

video = []

for i in range(len(res)):
	link = src[res[i]:end[i]]
	if "kalvidres" in link:
		video.append(link)

#for link in video:
#	print(link)

#print(len(video))

for video_cont in range(len(video)):

	driver.get(video[video_cont])
	time.sleep(10)

	driver.switch_to.frame(driver.find_element_by_id("contentframe"))
	driver.switch_to.frame(driver.find_element_by_id("kplayer_ifp"))

	elem = driver.find_element_by_id("pid_kplayer")

	url = elem.get_attribute("src")

	driver.switch_to.default_content()


	os.system("ffmpeg -i \"" + url + "\" -codec copy video/" + str(video_cont).zfill(2) + "-" + driver.title.replace(" ", "_") + ".mp4")


driver.quit()


f.close()