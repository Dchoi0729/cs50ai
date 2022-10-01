import tictactoe
from copy import deepcopy
# import the builtin time module
import time

X = "X"
O = "O"
EMPTY = None


board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
        



# Grab Currrent Time Before Running the Code
start = time.time()

print(tictactoe.minimax(board))

# Grab Currrent Time After Running the Code
end = time.time()

#Subtract Start Time from The End Time
total_time = end - start
print("\n"+ str(total_time))

'''
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
'''