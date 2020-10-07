from selenium import webdriver

from Element import Element
from waitForElement import waitForElement
from config import *

def removeSpan(txt):
	pattern='<span'
	for i in range(0, len(txt)):
		if (txt.startswith(pattern, i)):
			return txt[0:i]

def findTitle(src, pivot, pattern = "instancename"):
	start = 0
	for i in range(pivot, len(src)):
		if (src.startswith(pattern, i)):
			start = i+14
			break
	pattern="</span"
	for i in range(start, len(src)):
		if (src.startswith(pattern, i)):
			if ("<span" in src[start:i]):
				return removeSpan(src[start:i])
			else:
				return src[start:i]

def printElement(elem):
	types = ["PDF", "ARCHIVE", "ZOOM", "VIDEO", "YOUTUBE", "SECTION", "SUBFOLDER"]
	print(types[elem.type] + " - " + elem.title)
	if (elem.link!=""):
		print(elem.link)
	print("-------")

def exploreSubFolders(driver, element):

	driver.get(element.link)
	waitForElement(driver, 'page-content')
	src = driver.page_source

	startPattern = "href=\"https:"
	startIndexes = [i+6 for i in range(len(src)) if src.startswith(startPattern, i)] 

	endPattern = "\""
	endIndexes = []

	for pivot in startIndexes:
		for i in range(pivot, len(src)):
			if (src.startswith(endPattern, i)):
				endIndexes.append(i)
				break

	elements = []

	for i in range(len(startIndexes)):
		link = src[startIndexes[i]:endIndexes[i]]
		if "/pluginfile.php/" in link:
			title = findTitle(src, endIndexes[i], pattern="\"fp-filename\"")
			obj = None
			if ".pdf" in title:
				obj = Element(PDF, title, link)
			elif ".zip" in title:
				obj = Element(ARCHIVE, title, link)
			elif ".mp4" in title:
				obj = Element(VIDEO, title, link)
			else:
				print("I found an unknown MIME extension: " + title)
			if obj!=None:
				elements.append(obj)
	element.elements = elements

def parsePage(driver, URL, level=0):			## LOOK ALSO FOR sectionname

	elements = []
	subfolders_cont = 0

	if (level!=0):
		print("press Enter to start parsing the subfolder...")
		input()
	
	driver.get(URL)
	
	waitForElement(driver, 'page-content')
	
	src = driver.page_source

	link_start_pattern = "href=\"https:"
	section_start_pattern="class=\"sectionname\""
	link_end_pattern = "\""
	section_end_pattern= "</span>"

	for i in range(len(src)):
		if src.startswith(link_start_pattern, i):
			for j in range(i+6, len(src)):
				if (src.startswith(link_end_pattern, j)):
					link = src[i+6:j]
					if (len(link)>300):
						print("ERROR: LINK LENGTH TOOOO LONG")
						print(link)
						driver.quit()
						exit()
					if "/kalvidres/" in link or '/url/' in link:
						title = findTitle(src, j)
						obj = Element(VIDEO, title, link)
						elements.append(obj)
					elif "/resource/" in link:
						title = findTitle(src, j)
						obj = Element(PDF, title, link)
						elements.append(obj)
					elif "/folder/" in link and link!=URL:
						subfolders_cont += 1
						title = findTitle(src, j)
						obj = Element(SUBFOLDER, title, link)
						elements.append(obj)
					break

		elif src.startswith(section_start_pattern, i):
			for j in range(i+26, len(src)):
				if (src.startswith(section_end_pattern, j)):
					title = src[i+26:j]
					if (len(title)>300):
						print("ERROR: TITLE LENGTH TOOOO LONG")
						driver.quit()
						exit()
					obj = Element(SECTION, title)
					elements.append(obj)
					break

	if level==0:
		for elem in elements:
			if elem.type==SUBFOLDER:
				exploreSubFolders(driver, elem)
				

	return elements