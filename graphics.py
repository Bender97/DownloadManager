from tkinter import *
import tkinter as tk


res_checkbuttons = []
res_checkVar = []

vid_checkbuttons = []
vid_checkVar = []


def downloadCallback(elements):
	for i in range(len(elements.resource)):
		if(res_checkVar[i].get()):
			print(elements.resource[i])
	for i in range(len(elements.video)):
		if(vid_checkVar[i].get()):
			print(elements.video[i])

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
		if len(res[0])>maxlen:
			maxlen=len(res[0])
	for vid in elements.video:
		if len(vid[0])>maxlen:
			maxlen=len(vid[0])

	root = tk.Tk()
	root.geometry(str(maxlen*10)+ "x600")
	canvas = tk.Canvas(root)
	#FOR WINDOWS (must write function)
	#canvas.bind_all("<MouseWheel>", on_mousewheel)
	
	#FOR LINUX
	canvas.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
	canvas.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))
	
	frame = tk.Frame(canvas)
	vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
	canvas.configure(yscrollcommand=vsb.set)

	vsb.pack(side="right", fill="y")
	
	canvas.pack(side="left", fill="both", expand=True)
	canvas.create_window((4, 4), window=frame, anchor="nw")

	
	
	pdfLabel = tk.Label(frame, text="PDF Resources", font='Helvetica 18 bold')
	pdfLabel.grid(row=0, sticky=W)
	pdfLabel.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
	pdfLabel.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	for i in range(len(elements.resource)):
		res_checkVar.append(IntVar())
		res_checkbuttons.append(Checkbutton(frame, text = elements.resource[i][0],\
			variable = res_checkVar[i], onvalue=1, offvalue=0, height=2))
		res_checkbuttons[i].grid(row=(i+1), sticky=W)
		res_checkbuttons[i].bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
		res_checkbuttons[i].bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	videoLabel = tk.Label(frame, text="Video Resources", font='Helvetica 18 bold')
	videoLabel.grid(row=(len(elements.resource)+1), sticky=W)
	videoLabel.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
	videoLabel.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	for i in range(len(elements.video)):
		vid_checkVar.append(IntVar())
		vid_checkbuttons.append(Checkbutton(frame, text = elements.video[i][0],\
			variable = vid_checkVar[i], onvalue=1, offvalue=0, height=2))
		vid_checkbuttons[i].grid(row=(i+2+len(elements.resource)), sticky=W)
		vid_checkbuttons[i].bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
		vid_checkbuttons[i].bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	B = Button(frame, text="Download", command=lambda: downloadCallback(elements))
	B.grid(row=(len(elements.video)+len(elements.resource)+2), sticky=W)
	B.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
	B.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	B_none = Button(frame, text="Select Nothing", command=lambda: noneBtnCallback(elements))
	B_none.grid(row=(len(elements.video)+len(elements.resource)+3), sticky=W)
	B_none.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
	B_none.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	B_all = Button(frame, text="Select All", command=lambda: allBtnCallback(elements))
	B_all.grid(row=(len(elements.video)+len(elements.resource)+4), sticky=W)
	B_all.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
	B_all.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))



	frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
	frame.bind("<Button-4>", lambda event : canvas.yview('scroll', -1, 'units'))
	frame.bind("<Button-5>", lambda event : canvas.yview('scroll', 1, 'units'))

	root.mainloop()