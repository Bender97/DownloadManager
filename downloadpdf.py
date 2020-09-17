from printProgress import printProgress

import requests
import time
import os

def getTitle(src):
	print(src)
	pattern="<title>"
	start = 0
	for i in range(len(src)):
		if src.startswith(pattern, i):
			start = i+7
			break
	pattern = "</title>"
	end = 0
	for i in range(len(src)):
		if src.startswith(pattern, i):
			end = i
			break
	return src[start:end]


def downloadpdf(driver, resources):

	with requests.Session() as s:

		for cookie in driver.get_cookies():
		    c = {cookie['name']: cookie['value']}
		    s.cookies.update(c)

		chunk_size = 2000
		for i, res in enumerate(resources):

			r = s.get(res[1], stream=True)
			time.sleep(2)
			filename = "pdf/" + str(i).zfill(2) + res[0].replace(" ", "_").replace("/", "-") + ".pdf"
			with open(filename, "wb") as fd:
				for chunk in r.iter_content(chunk_size):
					fd.write(chunk)
			printProgress(i, len(resources))

