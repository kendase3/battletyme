"""
	a small, turn-based game in which players try to kill
			other players!
"""

import time, random, os, sys 

sys.path.insert(0, os.path.join("..", "every", "common"))

# from every/common 
from game import Game
from screen import Screen
from asciipixel import AsciiPixel
from stevent import Stevent

# locals 
from display import Display

class Thing:
	"""
		all things are things.  a thing can be seen on the screen
	"""
	def __init__(self, ascii='?', asciiColor=None):
		if asciiColor == None:
			asciiColor = AsciiPixel.WHITE 
		self.ascii = ascii
		self.asciiColor = asciiColor

class Event:
	"""
		an event to tell the users WTF
		it is not used for game logic purposes,
		just for news items in the event ticker
	"""	
	NOTHING_TYPE = 0
	ATTACK_TYPE = 1 
	HIT_TYPE = 2
	MISS_TYPE = 3 
	DEATH_TYPE = 4 
	TURN_TYPE = 5
	MOVE_TYPE = 6
	def __init__(self, type=None, participants=None):
		if type == None:
			type = Event.NOTHING_TYPE
		self.type = type
		self.participants = participants
	
	def __repr__(self):
		if self.type == Event.NOTHING_TYPE:
			return "Nothing happens!"	
		elif self.type == Event.ATTACK_TYPE:
			return "%s attacks %s!" % (
					self.participants[0], self.participants[1]) 
		elif self.type == Event.HIT_TYPE:
			return "%s hits %s for %d damage!" % (
					self.participants[0], self.participants[1],
					self.participants[2])
		elif self.type == Event.MISS_TYPE:
			return "%s swings and misses %s" %(
					self.participants[0], self.participants[1])
		elif self.type == Event.DEATH_TYPE:
			return "%s has died!" % self.participants
		elif self.type == Event.TURN_TYPE:
			return "It is now %d's turn." % self.participants
		elif self.type == Event.MOVE_TYPE:
			return "player%d has moved %s" % (
					self.participants[0],
					self.participants[1]) 
		else:
			return "OH NO!  WHAT KIND OF EVENT IS THIS?  FREAK OUT!"

	def __str__(self):
		return repr(self)

class Cell(Thing):
	WALL = 'W', AsciiPixel.WHITE 
	FLOOR = '.', AsciiPixel.WHITE 
	def __init__(self, type = None):
		if type == None:
			type = Cell.WALL
		Thing.__init__(self, type[0], type[1])  
		self.creature = None
		self.objects = []
		self.type = type 

	def render(self):
		"""
			return an ascii-pixel representation of yourself
		"""
		ret = None
		if self.creature != None:
			ret = AsciiPixel(self.creature.ascii, self.creature.asciiColor) 	
		elif len(self.objects) > 0:
			#TODO: implement called data members 
			ret = AsciiPixel(self.objects[-1].ascii, self.objects[-1].asciiColor) 
		else:
			# if there's no player there, and 
			# there aren't any objects on the ground
			# then print the kind of cell
			ret = AsciiPixel(self.ascii, self.asciiColor)
		return ret


class Move:
	UP = 'up'
	DOWN = 'down'
	LEFT = 'left'
	RIGHT = 'right'	

class Creature(Thing): 
	"""
		eventually i'll have non-player participants!
	"""
	def __init__(self, x, y, type, maxHp):
		self.x = x
		self.y = y
		self.type = type
		self.dead = False
		self.maxHp = maxHp
		self.hp = maxHp

class Player(Creature):
	def __init__(self, id, x, y):
		Creature.__init__(self, x, y, 'player', 10)
		self.id = id
		self.nextMove = None
		self.dodge = 5 
		self.ascii = '@'
		self.asciiColor = AsciiPixel.BLUE

