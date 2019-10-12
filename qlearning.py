import numpy as np
import time, random, json
from qTable import ternery, Q, steralize
'''
TODO
1. Make reward function work
2. Make training work
3. Implement winning
'''
class Board:
	# board object contains a state, a ternery represenation of the board, ie each column is represented by a number
	def __init__(self):
		self.state = np.zeros(7, dtype=int)
		self.winner = None
	def isFull(self):
		l = 0
		for i in range(7):
			column = self.state[i]
			tern = ternery(column)
			if len(tern) == 6:
				l += 1
		if l == 7:
			return True
		else:
			return False


	def transition(self, column_choice, player):
		column = self.state[column_choice]
		tern = ternery(column)
		if len(tern) == 6:
			return False
		new = str(player) + tern if tern != '0' else str(player)
		self.state[column_choice] = int(new, 3)
		return True

	def gameOver(self):
		arr = []
		for column in self.state:
			tern = ternery(column)
			while len(tern) != 6:
				tern = '0' + tern
			arr.append(list(tern))

		p1_rows = findInARow(arr, '1')
		p2_rows = findInARow(arr, '2')
		if 4 in [len(n) for n in p1_rows]:
			self.winner = '1'
			return True
		if 4 in [len(n) for n in p2_rows]:
			self.winner = '2'
			return True
		
		elif self.isFull():
			return True
		else:
			return False


def get_reward(state, stateprime, player):
	# TODO
	'''
	REWARD RULESET
	1. 1 point for every 2 in a row
	2. 2 points for every 3 in a row
	3. -1 point for every opponent 2 in a row
	4. -2 points for every opponent 3 in a row
	5. 9999999? for four in a row
	6. -9999999? for opponent 4 in a row
	'''
	scorecard = {2: 10, 3: 100, 4: 99999999}
	# brute force
	arr = []
	for column in state:
		tern = ternery(column)
		while len(tern) != 6:
			tern = '0' + tern
		arr.append(list(tern))

	p1_rows = findInARow(arr, '1')
	p2_rows = findInARow(arr, '2')

	
	state1_score = 0
	for i in p1_rows:
		state1_score = state1_score + scorecard[len(i)] if player == '1' else state1_score - scorecard[len(i)]
	for i in p2_rows:
		state1_score = state1_score - scorecard[len(i)] if player == '1' else state1_score + scorecard[len(i)]

	arr = []
	for column in stateprime:
		tern = ternery(column)
		while len(tern) != 6:
			tern = '0' + tern
		arr.append(list(tern))

	p1_rows = findInARow(arr, '1')
	p2_rows = findInARow(arr, '2')

	
	state2_score = 0
	
	for i in p1_rows:
		state2_score = state2_score + scorecard[len(i)] if player == '1' else state2_score - scorecard[len(i)]
	for i in p2_rows:
		state2_score = state2_score - scorecard[len(i)] if player == '1' else state2_score + scorecard[len(i)]

	return state2_score - state1_score if player == '1' else state1_score - state2_score

def findAdj(arr, c, r):
	looking_for = arr[c][r]
	adj = []
	adj_coor = [
		(c+1, r),
		(c-1, r),
		(c, r+1),
		(c, r-1),
		(c+1, r+1),
		(c-1, r+1),
		(c+1, r-1),
		(c-1, r-1),
	]
	for coor in adj_coor:
		try:
			if arr[coor[0]][coor[1]] == looking_for:
				adj.append(coor)
		except IndexError:
			continue
	return adj

def findInARow(arr, player):
	found = []
	for c, column in enumerate(arr):
		for r, cell in enumerate(column):
			if cell == player:
				adj = findAdj(arr, c, r)
				for i in adj:
					direction = (i[0]-c, i[1]-r)
					f = None
					try:
						if arr[i[0] + direction[0]][i[1] + direction[1]] == player:
							if arr[i[0] + 2*direction[0]][i[1] + 2*direction[1]] == player:
								f = [(c, r), (c+direction[0], r+direction[1]), (c+2*direction[0], r+2*direction[1]), (c+3*direction[0], r+3*direction[1])]
							elif arr[i[0] + 2*direction[0]][i[1] + 2*direction[1]] == '0':
								f = [(c, r), (c+direction[0], r+direction[1]), (c+2*direction[0], r+2*direction[1])]
						if f is None and arr[i[0] + 2*direction[0]][i[1] + 2*direction[1]] == '0' and arr[i[0] + direction[0]][i[1] + direction[1]] == '0':
							f = [(c, r), (c+direction[0], r+direction[1])]
					except IndexError:
						pass

					
					if f and sorted(f) not in found:
						found.append(sorted(f))

	# removes sublists, ie if u had [(3, 1), (3, 2), (3, 3), (3, 4)] and [(3, 2), (3, 3), (3, 4)] in found this removes the latter as it is a sublist
	to_remove = []
	for i in found:
		for j in found:
			if len(j) > len(i):
				good = True
				for t in i:
					if t not in j:
						good = False
						break
				if good:
					to_remove.append(i)


	return [n for n in found if n not in to_remove]

	
	




# some variables, epsilon, alpha and gamma
e = 0.3
a = 0.5
g = 0.5

'''
q_new(s, a) = (1-a)*q(s, a) + a(r + g + max(Q(s+1, a)))
'''
ties = 0
wins= 0
def train():
	global ties, wins
	try:
		q.jsonRecover('qTable.json')
	except FileNotFoundError:
		print('No backup found. Creating new table')
	i = 0
	while True:
		board = Board()
		print('Game {}'.format(i))
		while not board.gameOver():
			# ---------- PLAYER 1 ---------- #
			state = np.copy(board.state)
			# choose action
			action = q.choose_action(e, state)
			
			# update env
			board.transition(action, '1')
			state_prime = np.copy(board.state)
			# find reward
			reward = get_reward(state, state_prime, '1')
			if reward > 999999 or reward < -999999:
				q.table[steralize(state_prime)] = np.array([reward for n in range(7)])
			else:
			# update q
				try: 
					value = (1-a)*q.get_value(state, action) + a*(reward + g*max(q.table[steralize(state_prime)]))
				except KeyError:
					value = (1-a)*q.get_value(state, action) + a*(reward)
				q.update(state, action, value)
			if board.gameOver():
				break
			# ---------- PLAYER 2 ---------- #
			state = np.copy(board.state)
			# choose action
			action = q.choose_action(e, state)
			# update env
			board.transition(action, '2')
			state_prime = np.copy(board.state)
			# find reward
			reward = get_reward(state, state_prime, '2')
			# update q
			if reward > 999999 or reward < -999999:
				q.table[steralize(state_prime)] = np.array([reward for n in range(7)])
			else:
			# update q
				try: 
					value = (1-a)*q.get_value(state, action) + a*(reward + g*max(q.table[steralize(state_prime)]))
				except KeyError:
					value = (1-a)*q.get_value(state, action) + a*(reward)
				q.update(state, action, value)
			q.update(state, action, value)
		if board.isFull():
			ties += 1
		else:
			wins += 1
		i += 1

	q.jsonDump('qTable.json')

if __name__ == '__main__':
	q = Q()
	try:
		train()
	except KeyboardInterrupt:
		print('\nTraining session ended with {} ties and {} wins'.format(ties, wins))
		q.jsonDump('qTable.json')


