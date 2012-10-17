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
	def __init__(self, feature = None):
		if feature == None:
			feature = Cell.WALL
		self.player = None
		self.objects = []
		self.feature = feature 

	def render(self):
		"""
			return an ascii-pixel representation of yourself
		"""
		ret = None
		if self.player != None:
			ret = AsciiPixel('@') 	
		elif len(self.objects) > 0:
			#TODO: implement called data members 
			ret = AsciiPixel(self.objects[-1].ascii, self.objects[-1].asciiColor) 
		else:
			# if there's no player there, and there aren't any objects on the ground
			# then print the kind of cell
			ret = AsciiPixel(self.feature)
		return ret


class Move:
	UP = 'up'
	DOWN = 'down'
	LEFT = 'left'
	RIGHT = 'right'	

class Creature: 
	PLAYER_TYPE = 0
	GRIDBUG_TYPE = 1
	PLAYER_HP = 8 
	GRIDBUG_HP = 5
	PLAYER_DODGE = 4 # must roll 4 or higher to hit
	GRIDBUG_DODGE = 3
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.dead = False
		self.reset()

	def reset(self):
		"""
			set creature to initial state
		"""
		if self.type == Creature.PLAYER:
			self.hp = Creature.PLAYER_HP 
		elif self.type == Creature.GRIDBUG:
			self.hp = Creature.GRIDBUG_HP
		else:
			print "unknown player type!"
			return 1

class Player(Creature):
	def __init__(self, id, x, y):
		Creature.__init__(self)
		self.id = id
		self.x = x
		self.y = y 
		self.nextMove = None
		self.dodge = Creature.PLAYER_DODGE 

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
				self.board[i][j].feature = Cell.FLOOR
		self.startTime = time.time() 
		self.lastIterated = self.startTime
		self.creatures = []
		self.curPlayerIndex = 0

	def iterate(self):
		curTime = time.time()
		if curTime - self.lastIterated > Arena.SECONDS_PER_TURN:
			print "tick!"
			print "current # of players: %d" % len(self.players)
			self.lastIterated = curTime
			# then we process the next player's move 
			if len(players) == 0:
				return
			player = self.players[self.curPlayerIndex] 			
			if player.nextMove == None:
				continue
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
					self.board[newY][newX].feature == Cell.FLOOR:
				if self.board[newY][newX].player == None:
					# if no one's there, we move there
					print "player move %s accepted!" % player.nextMove 
					self.board[player.y][player.x].player = None
					self.board[newY][newX].player = player 
					player.x = newX
					player.y = newY
				else: 
					# we attack that player standing there!
					attacker = player
					attackee = self.board[newY][newX].player
					self.handleAttack(attacker, attackee) 	
			else:
				print "player move of %s not accepted!" % player.nextMove
			player.nextMove = None
			self.curPlayerIndex += 1
			self.curPlayerIndex = self.curPlayerIndex % len(self.players)

	def handleAttack(attacker, attackee): 
		hitRoll = random.randint(0, 9)
		damageRoll = random.randint(0, 9)
		if hitRoll >= attackee.dodge: 
			attackee.hp -= hitRoll
			if atackee.hp < 0:
				atackee.dead = True

	def addPlayer(self, playerId):
		targetX = random.randint(0, 9)
		targetY = random.randint(0, 9) 
		targetCell = self.board[targetY][targetX] 
		while targetCell.player != None or targetCell.feature != Cell.FLOOR:
			targetX = random.randint(0, 9)
			targetY = random.randint(0, 9)
			targetCell = self.board[targetY][targetX] 
		newPlayer = Player(playerId, targetX, targetY) 
		targetCell.player = newPlayer
		self.players.append(newPlayer)

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
		elif stevent.key == ord('d') or stevent.key == ord('l'):
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
					curRow.append(AsciiPixel(ord(cell.feature), AsciiPixel.WHITE)) 
				else:
					curRow.append(AsciiPixel(ord('@'), AsciiPixel.BLUE)) 
			rowList.append(curRow)
			curRow = []
		screen = Screen(rowList)
		return screen

