import tictactoe
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
print(tictactoe.player(board))

print(len(board))
print(len(board[0]))

print(tictactoe.actions(board))



print(board)

#print(tictactoe.result(board, (0,3)))


print(tictactoe.winner(board))
print(tictactoe.terminal(board))
print(tictactoe.utility(board))
print(tictactoe.minimax(board))