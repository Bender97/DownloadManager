from OSUtilities import checkAndMkDir

import requests
import time

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


def downloadAPDF(driver, pdf, path="", fileindex = ""):

	with requests.Session() as session:

		for cookie in driver.get_cookies():
		    c = {cookie['name']: cookie['value']}
		    session.cookies.update(c)

		chunk_size = 2000

		r = session.get(pdf.link, stream=True)
		time.sleep(2)
		filename = path + ((fileindex.zfill(2) + " - ") if fileindex!="" else "") + pdf.title.replace(" ", "_").replace("/", "-") + (".pdf" if pdf.title[-4:]!=".pdf" else "")
		print(filename)
		with open(filename, "wb") as fd:
			for chunk in r.iter_content(chunk_size):
				fd.write(chunk)