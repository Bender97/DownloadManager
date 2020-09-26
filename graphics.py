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
	maxlen = 0
	for res in elements.resource:
		if len(res[0])>maxlen:
			maxlen=len(res[0])
	for vid in elements.video:
		if len(vid[0])>maxlen:
			maxlen=len(vid[0])

	root = tk.Tk()
	canvas = tk.Canvas(root)
	frame = tk.Frame(canvas)
	vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
	canvas.configure(yscrollcommand=vsb.set)
	vsb.pack(side="right", fill="y")
	canvas.pack(side="left", fill="both", expand=True)
	canvas.create_window((4, 4), window=frame, anchor="w")

	
	tk.Label(frame, text="PDF Resources").pack()

	for i in range(len(elements.resource)):
		res_checkVar.append(IntVar())
		res_checkbuttons.append(Checkbutton(frame, text = elements.resource[i][0],\
			variable = res_checkVar[i], onvalue=1, offvalue=0, height=2, width = maxlen))

	tk.Label(frame, text="Video Resources").pack()

	for i in range(len(elements.video)):
		vid_checkVar.append(IntVar())
		vid_checkbuttons.append(Checkbutton(frame, text = elements.video[i][0],\
			variable = vid_checkVar[i], onvalue=1, offvalue=0, height=2, width = maxlen))


	B = Button(frame, text="Download", command=lambda: downloadCallback(elements))
	B.pack(side = tk.BOTTOM)

	B_none = Button(frame, text="Select Nothing", command=lambda: noneBtnCallback(elements))
	B_none.pack(side = tk.BOTTOM)

	B_all = Button(frame, text="Select All", command=lambda: allBtnCallback(elements))
	B_all.pack(side = tk.BOTTOM)


	for i in range(len(elements.resource)):
		res_checkbuttons[i].pack(anchor = "e")
	for i in range(len(elements.video)):
		vid_checkbuttons[i].pack(anchor = "e")


	frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

	root.mainloop()