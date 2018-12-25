import json
import time
import random

from thebard.story.story import Story

class TheBard():
	"""docstring for TheBard"""
	def __init__(self, path=''):
		super(TheBard, self).__init__()
		self.path 		= path
		if self.path:
			file 			= open (self.path, 'r')
			self.raw 		= file.read()
			self.json 		= json.loads(self.raw)

			self.story = Story()
			self.story.parse(self.json)

		self.gameLoop 	 = False
		self.currentNode = 0
		self.debug 		 = False

	def start(self, debug=False):
		self.debug = debug

		command = 'not'

		if(not self.debug):
			self.tell([
				"Hello, my name is Bersi, The Bard.",
				"From now on I'll be guiding you through an exciting adventure.",
				"Just take a confortable seat and let's play.",
				'Just say "yes" if you want to proceed.'
			])
			command = input('>>> ')
		else:
			command = 'yes'

		if(command == 'yes'):
			self.gameLoop = True
			while(self.gameLoop):
				self.update()

		elif(command == 'no' or command == 'not'):
			self.end()
			exit(0)
		else:
			self.tell([
				'Sorry, didn\'t get what you jus said.',
				'I\'ll just leave you for now.',
				'Bye!'
			])
			self.end(defaultEndMessage=False)
			exit(0)

	def update(self):
		node = self.story.nodes[self.currentNode]
		self.tell(narrative=node.narrative)
		self.prompt()

	def end(self, defaultEndMessage=True):
		if(defaultEndMessage):
			self.tell([
					'Too bad. :(',
					'Hope to see ya again another time. :)'
				])

		self.gameLoop = False
		exit(0)

	
	def command(self,command):
		command = command.split()
		switcher = {
			'use' 		: self.commandNotImplementedYet,
			'wear' 		: self.commandNotImplementedYet,
			'look' 		: self.look,
			'see' 		: self.look,
			'pick' 		: self.pick,
			'attack' 	: self.commandNotImplementedYet,
			'open' 		: self.commandNotImplementedYet,
			'quit' 		: self.end,
			'exit' 		: self.end,

			# Commands for testing and debug
			'reload' 	: self.reload,
			'vardump'	: self.vardump,
			'node' 		: self.showCurrentNode
		}

		func = switcher.get(command[0], self.commandNotImplementedYet)
		if(func == self.look or func == self.pick):
			func(command[1:])
		else:
			func()

	def showCurrentNode(self):
		print(self.currentNode)
		self.prompt()

	def vardump(self):
		print(self.story.variables)
		self.prompt()

	def reload(self):
		file 			= open (self.path, 'r')
		self.raw 		= file.read()
		self.json 		= json.loads(self.raw)

		# self.story = Story()
		self.story.parse(self.json)
		self.prompt()

	def open(self, argArray=[]):
		# node = self.story.nodes[self.currentNode]
		pass

	def pick(self, argArray=[]):
		node = self.story.nodes[self.currentNode]
		if(len(argArray) > 0):
			if(len(node.objects) > 0):
				itemName = ' '.join(argArray)
				item = node.findObjectByName(itemName)

				if(item is not None):
					if(item.pick is not None):
						# Resolves the eval and the if and returns the lateIf if exists
						lr = self.resolve(item.pick)
						if lr is not None:
							# Executes the lateIf 
							lr.resolve(self)
					else:
						self.tell([
							"You can't pick {}. B".format(itemName)
						])
				else:
					self.tell([
						"There's nothing called \"{}\" in here. A".format(itemName)
					])
			else:
				self.tell([
					"There's nothing called \"{}\" in here. B".format(itemName)
				])
		else:
			self.tell([
				"I'm sorry, you can't pick this. =("
			])
				

		self.prompt()
		

	def look(self, argArray=[]):
		node = self.story.nodes[self.currentNode]
		if(len(argArray) > 0):
			if(len(node.objects) > 0):
				itemName = ' '.join(argArray)
				item = node.findObjectByName(itemName)

				if(item is not None):
					if(item.look is not None):
						lr = self.resolve(item.look)
						if lr is not None:
							lr.resolve(self)
					else:
						self.tell([
							"There's nothing special about {}. B".format(itemName)
						])
				else:
					self.tell([
						"There's nothing called \"{}\" in here. A".format(itemName)
					])
			else:
				self.tell([
					"There's nothing called \"{}\" in here. B".format(itemName)
				])
		else:
			if(node.look is not None):
				if('narrative' in node.look):
					self.tell(node.look['narrative'])

		self.prompt()

	def commandNotImplementedYet(self):
		self.tell([
			'Sorry I don\'t know how to proceed this way, yet... :(',
			'Please try another thing...'
		])

		self.prompt()

	def tell(self,narrative=[]):
		for speech in narrative:
			print('  The Bard is writing...', end="\r")
			
			if not self.debug:
				time.sleep(.25 + (random.random() * len(speech.split()) * .5))

			print('\r[The Bard says]: {}'.format(speech))

	def prompt(self):
		userInput = input('>>> ')
		self.command(userInput)

	@staticmethod
	def eval(self,obj):
		lhs = obj[0]
		op  = obj[1]
		rhs = obj[2]

		if op == '=':
			self.story.setVar(lhs,rhs)
		elif op == '==':
			if lhs in self.story.variables:
				return self.story.variables[lhs] == rhs
			else:
				return False
		elif op == '>':
			if lhs in self.story.variables:
				if isinstance(self.story.variables[lhs], (int, float, complex)):
					return self.story.variables[lhs] > rhs
				else:
					return False
			else:
				return False
		elif op == '<':
			if lhs in self.story.variables:
				if isinstance(self.story.variables[lhs], (int, float, complex)):
					return self.story.variables[lhs] < rhs
				else:
					return False
			else:
				return False
		elif op == '>=':
			if lhs in self.story.variables:
				if isinstance(self.story.variables[lhs], (int, float, complex)):
					return self.story.variables[lhs] >= rhs
				else:
					return False
			else:
				return False
		elif op == '<=':
			if lhs in self.story.variables:
				if isinstance(self.story.variables[lhs], (int, float, complex)):
					return self.story.variables[lhs] <= rhs
				else:
					return False
			else:
				return False

	def resolve(self,obj):
		if('eval' in obj):
			self.eval(self,obj['eval'])
		
		if('if' in obj):
			cr = Resolver(obj['if'])
			cr.resolve(self)
		
		if('narrative' in obj):
			self.tell(narrative=obj['narrative'])

		if('lateIf' in obj):
			cr = Resolver(obj['lateIf'])
			return cr
		else:
			return None

	def goto(self,nodeNumber):
		self.currentNode = nodeNumber

		node = self.story.nodes[self.currentNode]
		self.tell(node.narrative)
		self.prompt()

