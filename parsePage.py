from selenium import webdriver


import time
import os

from Elements import Elements, simpleElement, subfolderElement
from waitForElement import waitForElement

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
	for subfolder in elements.subfolder:

		print("------- exploring: \n" + subfolder.title + "\nat link:\n" + subfolder.link)
		
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

	'''f=open("chimica.txt", "r")
	src = f.read()
	f.close()'''

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
			#print("just added\n " + link + "\nwhile URL is\n " + URL)
			elements.subfolder.append(subfolderElement(title, link))

	'''print("FOUND: " + str(len(elements.subfolder)) + " elements")
	print("   at URL " + driver.current_url)'''

	'''if URL!="https://elearning.unipd.it/chimica/course/view.php?id=603":
		for sub in elements.subfolder:
			print(sub.title + " " + sub.link)
		driver.quit()
		exit()'''

	if len(elements.subfolder)>0 :
		exploreSubFolders(driver, elements)

	printElements(elements)

	return elements