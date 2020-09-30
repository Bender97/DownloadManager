import os

def checkAndMkDir(path, name):
	if not os.path.isdir(path + "/" + name):
		os.mkdir(path + "/" + name)
