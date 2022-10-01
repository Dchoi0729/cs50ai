import tictactoe
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