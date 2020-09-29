import math

def printProgress(current, tot, msg = ""):
	if (current>tot):
		print("printProgressError: current>tot")
		exit()
	if (tot==0):
		print(msg + (" " if msg!="" else "") + "progress: " + "="*(progressBarLen-1) + ">  " + " " + "100% completed")
		return
	progressBarLen = 20
	increase = progressBarLen/tot

	progress = math.ceil(increase*(current))
	print(msg + (" " if msg!="" else "") + "progress: " + "="*(progress-1) + ">  " + " "*(progressBarLen-progress) + "{:.2f}".format((100/tot)*(current)) + "% completed")