class Arena(Game):
	WIDTH = 10
	HEIGHT = 10
	SECONDS_PER_TURN = 2
	EVENT_LIMIT = 30
	def __init__(self):
		self.creatures = []
		self.board = [[Cell() for j in range(Arena.WIDTH)]
				for i in range(Arena.HEIGHT)]
		for i in range(2, 8):
			for j in range(2, 8):
				self.board[i][j].type = Cell.FLOOR
				self.board[i][j].ascii = Cell.FLOOR[0]
				self.board[i][j].asciiColor = Cell.FLOOR[1]
		self.startTime = time.time() 
		self.lastIterated = self.startTime
		self.curCreatureIndex = 0
		self.events = []

	def trimEvents(self):
		if len(self.events) > Arena.EVENT_LIMIT:
			self.events = self.events[(-1 * Arena.EVENT_LIMIT):]

	def iterate(self):
		curTime = time.time()
		self.trimEvents()
		if curTime - self.lastIterated > Arena.SECONDS_PER_TURN:
			self.handleTurn()
			print "New Turn!  Current player=%d" % self.curCreatureIndex 
			print "*** EVENT LOG ***"
			print repr(self.events)
			print "*** END EVENT LOG ***"
			print "current # of creatures: %d" % len(self.creatures)
			self.lastIterated = curTime

	def handleTurn(self):
		# then we process the next player's move 
		if len(self.creatures) == 0:
			return
		# at the last minute we update the index just in case someone quit
		self.curCreatureIndex = self.curCreatureIndex % len(self.creatures)
		creature = self.creatures[self.curCreatureIndex] 			
		if creature.type != 'player':
			creature.getNextMove()
		if creature.nextMove == None:
			print 'The current player did not move!'
			nothingEvent = Event()
			self.events.append(nothingEvent)
			self.incrementTurn()
			return
		xOffset = 0
		yOffset = 0
		if creature.nextMove == Move.LEFT:
			xOffset = -1
			yOffset = 0
		elif creature.nextMove == Move.RIGHT:
			xOffset = 1
			yOffset = 0
		elif creature.nextMove == Move.UP:
			xOffset = 0
			yOffset = -1	
		elif creature.nextMove == Move.DOWN: 
			xOffset = 0
			yOffset = 1
		newX = creature.x + xOffset
		newY = creature.y + yOffset
		if newX >= 0 and newX < len(self.board[0]) and (
				newY >= 0 and newY < len(self.board) and
				self.board[newY][newX].type == Cell.FLOOR):
			if self.board[newY][newX].creature == None:
				# if no one's there, we move there
				print "creature move %s accepted!" % creature.nextMove 
				moveEvent = Event(Event.MOVE_TYPE, 
						(creature.id, creature.nextMove)) 
				self.events.append(moveEvent)
				self.board[creature.y][creature.x].creature = None
				self.board[newY][newX].creature = creature 
				creature.x = newX
				creature.y = newY
			else: 
				# we attack that player standing there!
				attacker = creature 
				attackee = self.board[newY][newX].creature
				self.handleAttack(attacker, attackee) 	
		else:
			print "creature move of %s not accepted!" % creature.nextMove
		creature.nextMove = None
		self.incrementTurn()

	def incrementTurn(self):
		curCreature = None 
		while curCreature == None or curCreature.dead:
			self.curCreatureIndex += 1
			self.curCreatureIndex = self.curCreatureIndex % len(self.creatures)
			curCreature = self.creatures[self.curCreatureIndex] 
		turnEvent = Event(Event.TURN_TYPE, curCreature.id)  
		self.events.append(turnEvent)

	def handleAttack(self, attacker, attackee): 
		self.events.append(Event(Event.ATTACK_TYPE, (
				("player%d" % attacker.id),
				("player%d" % attackee.id)))) 
				 
		hitRoll = random.randint(0, 9)
		damageRoll = random.randint(0, 9)
		if hitRoll >= attackee.dodge: 
			self.events.append(Event(Event.HIT_TYPE, (
					("player%d" % attacker.id), 
					("player%d" % attackee.id), 
					hitRoll)))	
			attackee.hp -= hitRoll
			if attackee.hp < 0:
				# atackee dies
				self.removePC(attackee)
				self.events.append(Event(
						Event.DEATH_TYPE, "player%d" % attackee.id))
		else:
			self.events.append(Event(Event.MISS_TYPE, (
					("player%d" % attacker.id),
					("player%d" % attackee.id))))

	def addPlayer(self, playerId):
		targetX = random.randint(0, 9)
		targetY = random.randint(0, 9) 
		targetCell = self.board[targetY][targetX] 
		while targetCell.creature != None or targetCell.type != Cell.FLOOR:
			targetX = random.randint(0, 9)
			targetY = random.randint(0, 9)
			targetCell = self.board[targetY][targetX] 
		newPlayer = Player(playerId, targetX, targetY) 
		targetCell.creature = newPlayer
		self.creatures.append(newPlayer)

	def removePlayer(self, playerId):
		targetPlayer = None
		found = False
		targetPlayer = None
		for creature in self.creatures:
			if creature.type == 'player' and creature.id == playerId:
				found = True
				targetPlayer = creature 
				break
		if targetPlayer == None:
			print 'unable to find player to remove'
			return
		self.creatures.remove(targetPlayer)
		if not targetPlayer.dead:
			targetCell = self.board[targetPlayer.y][targetPlayer.x]
			targetCell.creature = None
		return

	def removePC(self, player):
		"""
			the player is still present, but their PC has died
			TODO: also add checking for this having happened
			inside removePlayer  
	
			either playerId or player are sufficient arguments
		"""
		# is player a playerId?  if so, we need to find the actual player 
		if isinstance(player, int):
			for creature in self.creatures:
				if creature.type == 'player' and creature.id == playerId:
					player = creature
		if player == None:
			print 'could not find PC to remove'
		else:
			player.dead = True
			targetCell = self.board[player.y][player.x]
			targetCell.creature = None			

	def getPlayer(self, playerId):
		for creature in self.creatures:
			if creature.type == 'player' and creature.id == playerId:
				return creature 
		print 'unable to find player'
		return None

	def handleInput(self, stevent, playerId):
		curPlayer = self.getPlayer(playerId)
		if curPlayer == None:
			return
		if stevent.type == Stevent.QUIT:
			print "###ATTEMPTING TO REMOVE PLAYER %d" % playerId
			self.removePlayer(playerId)
			return
		if curPlayer.dead:
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
		print "player %d's next move is currently %s" % (
				curPlayer.id, curPlayer.nextMove) 

	def getScreen(self, playerId): 
		player = self.getPlayer(playerId)
		display = Display(self.board, self.events)	
		player = self.getPlayer(playerId)
		curScreen = display.getScreen(player)
		return curScreen



