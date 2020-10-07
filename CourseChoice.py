from tkinter import *
import tkinter as tk
import platform
from config import *
from OSUtilities import isFile

class CourseChoice:
	def __init__(self):

		self.root = tk.Tk()
		self.root.geometry("800x600")
		self.canvas = tk.Canvas(self.root)
		
		self.configureCanvasToBeScrollable()

		self.frame = tk.Frame(self.canvas)

		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

		self.counter = 0
		self.toReturn = None		

		if (isFile("data/courseslist.txt")):
			with open("data/courseslist.txt", "r") as f:
				while True:
					line = f.readline()
					if not line:
						break
					if (line[len(line)-1] == '\n'):
						line = line[:-1]
					line = line.split(" ")
					title = ""
					for i in range(len(line)-1):
						title += line[i]
					link = line[len(line)-1]
					self.addElement(title, link)
		else:
			print("ERROR: couldn't find the data/courseslist.txt file!")

		self.updateGraphics()
		

	def callback(self, link):
		self.toReturn = link
		self.root.destroy()

	def addElement(self, title, link):
		var = IntVar()
		fg = "black"
		if "chimica" in link:
			fg = "darkorange"
		elif "dii" in link:
			fg = "brown"
		elif "dei" in link:
			fg = "blue"
		elif "math" in link:
			fg = "red"
		elem = Checkbutton(self.frame, text = title, font = "bold",\
			variable = var, onvalue=1, offvalue=0, height=2, \
			activebackground = "#FFFFFF", padx = 300, fg = fg,\
			compound = "left", command=lambda:self.callback(link))
	
		self.renderWidget(elem)



	def bindLinuxMouseScroll(self, elem):
		elem.bind("<Button-4>", lambda event : self.canvas.yview('scroll', -1, 'units'))
		elem.bind("<Button-5>", lambda event : self.canvas.yview('scroll', 1, 'units'))

	def bindWindowsMouseScroll(self, elem):
		elem.bind_all("<MouseWheel>", on_mousewheel)

	def bindMouse(self, elem):
		if (platform.system()=="Linux"):
			self.bindLinuxMouseScroll(self.canvas)
		elif platform.system()=="Windows":
			self.bindWindowsMouseScroll(self.canvas)

	def configureCanvasToBeScrollable(self):
		self.bindMouse(self.canvas)

		vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=vsb.set)
		vsb.pack(side="right", fill="y")

	def onFrameConfigure(self, canvas):
	    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def renderWidget(self, elem):
		
		elem.grid(row=self.counter, sticky=W)
		
		self.bindMouse(elem)
		self.counter += 1

	def updateGraphics(self):

		self.counter = 0

		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))

		self.bindMouse(self.frame)

	def getCourseURL(self):
		self.root.mainloop()
		return self.toReturn