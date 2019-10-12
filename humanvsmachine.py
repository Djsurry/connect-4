import numpy
from qTable import Q, ternery
from qlearning import Board
def pBoard(b):
    for i in range(6):
        for j in b.state:
            t = ternery(j)
            while len(t) < 6:
                t = '0' + t
            print(t[i], end='')
        print()


def game():
	q = Q()
	q.jsonRecover('qTable.json')
	board = Board()
	while not board.gameOver():
		pBoard(board)
		c = int(input('Your move: ')) - 1
		print()
		board.transition(c, '1')
		action = q.choose_action(0.8, board.state)
		board.transition(action, '2')
	if board.isFull():
		print('tie')
	if board.winner == '1':
		print('u won')
	else:
		pBoard(board)
		print('u absolute fukcing trash u lost to a machine u deserve to be gunned down in the street like the degenerate you r')



game()