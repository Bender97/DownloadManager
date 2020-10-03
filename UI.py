from tkinter import *
import tkinter as tk

from Element import Element
from config import *

class UI:
	def __init__(self, elements, mode=MOODLESIMULATOR):

		self.elements = elements

		self.moodleElements = []
		self.categorySortedElements = []

		self.mode = mode

		self.counter = 0

		self.toReturn = []

		self.root = tk.Tk()
		self.root.geometry("800x600")
		self.canvas = tk.Canvas(self.root)
		
		self.configureCanvasToBeScrollable()
		self.addMenuToRoot()

		self.frame = tk.Frame(self.canvas)

		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

		self.loadImages()
		self.initiateCheckVariables()

		self.root.update()

	def loadImages(self):
		self.recorded_zoom_icon = tk.PhotoImage(file="img/recorded_zoom_icon.png")
		self.pdf_icon = tk.PhotoImage(file="img/pdf_icon.png")
		self.youtube_icon = tk.PhotoImage(file="img/youtube_icon.png")
		self.subfolder_icon = tk.PhotoImage(file="img/subfolder_icon.png")
		self.archive_icon = tk.PhotoImage(file="img/archive_icon.png")

	def initiateCheckVariables(self):
		for elem in self.elements:
			if elem.type!=SECTION:
				elem.var = IntVar()
				elem.var.set(0)
				if elem.type==SUBFOLDER:
					for sub in elem.elements:
						sub.var=IntVar()
						elem.var.set(0)

	def bindLinuxMouseScroll(self, elem):
		elem.bind("<Button-4>", lambda event : self.canvas.yview('scroll', -1, 'units'))
		elem.bind("<Button-5>", lambda event : self.canvas.yview('scroll', 1, 'units'))

	def bindWindowsMouseScroll(self, elem):
		elem.bind_all("<MouseWheel>", on_mousewheel)

	def changeViewModeCallback(self):
		
		self.cleanFrame()

		if (self.mode==MOODLESIMULATOR):
			self.mode=CATEGORYSORTED
			self.buildGraphicsWidgets_CategorySorted()
		elif (self.mode==CATEGORYSORTED):
			self.mode=MOODLESIMULATOR
			self.buildGraphicsWidgets_MoodleSimulator()
		
		self.updateGraphics()
		self.addMenuToRoot()

	def cleanFrame(self):
		iterable = None
		if (self.mode==MOODLESIMULATOR):
			iterable = self.moodleElements
		elif (self.mode==CATEGORYSORTED):
			iterable = self.categorySortedElements

		for elem in iterable:
			elem.widget.grid_forget()
			if (elem.type==SUBFOLDER):
				for sub in elem.elements:
					sub.widget.grid_forget()

	def addMenuToRoot(self):
		menubar = Menu(self.root)

		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Download", 		 command = lambda: self.downloadCallback())
		filemenu.add_command(label="Select nothing", command = lambda: self.noneBtnCallback())
		filemenu.add_command(label="Select all",	 command = lambda: self.allBtnCallback())
		menubar.add_cascade(label="File", menu=filemenu)

		viewmenu = Menu(menubar, tearoff=0)
		if (self.mode==MOODLESIMULATOR):
			viewmenu.add_command(label="Change to CategorySorted View", command = lambda: self.changeViewModeCallback())
		else:
			viewmenu.add_command(label="Change to MoodleSimulator View", command = lambda: self.changeViewModeCallback())
		menubar.add_cascade(label="View", menu=viewmenu)

		self.root.config(menu=menubar)

	def configureCanvasToBeScrollable(self):
		#FOR WINDOWS (must write function)
		#ui.bindLinuxMouseScroll(canvas)

		#FOR LINUX
		self.bindLinuxMouseScroll(self.canvas)

		vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=vsb.set)
		vsb.pack(side="right", fill="y")

	def subfolderCallback(self, elem=""):
		
		self.cleanFrame()

		elem.expand = not elem.expand
		for sub in elem.elements:
			sub.widget.select()
		self.updateGraphics()

	def downloadCallback(self):
		
		iterable = None
		if self.mode == MOODLESIMULATOR:
			iterable = self.moodleElements
		elif self.mode == CATEGORYSORTED:
			iterable = self.categorySortedElements

		for elem in iterable:
			if(elem.type!=SECTION and elem.var.get()):
				self.toReturn.append(elem)
				
		self.root.destroy()

	def noneBtnCallback(self):
		iterable = None
		if self.mode == MOODLESIMULATOR:
			iterable = self.moodleElements
		elif self.mode == CATEGORYSORTED:
			iterable = self.categorySortedElements

		for elem in iterable:
			if elem.type!=SECTION:
				elem.var.set(0)
				elem.widget.deselect()
				if elem.type == SUBFOLDER:
					elem.expand = False
					for sub in elem.elements:
						sub.var.set(0)
						sub.widget.deselect()
		self.updateGraphics()

	def allBtnCallback(self):
		iterable = None
		if self.mode == MOODLESIMULATOR:
			iterable = self.moodleElements
		elif self.mode == CATEGORYSORTED:
			iterable = self.categorySortedElements

		for elem in iterable:
			if elem.type!=SECTION:
				elem.var.set(1)
				elem.widget.select()
				if elem.type == SUBFOLDER:
					elem.expand = True
					for sub in elem.elements:
						elem.var.set(1)
						sub.widget.select()
		self.updateGraphics()

	def buildCheckbutton(self, elem, image, frame):
		elem.widget = Checkbutton(frame, text = elem.title,\
			variable = elem.var, onvalue=1, offvalue=0, height=35, \
			activebackground = "#D3D3D3", image = image, \
			compound = "left")

	def configureUIElement(self, elem):
		if (elem.type == SECTION):
			elem.widget = tk.Message(self.frame, width=self.root.winfo_height(), text=elem.title, font='Helvetica 18 bold')
		elif (elem.type == VIDEO):
			self.buildCheckbutton(elem, self.recorded_zoom_icon, self.frame)
		elif (elem.type == PDF):
			self.buildCheckbutton(elem, self.pdf_icon, self.frame)
		elif (elem.type == YOUTUBE):
			self.buildCheckbutton(elem, self.youtube_icon, self.frame)
		elif (elem.type == SUBFOLDER):
			self.buildCheckbutton(elem, self.subfolder_icon, self.frame)
			elem.widget.configure(command = lambda: self.subfolderCallback(elem))
		elif (elem.type == ARCHIVE):
			self.buildCheckbutton(elem, self.archive_icon, self.frame)
		'''elif (elem.type == ZOOM):
			pass'''

	def onFrameConfigure(self, canvas):
	    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def buildGraphicsWidgets_MoodleSimulator(self):
		if len(self.moodleElements) == 0:
			for elem in self.elements:
				self.configureUIElement(elem)
				self.moodleElements.append(elem)
				if (elem.type==SUBFOLDER):
					for sub in elem.elements:
						self.configureUIElement(sub)

	def buildGraphicsWidgets_CategorySorted(self):
		if len(self.categorySortedElements) == 0:
			
			pdf = Element(SECTION, "PDF Resources")
			self.configureUIElement(pdf)
			vid = Element(SECTION, "VIDEO Resources")
			self.configureUIElement(vid)
			arc = Element(SECTION, "ARCHIVE Resources")
			self.configureUIElement(arc)
			sub = Element(SECTION, "SUBFOLDER Resources")
			self.configureUIElement(sub)

			for elemType, section in [[PDF, pdf], [VIDEO, vid], [ARCHIVE, arc], [SUBFOLDER, sub]]:
				self.categorySortedElements.append(section)
				for elem in self.elements:
					if elem.type==elemType:
						self.configureUIElement(elem)
						self.categorySortedElements.append(elem)
						if (elem.type==SUBFOLDER):
							for sub in elem.elements:
								self.configureUIElement(sub)

	def renderWidget(self, elem, padx = 1):
		if elem.type==SECTION:
			elem.widget.grid(row=self.counter, sticky=W)
		else:
			elem.widget.grid(row=self.counter, sticky=W, padx=padx)

		self.bindLinuxMouseScroll(elem.widget)
		self.counter += 1

	def updateGraphics(self):

		self.counter = 0
		iterable = None
		if self.mode == MOODLESIMULATOR:
			iterable = self.moodleElements
		elif self.mode == CATEGORYSORTED:
			iterable = self.categorySortedElements

		for elem in iterable:
			self.renderWidget(elem)
			if (elem.type==SUBFOLDER):
				if elem.expand==True:
					for sub in elem.elements:
						self.renderWidget(sub, padx=40)
				else:
					for sub in elem.elements:
						sub.widget.grid_forget()


		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))

		self.bindLinuxMouseScroll(self.frame)

	def performSelection(self):
		if (self.mode==MOODLESIMULATOR):
			self.buildGraphicsWidgets_MoodleSimulator()
		elif (self.mode==CATEGORYSORTED):
			self.buildGraphicsWidgets_CategorySorted()
		else:
			print("ERROR: performSelection UI mode not supported. Abort.")
			exit()
		self.updateGraphics()
		self.root.mainloop()
		return self.toReturn