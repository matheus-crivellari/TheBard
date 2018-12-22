import json
import time
import random

from thebard.story.story import Story

class TheBard():
	"""docstring for TheBard"""
	def __init__(self, path=''):
		super(TheBard, self).__init__()
		self.path 		= path
		file 			= open (self.path, 'r')
		self.raw 		= file.read()
		self.json 		= json.loads(self.raw)

		self.story = Story()
		self.story.parse(self.json)
		self.gameLoop = False

		self.currentNode = 0

	def start(self):

		self.tell([
			'Hello, from now on I\'ll be guiding you through an exciting adventure.',
			'Just take a confortable seat and let\'s play.',
			'Say "yes" to proceed.'
		])

		command = input('>>> ')
		if(command == 'yes'):

			self.gameLoop = True
			while(self.gameLoop):
				self.update()

		elif(command == 'no'):
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
	
	def command(self,command):
		command = command.split()
		switcher = {
			'use' 		: self.commandNotImplementedYet,
			'wear' 		: self.commandNotImplementedYet,
			'look' 		: self.look,
			'pick' 		: self.commandNotImplementedYet,
			'attack' 	: self.commandNotImplementedYet,
			'open' 		: self.commandNotImplementedYet,
			'quit' 		: self.end
		}

		func = switcher.get(command[0], self.commandNotImplementedYet)
		if(func == self.look):
			func(command[1:])
		else:
			func()

	def look(self, argArray=[]):
		node = self.story.nodes[self.currentNode]
		if(len(argArray) > 0):
			if(len(node.objects) > 0):
				itemName = ' '.join(argArray)
				item = node.findObjectByName(itemName)

				if(item is not None):
					if(item.look is not None):
						if(item.look.narrative is not None):
							self.tell(item.look.narrative)
						else:
							self.tell([
								"There's nothing special about {}.".format(itemName)
							])
					else:
						self.tell([
							"There's nothing special about {}.".format(itemName)
						])
				else:
					self.tell([
						"There's nothing called \"{}\" in here.".format(itemName)
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
			time.sleep(.25 + (random.random() * len(speech.split()) * .5))
			print('\r[The Bard says]: {}'.format(speech))

	def prompt(self):
		userInput = input('>>> ')
		self.command(userInput)

	def resolve(self,obj):
		if('narrative' in obj):
			self.tell(narrative=obj['narrative'])

		if('eval' in obj):
			# TO-DO
			pass

		if('if' in obj):
			cr = Resolver(obj['if'])
			cr.resolve(self)

		if('lateIf' in obj):
			cr = Resolver(obj['if'])
			return cr
		else:
			return None

class Resolver():
	def __init__(self, json):
		super(Resolver, self).__init__()
		self.condition 	= json['condition'] if 'condition' 	in json else None
		self.andOp 		= json['andOp'] 	if 'andOp' 		in json else None
		self.orOp 		= json['orOp'] 		if 'orOp' 		in json else None
		self.thenOp 	= json['thenOp'] 	if 'thenOp' 	in json else None
		self.elseOp 	= json['elseOp'] 	if 'elseOp' 	in json else None

	def resolve(self, bardInstance):
		return False
