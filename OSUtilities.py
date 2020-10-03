import os

def checkAndMkDir(path, name):
	if not os.path.isdir(path + "/" + name):
		os.mkdir(path + "/" + name)


def getcwd():
	return os.getcwd()


def isFile(path):
	return os.path.isfile(path)