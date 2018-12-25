class Story():
	def __init__(self):
		super(Story, self).__init__()
		self.nodes = []
		self.variables = dict()

	def parse(self, json):
		for n in json:
			paragraph = Node(n)
			self.nodes.append(paragraph)

	def setVar(self,lhs,rhs):
		self.variables[lhs] = rhs

class Node():
	def __init__(self, paragraph_json):
		super(Node, self).__init__()
		
		# Preload of raw json before initializing classes
		self.id 		 	= paragraph_json['id'] 			if 'id' 		in paragraph_json else None
		self.narrative 	 	= paragraph_json['narrative'] 	if 'narrative' 	in paragraph_json else None
		self.look 	 		= paragraph_json['look'] 		if 'look' 		in paragraph_json else None
		self.pick 	 		= paragraph_json['pick'] 		if 'pick' 		in paragraph_json else None
		self._objects_raw 	= paragraph_json['objects'] 	if 'objects' 	in paragraph_json else None
		self._npcs_raw 	 	= paragraph_json['npcs'] 		if 'npcs' 		in paragraph_json else None

		# Initializing classes
		self.objects = []
		if(self._objects_raw is not None):
			for key in self._objects_raw:
				o = self._objects_raw[key]
				go = GameObject(o, name=key)
				self.objects.append(go)

	def findObjectByName(self, name):
		name = name.lower()

		for obj in self.objects:
			if(obj.name == name):
				return obj
				
		return None

class GameObject():
	def __init__(self,json, name='Ordinary  Object'):
		super(GameObject, self).__init__()
		self.name = name
		self.look = json['look'] if 'look' in json else None
		self.pick = json['pick'] if 'pick' in json else None
		self.open = json['open'] if 'open' in json else None