from sudoku import *
import sys

def main():

    # Check usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python generate.py structure output")
    
    # Parse command-line arguments
    structure = sys.argv[1]
    output = sys.argv[2]

    try:
        sudoku = Sudoku(structure)
    except ValueError as error:
        print(error)
        sys.exit(1)

    board = sudoku.board

    for row in board:
        print(row)
    
if __name__ == "__main__":
    main()
