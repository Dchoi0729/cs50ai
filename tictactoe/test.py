import tictactoe
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


board = [[O, O, X],
            [X, O, O],
            [X, X, O]]
print(tictactoe.player(board))

print(len(board))
print(len(board[0]))

print(tictactoe.actions(board))



print(board)

#print(tictactoe.result(board, (0,3)))

a = ['X', 'O', 'X']
print(len(set(a)))

print(tictactoe.winner(board))