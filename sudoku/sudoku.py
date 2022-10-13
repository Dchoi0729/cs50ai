class Sudoku():
    def __init__(self, structure_file):
        self.SIZE = 9

        # Determine intial board configuration
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.initial_board = []
            for i in range(len(contents)):
                row = [*contents[i]]
                self.initial_board.append(row)

        # Convert all cells of the board to numbers
        # Check if structure is valid
        for row in self.initial_board:
            for i in range(len(row)):
                row[i] = int(row[i])
                if row[i] > 9 or row[i] < 0:
                    raise ValueError("Number must be between 0 and 9")
            if len(row) != self.SIZE:
                raise ValueError("Provide 9 by 9 grid")
        
        if len(self.initial_board) != self.SIZE:
            raise ValueError("Provide 9 by 9 grid")
    
    def neighbors(self, cell):
        """
        For a given cell, return a set of all cells on the
        same row, column, and square (3 by 3)
        """
        row, col = cell

        horizontal = set(
            (row,i) for i in range(self.SIZE)
        )
        
        vertical = set(
            (i,col) for i in range(self.SIZE)
        )
        
        square = set(
            (i,j) 
            for i in range((row//3)*3, (row//3)*3 + 3)
            for j in range((col//3)*3, (col//3)*3 + 3)
        )

        return (horizontal | vertical | square) - {cell}
    
