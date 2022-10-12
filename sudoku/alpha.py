from sudoku import *
from generate import *
import sys

def main():

    
    sudoku = Sudoku("structure.txt")
    solver = SudokuSolver(sudoku)
    print(sudoku.neighbors((1,3)))
    print(solver.domains)

    queue = [
        ((i1,j1),(i2,j2)) 
        for i1 in range(9) for j1 in range(9)
        for i2 in range(9) for j2 in range(9)
        if not (i1 == i2 and j1 == j2)
    ]
    print(queue)


    
if __name__ == "__main__":
    main()
