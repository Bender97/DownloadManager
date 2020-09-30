from downloadVideo import downloadVideo
from downloadResources import downloadResources

import os

def checkAndMkDir(path, name):
	if not os.path.isdir(path + "/" + name):
		os.mkdir(path + "/" + name)

class Download:
	def __init__(self):
		self.currentpath = ""
		self.previouspath = ""

	def download(self, driver, elements, name = ""):

		self.previouspath = self.currentpath

		if name=="":
			self.currentpath = os.getcwd()
		else:
			self.currentpath = name

		if (len(elements.resource)>0):
			downloadResources(driver, elements.resource, path = self.currentpath)
		
		if (len(elements.video)>0):
			downloadVideo(driver, elements.video, path = self.currentpath)

		for sub in elements.subfolder:
			checkAndMkDir(self.currentpath, sub.title)
			self.download(driver, sub.elements, name = self.currentpath + "/" + sub.title)

		self.currentpath = self.previouspath