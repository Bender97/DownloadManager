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


def downloadResources(driver, resources, path=""):

	# CHECK IF FOLDER EXISTS. IF NOT: MKDIR
	if not os.path.isdir(path + '/pdf'):
		os.mkdir(path + '/pdf')

	printProgress(0, len(resources), msg="[res]")

	with requests.Session() as session:

		for cookie in driver.get_cookies():
		    c = {cookie['name']: cookie['value']}
		    session.cookies.update(c)

		chunk_size = 2000
		for i, res in enumerate(resources):

			r = session.get(res.link, stream=True)
			time.sleep(2)
			filename = path + "/pdf/" + str(i).zfill(2) + res.title.replace(" ", "_").replace("/", "-") + ".pdf"
			with open(filename, "wb") as fd:
				for chunk in r.iter_content(chunk_size):
					fd.write(chunk)
			printProgress(i+1, len(resources), msg="[res]")