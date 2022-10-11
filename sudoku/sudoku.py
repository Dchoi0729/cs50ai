class Sudoku():
    def __init__(self, structure_file):
        self.HEIGHT = 9
        self.WIDTH = 9

        # Determine intial board configuration
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.board = []
            for i in range(len(contents)):
                row = contents[i].split()
                self.board.append(row)
        
        # Convert all cells of the board to numbers
        # Check if structure is valid
        for row in self.board:
            for i in range(len(row)):
                row[i] = int(row[i])
                if row[i] > 9 or row[i] < 0:
                    raise ValueError("Number must be between 0 and 9")
            if len(row) != self.WIDTH:
                raise ValueError("Provide 9 by 9 grid")
        
        if len(self.board) != self.HEIGHT:
            raise ValueError("Provide 9 by 9 grid")
    
    def find_square(self, cell):
        pass
