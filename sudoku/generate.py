import argparse
import copy
import sys
import time

from PIL import Image, ImageDraw, ImageFont
from sudoku import Sudoku


def main():
    # Create command line parser that can detail usage
    parser = argparse.ArgumentParser(description="Program Usage",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--log", action="store_true", help="show log of all backtrack search")
    parser.add_argument("-c", "--compare", action="store_true", help="prints initial sudokuboard next to answer")
    parser.add_argument("src", help="Source file of inital sudoku configuration")
    parser.add_argument("output", help="Name of output png file (stored in solutions dir)")
    
    # Load command line data
    config = vars(parser.parse_args())
    structure = config["src"]
    output = f"./solutions/{config['output']}.png"
    show_log = config["log"]
    show_init = config["compare"]

    # Generate sudoku based on structure
    try:
        sudoku = Sudoku(structure)
    except ValueError as error:
        print(error)
        sys.exit(1)
    
    # Create sudoku solver with given tags
    solver = SudokuSolver(sudoku, show_log=show_log, show_init=show_init)
    
    # Solve sudoku, adding decorator if log print is requested
    if show_log:
        solution = measure_time(solver.solve)()
    else:
        solution = solver.solve()

    # Print result
    if solution is None:
        print("No solution.")
    else:
        solver.save(solution, output)
    
    # Print log details
    if show_log:
        print(f"Backtrack function count: {solver.backtrack_counter}")
        print(f"Numbers tested: {solver.numers_tested}")


class SudokuSolver():
    def __init__(self, sudoku, show_log=False, show_init=False):
        """
        Create new CSP sudoku solver.
        """
        self.sudoku = sudoku
        self.domains = {
            (i,j): (
                [k for k in range(1,10)] if self.sudoku.initial_board[i][j] == 0
                else [self.sudoku.initial_board[i][j]]
            )
            for i in range(9) for j in range(9)
        }
        self.show_log = show_log
        self.show_init = show_init
        self.backtrack_counter = 0
        self.numers_tested = 0

    def print(self, assignment):
        """
        Print sudoku assignment to the terminal.
        """
        for i in range(self.sudoku.SIZE):
            for j in range(self.sudoku.SIZE):
                if (i,j) in assignment.keys():
                    if j == 8:
                        print(f"{assignment[(i,j)]} ")
                    else:
                        print(f"{assignment[(i,j)]} ", end="")
                else:
                    if j == 8:
                        print("  ")
                    else:
                        print("  ", end="")
                if j == 2 or j == 5:
                    print("| ", end="")
            if i == 2 or i == 5:
                print("----------------------")

    def save(self, solution, filename):
        """
        Save finished sudoku to an image file.
        If show_init is true, prints intial configuration 
        side by side with the solution
        """
        cell_size, cell_border = 100, 2
        interior_size = cell_size - 2 * cell_border
        gap, divider = 5, 10
        canvas_width = (9 * cell_size + 2 * gap if not self.show_init 
                        else 2 * (9 * cell_size + 2 * gap) + divider)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (canvas_width, 9 * cell_size + 2 * gap),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        offset = 9 * cell_size + 2 * gap + divider if self.show_init else 0

        for i in range(9):
            for j in range(9):
                # Set offset to create borders seperating 3 by 3 squares
                x_offset = 0 if i < 3 else 2 if i > 5 else 1
                y_offset = 0 if j < 3 else 2 if j > 5 else 1

                if self.show_init:
                    rect = [
                        (j * cell_size + cell_border + y_offset * gap,
                            i * cell_size + cell_border + x_offset * gap),
                        ((j + 1) * cell_size - cell_border + y_offset * gap,
                            (i + 1) * cell_size - cell_border + x_offset * gap)
                    ]
                    number = self.sudoku.initial_board[i][j]

                    # Draw rectangular cell for the number
                    draw.rectangle(rect, fill="white")

                    # Store size of number in w, h
                    no, need, w, h = draw.textbbox((0,0), str(number), font=font)

                    # Draw number centered in cell
                    if number != 0:
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10),
                            str(number), fill="black", font=font
                        )
                
                number = solution[(i,j)]
                color = "black" if self.sudoku.initial_board[i][j] != 0 else "blue"
                
                rect = [
                    (j * cell_size + cell_border + y_offset * gap + offset,
                        i * cell_size + cell_border + x_offset * gap),
                    ((j + 1) * cell_size - cell_border + y_offset * gap + offset,
                        (i + 1) * cell_size - cell_border + x_offset * gap)
                ]

                # Draw rectangular cell for the number
                draw.rectangle(rect, fill="white")

                # Store size of number in w, h
                no, need, w, h = draw.textbbox((0,0), str(number), font=font)

                # Draw number centered in cell
                draw.text(
                    (rect[0][0] + ((interior_size - w) / 2),
                        rect[0][1] + ((interior_size - h) / 2) - 10),
                    str(number), fill=color, font=font
                )

        img.save(filename)

    def solve(self):
        """
        Enforce arc consistency, and then solve the CSP.
        (node consistency is unnecessary)
        """

        self.ac3()
        inital_assignment = {
            (i, j) : self.domains[(i,j)][0]
            for i in range(9) for j in range(9)
            if len(self.domains[(i,j)]) == 1
        }
        return self.backtrack(inital_assignment)

    def revise(self, x, y):
        """
        Make cell `x` arc consistent with cell `y`.
        Removes values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        
        # Check if y has more than one value in its domain
        if len(self.domains[y]) != 1:
            return False

        # Check if y and x are not related
        if y not in self.sudoku.neighbors(x):
            return False
        
        for x_val in self.domains[x].copy():
            y_val = list(self.domains[y])[0]
            if x_val == y_val:
                revised = True
                self.domains[x].remove(x_val)

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = [
            ((i1,j1),(i2,j2)) 
            for i1 in range(9) for j1 in range(9)
            for i2 in range(9) for j2 in range(9)
            if not (i1 == i2 and j1 == j2)
        ] if arcs == None else arcs

        while len(queue) > 0:
            x,y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.sudoku.neighbors(x) - {y}:
                    queue.append((z,x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        cell); return False otherwise.
        """
        return len(assignment) == self.sudoku.SIZE * self.sudoku.SIZE

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., no numbers
        violate sudoku rule); return False otherwise.
        """
        for var in assignment.keys():
            value = assignment[var]
            for other_var in assignment.keys():
                if other_var in self.sudoku.neighbors(var):
                    if value == assignment[other_var]:
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        """
        
        def rule_out(value):
            """
            Return the number of values a given value for var can rule out
            for neighboring variables
            """
            counter = 0
            # For all neighboring variables not yet assigned a value
            for other in self.sudoku.neighbors(var) - set(assignment.keys()):
                if value in self.domains[other]:
                    counter += 1
                
            return counter

        return sorted(self.domains[var], key=rule_out)
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. 
        """
        
        unassigned = set(self.domains.keys()) - set(assignment.keys())
        
        sorted_unassigned = sorted(
            unassigned, 
            key=lambda var:(len(self.domains[var]))
        )

        return sorted_unassigned.pop(0)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        self.backtrack_counter += 1
        
        # Assignment complete
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            self.numers_tested += 1
            assignment[var] = value
            if self.show_log:
                print("***********************")
                print(f"{var} : {value}")
                print()
                self.print(assignment)
            if self.consistent(assignment):
                prev_domain = copy.deepcopy(self.domains)
                self.domains[var] = [value]
                inference = self.inference(var, assignment)
                if inference != None:
                    assignment.update(inference)
                result = self.backtrack(assignment)
                if result != None:
                    return result
                if inference != None:
                    # Delete all the inferences added to assignment
                    for inference_var in inference.keys():
                        del assignment[inference_var]
                
            # Assignment of value is wrong for var, delete assignemnt
            del assignment[var]
            self.domains = prev_domain
        
        # Current var has no value in its domain that works
        return None

    def inference(self, var, assignment):
        """
        Implements ac3 algorithm on given assignment of var to maintain arc consistency

        Return a dict of assignments that can be inferred from given assigments;
        return None if given assignment leads to no farther future progress
        """

        self.ac3([(other, var) for other in self.sudoku.neighbors(var)])

        # For variables that aren't yet assigned check if new inferences can be made
        # aka a variable has only one value left in domain (add) or none left (abort)
        new_inferences = dict()
        for var in set(self.domains.keys()) - set(assignment.keys()):
            if len(self.domains[var]) == 0:
                return None
            if len(self.domains[var]) == 1:
                new_inferences[var] = list(self.domains[var])[0]
        return new_inferences


def measure_time(func):
    '''Decorator that reports the execution time.'''
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
          
        print(f"Time to solve: {end-start} seconds")
        return result

    return wrapper


if __name__ == "__main__":
    main()