from selenium import webdriver

from ssologin import SSOLogin
from downloadVideo import downloadVideo
from downloadpdf import downloadpdf
from parsePage import parsePage, printElements
from setAndCreateFirefoxProfile import setAndCreateFirefoxProfile

from tkinter import *
import tkinter as tk


checkbuttons = []
checkVar = []

num = 10

def downloadCallback():
	for i in range(num):
		print(checkVar[i].get())

def noneBtnCallback():
	for btn in checkbuttons:
		btn.deselect()

def allBtnCallback():
	for btn in checkbuttons:
		btn.select()

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

root = tk.Tk()
canvas = tk.Canvas(root)
frame = tk.Frame(canvas)
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4, 4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

for i in range(num):
	checkVar.append(IntVar())
	checkbuttons.append(Checkbutton(frame, text = "prova"+str(i),\
		variable = checkVar[i], onvalue=1, offvalue=0, height=2, width = 20))


B = Button(frame, text="Download", command=downloadCallback)
B.pack(side = tk.BOTTOM)

B_none = Button(frame, text="Select Nothing", command=noneBtnCallback)
B_none.pack(side = tk.BOTTOM)

B_all = Button(frame, text="Select All", command=allBtnCallback)
B_all.pack(side = tk.BOTTOM)


for i in range(num):
	checkbuttons[i].pack()

root.mainloop()




exit()

path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"
fp = setAndCreateFirefoxProfile()

driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)

#courseURL = "https://elearning.dei.unipd.it/course/view.php?id=4476"
courseURL = "https://elearning.unipd.it/chimica/course/view.php?id=603"

SSOLogin(driver, courseURL)
	
elements = parsePage(driver, courseURL)

printElements(elements)

#downloadVideo(driver, elements.video)
#downloadpdf(driver, elements.resource)

driver.quit()