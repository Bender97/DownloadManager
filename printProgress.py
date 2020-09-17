import math

def printProgress(current, tot, msg = ""):
	if (current>tot):
		print("printProgressError: current>tot")
		exit()
	progressBarLen = 20
	increase = progressBarLen/tot

	progress = math.ceil(increase*(current))
	print("progress: " + "="*(progress-1) + ">  " + " "*(progressBarLen-progress) + "{:.2f}".format((100/tot)*(current)) + "% completed")