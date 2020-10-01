from selenium import webdriver

from Elements import Elements, simpleElement, subfolderElement, MoodleElement
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

def printElements(elements, level=0):

	if (len(elements.resource)>0):
		print("-"*(level*4) + " RESOURCES -------- " + str(len(elements.resource)))
		for res in elements.resource:
			print(res.title)
		print()

	if (len(elements.video)>0):
		print("-"*(level*4) + " VIDEOS ----------- " + str(len(elements.video)))
		for vid in elements.video:
			print(vid.title)
		print()
	
	if (len(elements.subfolder)>0):	
		print("-"*(level*4) + " SUBFOLDERS (" + str(len(elements.subfolder)) + ") ----------- ")
		for i, subfolder in enumerate(elements.subfolder):
			print("-"*(level*4+1) + "SUBFOLDER PROGRESS: " + str(i) + "/" + str(len(elements.subfolder)))
			print("-"*(level*4+1) + "SUBFOLDER title: " + subfolder.title)
			print("-"*(level*4+1) + "SUBFOLDER resource  len: " + str(len(subfolder.elements.resource)))
			print("-"*(level*4+1) + "SUBFOLDER video     len: " + str(len(subfolder.elements.video)))
			print("-"*(level*4+1) + "SUBFOLDER subfolder len: " + str(len(subfolder.elements.subfolder)))

			if not subfolder.elements.isEmpty():
				printElements(subfolder.elements, level+1)

def exploreSubFolders(driver, elements):
	for i, subfolder in enumerate(elements.subfolder):

		print("subfolder " + str(i+1).ljust(2) + " of " + str(len(elements.subfolder)))
		driver.get(subfolder.link)
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

		for i in range(len(startIndexes)):
			link = src[startIndexes[i]:endIndexes[i]]
			if "/pluginfile.php/" in link:
				title = findTitle(src, endIndexes[i], pattern="\"fp-filename\"")
				subfolder.elements.resource.append(simpleElement(title, link))

def parsePage(driver, URL):

	elements = Elements()
	
	driver.get(URL)
	
	waitForElement(driver, 'page-content')
	
	src = driver.page_source

	sub = "href=\"https:"

	res = [i+6 for i in range(len(src)) if src.startswith(sub, i)] 

	end = []
	endsub = "\""

	for pivot in res:
		for i in range(pivot, len(src)):
			if (src.startswith(endsub, i)):
				end.append(i)
				break

	for i in range(len(res)):
		link = src[res[i]:end[i]]
		if "/kalvidres/" in link:
			title = findTitle(src, end[i])
			elements.video.append(simpleElement(title, link))
		elif "/resource/" in link:
			title = findTitle(src, end[i])
			elements.resource.append(simpleElement(title, link))
		elif "/folder/" in link and link!=URL:
			title = findTitle(src, end[i])
			elements.subfolder.append(subfolderElement(title, link))

	if len(elements.subfolder)>0 :
		exploreSubFolders(driver, elements)

	return elements

def printMoodleElement(elem):
	types = ["PDF", "ARCHIVE", "ZOOM", "VIDEO", "YOUTUBE", "SECTION", "SUBFOLDER"]
	print(types[elem.type] + " - " + elem.title)
	if (elem.link!=""):
		print(elem.link)
	print("-------")

def exploreSubFoldersMoodleSimulator(driver, element):

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
			obj = MoodleElement(PDF, title, link)
			elements.append(obj)
	element.elements = elements

def parsePage_MoodleSimulator(driver, URL, level=0):			## LOOK ALSO FOR sectionname

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
					if "/kalvidres/" in link:
						title = findTitle(src, j)
						obj = MoodleElement(VIDEO, title, link)
						elements.append(obj)
					elif "/resource/" in link:
						title = findTitle(src, j)
						obj = MoodleElement(PDF, title, link)
						elements.append(obj)
					elif "/folder/" in link and link!=URL:
						subfolders_cont += 1
						title = findTitle(src, j)
						obj = MoodleElement(SUBFOLDER, title, link)
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
					obj = MoodleElement(SECTION, title)
					elements.append(obj)
					break

	if level==0:
		for elem in elements:
			printMoodleElement(elem)
			if elem.type==SUBFOLDER:
				print("exploring subfolder")
				exploreSubFoldersMoodleSimulator(driver, elem)
				for sub in elem.elements:
					printMoodleElement(sub)

	return elements