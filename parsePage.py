from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import os

from Elements import Elements

def findTitle(src, pivot):
	pattern="instancename"
	start = 0
	for i in range(pivot, len(src)):
		if (src.startswith(pattern, i)):
			start = i+14
			break
	pattern="<span"
	for i in range(start, len(src)):
		if (src.startswith(pattern, i)):
			return src[start:i]

def parsePage(driver, URL):

	elements = Elements()

	f = open("src.txt", "r")
	src = f.read()
	f.close()

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

	for i in range(len(res)):
		link = src[res[i]:end[i]]
		if "/kalvidres/" in link:
			elements.video.append(link)
		elif "/resource/" in link:
			title = findTitle(src, end[i])
			elements.resource.append([title, link])


	return elements