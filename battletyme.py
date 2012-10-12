"""
	a small, turn-based game in which players try to kill
			other players!
"""

import time, random, os, sys 

sys.path.insert(0, os.path.join("..", "every", "common"))

# locals 
from game import Game
from screen import Screen
from asciipixel import AsciiPixel
from stevent import Stevent

class Cell:
	WALL = 'W'
	FLOOR = '.'
	def __init__(self, contents = 'W'):
		self.player = None
		self.objects = []
		self.contents = contents

class Move:
	UP = 'up'
	DOWN = 'down'
	LEFT = 'left'
	RIGHT = 'right'	

class Player:
	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y 
		self.nextMove = None

class Arena(Game):
	WIDTH = 10
	HEIGHT = 10
	SECONDS_PER_TURN = 2
	def __init__(self):
		self.players = []
		self.board = [[Cell() for j in range(Arena.WIDTH)]
				for i in range(Arena.HEIGHT)]
		for i in range(2, 8):
			for j in range(2, 8):
				self.board[i][j].contents = Cell.FLOOR
		self.startTime = time.time() 
		self.lastIterated = self.startTime

	def iterate(self):
		curTime = time.time()
		if curTime - self.lastIterated > Arena.SECONDS_PER_TURN:
			print "tick!"
			self.lastIterated = curTime
			# then we process each player's move (in player order for now)
			for player in self.players:
				xOffset = 0
				yOffset = 0
				if player.nextMove == Move.LEFT:
					xOffset = -1
					yOffset = 0
				elif player.nextMove == Move.RIGHT:
					xOffset = 1
					yOffset = 0
				elif player.nextMove == Move.UP:
					xOffset = 0
					yOffset = -1	
				elif player.nextMove == Move.DOWN: 
					xOffset = 0
					yOffset = 1
				newX = player.x + xOffset
				newY = player.y + yOffset
				if newX >= 0 and newX < len(self.board[0]) and (
						newY >= 0 and newY < len(self.board) and
						self.board[newY][newX].contents == Cell.FLOOR and
						self.board[newY][newX] == None):
					player.x = newX
					player.y = newY

	def addPlayer(self, playerId):
		targetX = random.randint(0, 9)
		targetY = random.randint(0, 9) 
		targetCell = self.board[targetY][targetX] 
		while targetCell.player != None or targetCell.contents != Cell.FLOOR:
			targetX = random.randint(0, 9)
			targetY = random.randint(0, 9)
			targetCell = self.board[targetY][targetX] 
		newPlayer = Player(playerId, targetX, targetY) 
		targetCell.player = newPlayer

	def removePlayer(self, playerId):
		targetPlayer = None
		found = False
		targetPlayer = None
		for player in self.players:
			if player.id == playerId:
				found = True
				targetPlayer = player 
				break
		self.players.remove(targetPlayer)
		targetCell = self.board[targetPlayer.y][targetPlayer.x]
		targetCell.player = None
		return

	def getPlayer(self, playerId):
		for player in self.players:
			if player.id == playerId:
				return player
		return None

	def handleInput(self, stevent, playerId):
		curPlayer = self.getPlayer(playerId)
		if curPlayer == None:
			return
		if stevent.type == Stevent.QUIT:
			self.removePlayer(playerId)
			return
		if stevent.type != Stevent.KEYDOWN:
			return
		if stevent.key == ord('a') or stevent.key == ord('h'):
			curPlayer.nextMove = Move.LEFT	
		elif sevent.key == ord('d') or stevent.key == ord('l'):
			curPlayer.nextMove = Move.RIGHT	
		elif stevent.key == ord('s') or stevent.key == ord('j'):
			curPlayer.nextMove = Move.DOWN
		elif stevent.key == ord('w') or stevent.key == ord('k'):
			curPlayer.nextMove = Move.UP 
		print "player %d's next move is currently %s" % (curPlayer.id, curPlayer.nextMove) 

	def getScreen(self, playerId): 
		rowList = []
		curRow = []
		for row in self.board:
			for cell in row:
				if cell.player == None:
					curRow.append(AsciiPixel(ord(cell.contents), AsciiPixel.WHITE)) 
				else:
					curRow.append(AsciiPixel(ord('@'), AsciiPixel.BLUE)) 
			rowList.append(curRow)
			curRow = []
		screen = Screen(rowList)
		return screen

