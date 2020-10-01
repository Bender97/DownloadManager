from tkinter import *
import tkinter as tk

from Elements import Elements
from config import *

class CustomCheckbutton:
	def __init__(self, elem, image, frame):
		self.var = IntVar()
		self.widget = Checkbutton(frame, text = elem.title,\
			variable = self.var, onvalue=1, offvalue=0, height=35, \
			activebackground = "#D3D3D3", image = image, \
			compound = "left")		

class UI:
	def __init__(self, elements):

		self.elements = elements

		self.counter = 0

		self.toReturn = Elements()

		self.root = tk.Tk()
		self.root.geometry("800x600")
		self.canvas = tk.Canvas(self.root)
		
		self.configureCanvasToBeScrollable()
		self.addMenuToRoot()

		self.frame = tk.Frame(self.canvas)

		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

		self.loadImages()

		self.root.update()

	def loadImages(self):
		self.recorded_zoom_icon = tk.PhotoImage(file="img/recorded_zoom_icon.png")
		self.pdf_icon = tk.PhotoImage(file="img/pdf_icon.png")
		self.youtube_icon = tk.PhotoImage(file="img/youtube_icon.png")
		self.subfolder_icon = tk.PhotoImage(file="img/subfolder_icon.png")
		#self.archive_icon = tk.PhotoImage(file="../img/archive_icon.png")

	def bindLinuxMouseScroll(self, elem):
		elem.bind("<Button-4>", lambda event : self.canvas.yview('scroll', -1, 'units'))
		elem.bind("<Button-5>", lambda event : self.canvas.yview('scroll', 1, 'units'))

	def bindWindowsMouseScroll(self, elem):
		elem.bind_all("<MouseWheel>", on_mousewheel)

	def addMenuToRoot(self):
		menubar = Menu(self.root)

		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Download", 		 command = lambda: self.downloadCallback())
		filemenu.add_command(label="Select nothing", command = lambda: self.noneBtnCallback())
		filemenu.add_command(label="Select all",	 command = lambda: self.allBtnCallback())
		menubar.add_cascade(label="File", menu=filemenu)

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
		if (elem==""):
			return
		if (elem.widget.var.get()==1):
			elem.widget.widget.select()
		else:
			elem.widget.widget.deselect()
		elem.expand = not elem.expand
		for sub in elem.elements:
			sub.widget.widget.select()
		self.updateGraphics()

	def configureUIElement(self, elem):
		if (elem.type == SECTION):
			elem.widget = tk.Message(self.frame, width=self.root.winfo_height(), text=elem.title, font='Helvetica 18 bold')
		elif (elem.type == VIDEO):
			elem.widget = CustomCheckbutton(elem, self.recorded_zoom_icon, self.frame)
		elif (elem.type == PDF):
			elem.widget = CustomCheckbutton(elem, self.pdf_icon, self.frame)
		elif (elem.type == YOUTUBE):
			elem.widget = CustomCheckbutton(elem, self.youtube_icon, self.frame)
		elif (elem.type == SUBFOLDER):
			elem.widget = CustomCheckbutton(elem, self.subfolder_icon, self.frame)
			elem.widget.widget.configure(command = lambda: self.subfolderCallback(elem))
		'''elif (elem.type == ARCHIVE):
			pass
		elif (elem.type == ZOOM):
			pass'''

	def downloadCallback(self):
		for i, res in enumerate(self.elements.resource):
			if(self.res_checkVar[i].get()):
				self.toReturn.resource.append(res)
		for i, vid in enumerate(self.elements.video):
			if(self.vid_checkVar[i].get()):
				self.toReturn.video.append(vid)
		for i, sub in enumerate(self.elements.subfolder):
			if(self.sub_checkVar[i].get()):
				self.toReturn.subfolder.append(sub)
		
		self.root.destroy()

	def noneBtnCallback(self):
		for chkbtn in self.res_checkbuttons:
			chkbtn.deselect()
		for chkbtn in self.vid_checkbuttons:
			chkbtn.deselect()
		for chkbtn in self.sub_checkbuttons:
			chkbtn.deselect()

	def allBtnCallback(self):
		for chkbtn in self.res_checkbuttons:
			chkbtn.select()
		for chkbtn in self.vid_checkbuttons:
			chkbtn.select()
		for chkbtn in self.sub_checkbuttons:
			chkbtn.select()

	def onFrameConfigure(self, canvas):
	    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def buildGraphicsWidgets(self):
		for elem in self.elements:
			self.configureUIElement(elem)
			if (elem.type==SUBFOLDER):
				for sub in elem.elements:
					self.configureUIElement(sub)

	def renderWidget(self, elem, padx = 1):
		if elem.type==SECTION:
			elem.widget.grid(row=self.counter, sticky=W)
			self.bindLinuxMouseScroll(elem.widget)
		else:
			elem.widget.widget.grid(row=self.counter, sticky=W, padx=padx)
			self.bindLinuxMouseScroll(elem.widget.widget)

		self.counter += 1

	def updateGraphics(self):

		self.counter = 0

		for elem in self.elements:
			self.renderWidget(elem)
			if (elem.type==SUBFOLDER and elem.expand==True):
				for sub in elem.elements:
					self.renderWidget(sub, padx=40)

		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))

		self.bindLinuxMouseScroll(self.frame)

	def UI_MoodleSimulator(self):
		self.buildGraphicsWidgets()
		self.updateGraphics()
		self.root.mainloop()
		return self.toReturn