from config import *

class simpleElement:
	def __init__(self, title, link):
		self.title = title
		self.link = link

class subfolderElement:
	def __init__(self, title, link):
		self.title = title
		self.link = link
		self.elements = Elements()

class Elements:
	def __init__(self):
		self.video = []			# a collection of simpleElement s
		self.resource = []		# a collection of simpleElement s
		self.subfolder = []		# a collection of subfolderElement s

	def isEmpty(self):
		if len(self.video)==0 and len(self.resource)==0 and len(self.subfolder)==0:
			return True
		return False


class MoodleElements:
	def __init__(self, elementType, title, link, elements=None):
		if self.type not in supportedTypes:
			print("Error: MoodleElement type requested is not supported yet.")
			exit()
		self.type = elementType
		self.title = title
		self.link = link
		if elements!=None:
			self.elements = elements
