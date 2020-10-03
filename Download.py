from downloadAVideo import downloadAVideo
from downloadAPDF import downloadAPDF
from config import *
from OSUtilities import checkAndMkDir, getcwd
from progressBar import progressBar

class Download:
	def __init__(self, driver, elements, target_folder_name = "/chimica/"):
		self.driver = driver

		self.currentpath = ""
		self.previouspath = ""

		cont = len(elements)
		for elem in elements:
			if (elem.type==SUBFOLDER):
				cont+= len(elem.elements)-1

		self.progressBar = progressBar(cont)
		checkAndMkDir(getcwd(), target_folder_name)
		self.target_folder_name = getcwd() + target_folder_name

	def download(self, elements, path = "", fileindexoffset = 0):

		if (path!=""):
			checkAndMkDir("", path)

		for i, elem in enumerate(elements):
			if elem.type==PDF:
				downloadAPDF(self.driver, elem, path = (self.target_folder_name if path=="" else path), fileindex = str(i + fileindexoffset))
			elif elem.type==VIDEO:
				downloadAVideo(self.driver, elem, path = (self.target_folder_name if path=="" else path), fileindex = str(i + fileindexoffset))
			elif elem.type==SUBFOLDER:
				self.download(elem.elements, path = (self.target_folder_name + elem.title + "/"), fileindexoffset = i)
			self.progressBar.printProgress()