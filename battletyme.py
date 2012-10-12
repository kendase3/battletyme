"""
	a small, turn-based game in which players try to kill
			other players!
"""

import time, random, os, sys 

sys.path.insert(0, os.path.join("..", "every", "common"))

# locals 
from game import Game
from screen import Screen
from cell import Cell
from asciipixel import AsciiPixel
from player import Player
from stevent import Stevent

class Cell:
	WALL = 'W'
	FLOOR = '.'
	def __init__(self, type = Cell.WALL):
		self.player = None
		self.objects = []
		self.type = type

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

class Arena(Game):
	WIDTH = 10
	HEIGHT = 10
	def __init__(self):
		self.players = []
		self.board = [[Cell() for j in range(Arena.WIDTH)]
				for i in range(Arena.HEIGHT)]
		for i in range(2, 8):
			for j in range(2, 8):
				self.board[i][j].type = Cell.FLOOR

	def iterate(self):
		#TODO: determine if so many seconds have passed, then actually iterate a turn
		return

	def addPlayer(self, playerId):
		targetX = random.randint(0, 9)
		targetY = random.randint(0, 9) 
		targetCell = self.board[targetY][targetX] 
		while targetCell.player != None or targetCell.type != Cell.FLOOR:
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

	def getPlayer(playerId):
		for player in self.players:
			if player.id == playerId:
				return player
		return None

	def handleInput(self, stevent, playerId):
		if stevent.type == Stevent.QUIT:
			self.removePlayer(playerId)
			return
		if stevent.type != Stevent.KEYDOWN:
			return
		curPlayer = self.getPlayer(playerId)
		if curPlayer == None:
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
					curRow.append(AsciiPixel(ord(Cell.type), AsciiPixel.WHITE)) 
				else:
					curRow.append(AsciiPixel(ord('@'), AsciiPixel.BLUE)) 
				rowList.append(curRow)
				curRow = []
		screen = Screen(rowList)
		return screen

