from keras.models import load_model
import numpy as np
from qTable import Q, ternery
from qlearning import Board
import time

def ternery(n):
    try:
        n = int(n)
    except TypeError:
        print(n)
        raise(TypeError)
    if n == 0:
        return ''
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def neural_network_choose(board, player, model):
	
	inputs = []
	for col in board.state:
		tern = ternery(col) if col != ' ' else ''
		a = [int(n) for n in list(tern)]
		for n, i in enumerate(a):
			if i == 2:
				a[n] = -1
		
		while len(a) != 6:
			a.append(0)
		inputs += a
	
	array = np.array([inputs])
	t = model.predict(array, batch_size=10).tolist()
	board.transition(t.index(max(t)), player)
	return board

def reinforcement_choose(board, player, q):
	
	action = q.choose_action(0.8, board.state)
	board.transition(action, player)
	return board


def play(q, model, player1 = 'nn'):

	board = Board()
	
	players = {'nn': '1', 'rl': '2'}
	if player1 == 'rl':
		players = {'rl': '1', 'nn': '2'}
	while not board.gameOver():
		t = time.time()
		board = neural_network_choose(board, players['nn'], model)
		t1 = time.time()-t
		if board.gameOver():
			break
		t = time.time()
		board = reinforcement_choose(board, players['rl'], q)
		t2 = time.time()-t
	return board.winner, t1, t2

def main():
	rl_wins = 0
	nn_wins = 0
	nn_avg = []
	rl_avg = []
	ties = 0
	t = time.time()
	q = Q()
	q.jsonRecover('qTable.json')
	print(f'loaded q table, took {time.time()-t}')
	t = time.time()
	model = load_model('nn/model/model.h5')
	print(f'loaded model, took {time.time()-t}')
	for i in range(10000):
		if i%2 == 0:
			player1 = 'nn'
		else:
			player1 = 'rl'
		result, t1, t2 = play(q, model, player1=player1)
		nn_avg.append(t1)
		rl_avg.append(t2)
		if result == '1':
			nn_wins += 1
		elif result == '2':
			rl_wins += 1
		else:
			ties += 1
		print(f'Finished {i}')
	print(f'RL: {rl_wins} NN: {nn_wins} Ties: {ties}')
	print(f'RL: {sum(rl_avg)/len(rl_avg)}s NN: {sum(nn_avg)/len(nn_avg)}s')
	quit() 

main()

