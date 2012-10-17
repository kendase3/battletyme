
class Display:
	DEFAULT_MAPP_HEIGHT = 21
	DEFAULT_MAPP_WIDTH = 21
	DEFAULT_EVENT_HEIGHT = 21
	DEFAULT_EVENT_WIDTH = 59 
	def __init__(self, mapp, events):
		"""
			a screen generator
		"""
		self.mappHeight = DEFAULT_MAPP_HEIGHT
		self.mappWidth = DEFAULT_MAPP_WIDTH
		self.eventHeight = DEFAULT_EVENT_HEIGHT
		self.eventWidth = DEFAULT_EVENT_WIDTH
		self.mapp = mapp
		self.events = events

	def getScreen(self, player):
		mappDisplay = self.getMapDisplay(player) 
		eventDisplay = self.getEventDisplay(player)  

	def getMapDisplay(self, player):
		centerX = player.x
		centerY = player.y
		startX = player.x - (self.mappWidth - 1) / 2 
		startY = player.y - (self.mappHeight - 1) / 2
		mappDisplay = []
		for i in range(startY, startY + self.mappHeight):
			curRow = []
			for j in range(startX, startX + self.mappWidth):
				curPix = None
				if self.mapp.isWithinBounds(j, i):
					curPix = mapp[i][j].render()	
				else:
					curPix = AsciiPixel()  
				curRow.append(curPix)
			mappDisplay.append(curRow)
			curRow = []
		return mappDisplay

	def getEventDisplay(self, player): 
		#TODO
		return None
