from selenium import webdriver


import time
import os

from Elements import Elements
from waitForElement import waitForElement

def removeSpan(txt):
	pattern='<span'
	for i in range(0, len(txt)):
		if (txt.startswith(pattern, i)):
			return txt[0:i]

def findTitle(src, pivot):
	pattern="instancename"
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

def printElements(elements):
	print("------- RESOURCES -------- " + str(len(elements.resource)))
	for res in elements.resource:
		print(res)

	print()
	print("------- VIDEOS ----------- " + str(len(elements.video)))
	for vid in elements.video:
		print(vid)
	print()

def parsePage(driver, URL):

	elements = Elements()
	
	'''driver.get(URL)
	
	waitForElement(driver, 'page-content')
	
	src = driver.page_source'''

	f=open("chimica.txt", "r")
	src = f.read()
	f.close()

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
			elements.video.append([title, link])
		elif "/resource/" in link:
			title = findTitle(src, end[i])
			elements.resource.append([title, link])


	return elements