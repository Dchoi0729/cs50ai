"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for entry in row:
            if not entry == EMPTY:
                count += 1
    
    return X if count % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allowed_moves = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                allowed_moves.append((i,j))

    return allowed_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("invalid move")
    result_board = deepcopy(board)
    result_board[action[0]][action[1]] = player(board)

    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    
    # Check columns
    for i in range(len(board[0])):
        col = [row[i] for row in board]
        if len(set(col)) == 1:
            return col[0]
    
    # Check diagonal \
    diagonal_winner, i, j = board[0][0], 0, 0
    while True:
        if i > len(board) - 1 or j > len(board[0]) - 1:
            return diagonal_winner  
        if not diagonal_winner == board[i][j]:
            break
        i += 1
        j += 1

    
    # Check diagonal /
    diagonal_winner, i, j = board[2][0], 2, 0
    while True:
        if i < 0 or j > len(board[0]) - 1:
            return diagonal_winner  
        if not diagonal_winner == board[i][j]:
            break
        i -= 1
        j += 1

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