class Resolver():
	def __init__(self, json):
		super(Resolver, self).__init__()
		self.condition 	= json['condition'] if 'condition' 	in json else None
		self.andOp 		= json['and'] 		if 'and' 		in json else None
		self.orOp 		= json['or'] 		if 'or' 		in json else None
		self.thenOp 	= json['then'] 		if 'then' 		in json else None
		self.elseOp 	= json['else'] 		if 'else' 		in json else None

		self._return = False

	def resolve(self, bardInstance):

		# Test the main condition
		if self.condition is not None and bardInstance is not None:
			self._return = TheBard.eval(bardInstance,self.condition)
		else:
			self._return = False

		# Test the 'AND' support condition and makes a boolean AND with previous condition
		if self.andOp is not None and bardInstance is not None:
			self._return = self._return and TheBard.eval(bardInstance,self.andOp)
		else:
			self._return = self._return and False

		# Test the 'OR' support condition and makes a boolean OR with previous condition
		if self.orOp is not None and bardInstance is not None:
			self._return = self._return or TheBard.eval(bardInstance,self.orOp)
		else:
			self._return = self._return or False

		if self.thenOp is not None and bardInstance is not None:
			f = self.thenOp.split(':')

			if f[0] == 'GOTO':
				bardInstance.goto(int(f[1]))
