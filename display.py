
import os, sys
sys.path.insert(0, os.path.join("..", "every", "common"))
from asciipixel import AsciiPixel
from screen import Screen

class Display:
	DEFAULT_BOARD_HEIGHT = 21
	DEFAULT_BOARD_WIDTH = 21
	DEFAULT_EVENT_HEIGHT = 21
	DEFAULT_EVENT_WIDTH = 59 
	def __init__(self, board, events):
		"""
			a screen generator
		"""
		self.boardHeight = Display.DEFAULT_BOARD_HEIGHT
		self.boardWidth = Display.DEFAULT_BOARD_WIDTH
		self.eventHeight = Display.DEFAULT_EVENT_HEIGHT
		self.eventWidth = Display.DEFAULT_EVENT_WIDTH
		self.board = board
		self.events = events

	def getScreen(self, player):
		boardDisplay = self.getBoardDisplay(player) 
		eventDisplay = self.getEventDisplay(player)  
		retPixels = []
		height = max(self.boardHeight, self.eventHeight)
		for i in range(0, height):
			retRow = []
			for j in range(0, self.boardWidth):
				retRow.append(boardDisplay[i][j])			 
			for j in range(0, self.eventWidth):
				retRow.append(eventDisplay[i][j]) 
			retPixels.append(retRow)
			retRow = []
		retScreen = Screen(retPixels)
		return retScreen

	def getBoardDisplay(self, player):
		if player == None:
			# can happen if they recently disconnected
			return
		centerX = player.x
		centerY = player.y
		startX = player.x - (self.boardWidth - 1) / 2 
		startY = player.y - (self.boardHeight - 1) / 2
		boardDisplay = []
		for i in range(startY, startY + self.boardHeight):
			curRow = []
			for j in range(startX, startX + self.boardWidth):
				curPix = None
				if self.isWithinBounds(j, i):
					curPix = self.board[i][j].render()	
				else:
					curPix = AsciiPixel()  
				curRow.append(curPix)
			boardDisplay.append(curRow)
			curRow = []
		return boardDisplay

	def isWithinBounds(self, x, y):
		if x >= 0 and x < len(self.board[0]) and (
				y >= 0 and y < len(self.board)):
			return True
		else:
			return False

	def getEventDisplay(self, player): 
		"""
			we'll print out the most recent events!
		"""
		eventDisplay = []
		for i in range(-1, -1 * (self.eventHeight + 1), -1):
			eventRow = []
			if len(self.events) >= (-1 * i):
				curEventStr = str(self.events[i]) 
				for j in range(0, self.eventWidth):
					curPix = None
					if j < len(curEventStr):
						curChar = curEventStr[j]
						curPix = AsciiPixel(ord(curChar))
					else:
						curPix = AsciiPixel(ord(' '))
					eventRow.append(curPix)
			else:
				for j in range(0, self.eventWidth):
					curPix = AsciiPixel(ord(' '))
					eventRow.append(curPix)
			eventDisplay.append(eventRow)
		return eventDisplay
