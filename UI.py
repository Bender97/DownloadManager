from tkinter import *
import tkinter as tk

from Elements import Elements

class UI:
	def __init__(self, elements):

		self.elements = elements

		self.counter = 0
		self.objects = []

		self.res_checkVar = []
		self.res_checkbuttons = []

		self.vid_checkVar = []
		self.vid_checkbuttons = []

		self.sub_checkVar = []
		self.sub_checkbuttons = []

		self.toReturn = Elements()

		self.root = tk.Tk()
		self.root.geometry("200x600")
		
		self.canvas = tk.Canvas(self.root)
		
		self.configureCanvasToBeScrollable()
		self.addMenuToRoot()

		self.frame = tk.Frame(self.canvas)
		
		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4, 4), window=self.frame, anchor="nw")


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

	def configureUIElement(self, elem):
		elem.grid(row=self.counter, sticky=W)
		self.bindLinuxMouseScroll(elem)
		self.counter += 1

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


	def performSelection(self):			
		
		###### PDF RESOURCES
		self.configureUIElement(tk.Label(self.frame, text="PDF Resources", font='Helvetica 18 bold'))
		
		for i, res in enumerate(self.elements.resource):
			self.res_checkVar.append(IntVar())
			self.res_checkbuttons.append(Checkbutton(self.frame, text = res.title,\
				variable = self.res_checkVar[i], onvalue=1, offvalue=0, height=2))
			self.configureUIElement(self.res_checkbuttons[i])

		###### VIDEO RESOURCES
		self.configureUIElement(tk.Label(self.frame, text="Video Resources", font='Helvetica 18 bold'))

		for i, vid in enumerate(self.elements.video):
			self.vid_checkVar.append(IntVar())
			self.vid_checkbuttons.append(Checkbutton(self.frame, text = vid.title,\
				variable = self.vid_checkVar[i], onvalue=1, offvalue=0, height=2))
			self.configureUIElement(self.vid_checkbuttons[i])

		###### SUBFOLDERS RESOURCES
		self.configureUIElement(tk.Label(self.frame, text="Subfolders", font='Helvetica 18 bold'))

		for i, subfolder in enumerate(self.elements.subfolder):
			self.sub_checkVar.append(IntVar())
			self.sub_checkbuttons.append(Checkbutton(self.frame, text = subfolder.title,\
				variable = self.sub_checkVar[i], onvalue=1, offvalue=0, height=2))
			self.configureUIElement(self.sub_checkbuttons[i])

		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))

		self.bindLinuxMouseScroll(self.frame)

		self.root.mainloop()

		return self.toReturn