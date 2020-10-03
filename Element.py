from config import *

class Element:
	def __init__(self, elementType, title, link=""):
		if elementType not in supportedTypes:
			print("Error: MoodleElement type requested is not supported yet.")
			exit()
		
		if link=="" and elementType!=SECTION:
			print("Error: an empty link is allowed only with section elements.")
			exit()

		self.type = elementType
		self.title = title
		self.link = link
		self.widget = None
		self.var = None

		if elementType==SUBFOLDER:
			self.elements = []
			self.expand = False