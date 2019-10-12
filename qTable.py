import json, random
import numpy as np

def ternery(n):
	try:
		n = int(n)
	except TypeError:
		print(n)
		raise(TypeError)
	if n == 0:
		return '0'
	nums = []
	while n:
		n, r = divmod(n, 3)
		nums.append(str(r))
	return ''.join(reversed(nums))

def steralize(state):
		return ' '.join([str(n) for n in state])

class Q:
	def __init__(self):
		self.table = {} # {state1: [a_1, a_2, a_3, a_4, a_5, a_6, a_7], ...}

	
	def update(self, state, action, value):
		self.table[steralize(state)][action] = value

	def get_value(self, state, action):
		return self.table[steralize(state)][action]

	def choose_action(self, epsilon, state):
		if steralize(state) not in self.table:
			self.table[steralize(state)] = np.zeros(7)
			
			return random.randint(0,6)

		best = max(self.table[steralize(state)])
		if random.randint(0,100) < epsilon*100: # Choose random option
			action = random.randint(0,6)
		else:
			action, = np.where(self.table[steralize(state)] == best)
			if len(action) != 1:
				action = action[0]
		return action

	def jsonDump(self, f):
		print('Dumping to file {}'.format(f))
		new = {}
		for key in self.table.keys():
			new[key] = [float(n) for n in list(self.table[key])]
		with open(f, 'w') as f:
			json.dump(new, f)

	def jsonRecover(self, f):
		print('Recovering from file {}'.format(f))
		with open(f) as f:
			table = json.load(f)
		for key in table.keys():
			self.table[key] = np.array(table[key])


