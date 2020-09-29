from tkinter import *
import tkinter as tk


res_checkbuttons = []
res_checkVar = []

vid_checkbuttons = []
vid_checkVar = []

class UI:
	def __init__(self):
		self.counter = 0
		self.objects = []

	def bindLinuxMouseScroll(self, elem):
		elem.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
		elem.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	def bindWindowsMouseScroll(self, elem):
		bind_all("<MouseWheel>", on_mousewheel)

	def configureUIElement(self, elem):
		elem.grid(row=self.counter, sticky=W)
		self.bindLinuxMouseScroll(elem)
		self.counter += 1

def downloadCallback(elements):
	for i in range(len(elements.resource)):
		if(res_checkVar[i].get()):
			print(elements.resource.title)
	for i in range(len(elements.video)):
		if(vid_checkVar[i].get()):
			print(elements.video.title)

def noneBtnCallback(elements):
	for btn in res_checkbuttons:
		btn.deselect()
	for btn in vid_checkbuttons:
		btn.deselect()

def allBtnCallback(elements):
	for btn in res_checkbuttons:
		btn.select()
	for btn in vid_checkbuttons:
		btn.select()

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


def performSelection(elements):
	global canvas
	maxlen = 0
	for res in elements.resource:
		if len(res.title)>maxlen:
			maxlen=len(res.title)
	for vid in elements.video:
		if len(vid.title)>maxlen:
			maxlen=len(vid.title)

	root = tk.Tk()
	root.geometry(str(maxlen*10)+ "x600")
	canvas = tk.Canvas(root)
	
	ui = UI()

	#FOR WINDOWS (must write function)
	#ui.bindLinuxMouseScroll(canvas)

	#FOR LINUX
	ui.bindLinuxMouseScroll(canvas)
	
	frame = tk.Frame(canvas)
	vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
	canvas.configure(yscrollcommand=vsb.set)

	vsb.pack(side="right", fill="y")
	
	canvas.pack(side="left", fill="both", expand=True)
	canvas.create_window((4, 4), window=frame, anchor="nw")
	
	ui.configureUIElement(tk.Label(frame, text="PDF Resources", font='Helvetica 18 bold'))
	

	for i in range(len(elements.resource)):
		res_checkVar.append(IntVar())
		res_checkbuttons.append(Checkbutton(frame, text = elements.resource[i].title,\
			variable = res_checkVar[i], onvalue=1, offvalue=0, height=2))
		ui.configureUIElement(res_checkbuttons[i])

	ui.configureUIElement(tk.Label(frame, text="Video Resources", font='Helvetica 18 bold'))
	

	for i in range(len(elements.video)):
		vid_checkVar.append(IntVar())
		vid_checkbuttons.append(Checkbutton(frame, text = elements.video[i].title,\
			variable = vid_checkVar[i], onvalue=1, offvalue=0, height=2))
		ui.configureUIElement(vid_checkbuttons[i])

	ui.configureUIElement(Button(frame, text="Download", command=lambda: downloadCallback(elements)))

	ui.configureUIElement(Button(frame, text="Select Nothing", command=lambda: noneBtnCallback(elements)))

	ui.configureUIElement(Button(frame, text="Select All", command=lambda: allBtnCallback(elements)))

	frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

	ui.bindLinuxMouseScroll(frame)

	root.mainloop()