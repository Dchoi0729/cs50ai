class Sudoku():
    """
    A class to represent a sudoku board
    """
    def __init__(self, structure_file):
        self.SIZE = 9

        # Determine intial board configuration
        with open(structure_file, encoding="utf-8") as f:
            contents = f.read().splitlines()
            self.initial_board = []
            for i, line in enumerate(contents):
                row = [*line]
                self.initial_board.append(row)

        # Convert all cells of the board to numbers
        # Check if structure is valid
        for row in self.initial_board:
            if len(row) != self.SIZE:
                raise ValueError("Provide 9 by 9 grid")
            for i in range(self.SIZE):
                row[i] = int(row[i])
                if row[i] > 9 or row[i] < 0:
                    raise ValueError("Number must be between 0 and 9")

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
    