import math

class progressBar:
	def __init__(self, max, progressBarLen=20):
		self.max = max
		self.counter = 1
		self.progressBarLen = progressBarLen

	def printProgress(self, msg = ""):
		if (self.counter>self.max):
			print("printProgressError: current>tot")
			return
		if (self.max==0):
			print(msg + (" " if msg!="" else "") + "progress: " + "="*(self.progressBarLen-1) + ">  " + " " + "100% completed")
			return
		increase = self.progressBarLen/self.max

		progress = math.ceil(increase*(self.counter))
		print(msg + (" " if msg!="" else "") + "progress: " + "="*(progress-1) + ">  " + " "*(self.progressBarLen-progress) + "{:.2f}".format((100/self.max)*(self.counter)) + "% completed")
		self.counter += 1