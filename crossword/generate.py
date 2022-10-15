import sys

from copy import deepcopy
from crossword import *

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, words in self.domains.items():
            length = variable.length
            for word in words.copy():
                if not len(word) == length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised, overlaps = False, self.crossword.overlaps[x, y]

        if overlaps == None:
            return False
            
        for x_word in self.domains[x].copy():
            consistent = False
            x_char = x_word[overlaps[0]]
            for y_word in self.domains[y]:
                y_char = y_word[overlaps[1]]
                if x_char == y_char:
                    consistent = True
                    break
            # No word in y's domain works with x_word
            if not consistent:
                revised = True
                self.domains[x].remove(x_word)

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
            (var1, var2) 
            for var1 in self.crossword.variables 
            for var2 in self.crossword.variables 
            if not var1 == var2
        ] if arcs == None else arcs

        while len(queue) > 0:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        # Check if any two words with overlap "fit" together
        for var in assignment.keys():
            word = assignment[var]
            for other_var in assignment.keys():
                if not var == other_var:
                    other_word = assignment[other_var]
                    overlap = self.crossword.overlaps[var, other_var]
                    if overlap == None:
                        continue
                    if not word[overlap[0]] == other_word[overlap[1]]:
                        return False
        
        # Check if all words are unique
        return len(assignment) == len(set(assignment.values()))

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def rule_out(value):
            """
            Return the number of values the given value for var can rule out
            for neighboring variables
            """
            counter = 0
            # For all neighboring variables not yet assigned a value
            for other in self.crossword.neighbors(var) - set(assignment.keys()):
                overlap = self.crossword.overlaps[var, other]
                var_letter = value[overlap[0]]
                for other_value in self.domains[other]:
                    other_letter = other_value[overlap[1]]
                    if not var_letter == other_letter:
                        counter += 1
                
            return counter

        return sorted(self.domains[var], key=rule_out)
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = self.crossword.variables - set(assignment.keys())

        sorted_unassigned = sorted(
            unassigned, 
            key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var)))
        )

        return sorted_unassigned.pop(0)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Assignment complete
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                prev_domain = deepcopy(self.domains)
                self.domains[var] = {value}
                inference = self.inference(var, assignment)
                if inference is not None:
                    assignment.update(inference)
                    result = self.backtrack(assignment)
                    if not result == None:
                        return result
                    else:
                        # Delete all the inferences added to assignment
                        for inference_var in inference.keys():
                            del assignment[inference_var]
            # Assignment of value is wrong for var, delete assignemnt
            del assignment[var]
                
        # Current var has no value in its domain that works
        return None

    def inference(self, var, assignment):
        """
        Implements ac3 algorithm on given assignment of var to maintain arc consistency

        Return a dict of assignments that can be inferred from given assigments;
        return None if given assignment leads to no farther future progress
        """
        self.ac3([(other, var) for other in self.crossword.neighbors(var)])

        # For variables that aren't yet assigned check if new inferences can be made
        # aka a variable has only one value left in domain (add) or none left (abort)
        new_inferences = dict()
        for var in set(self.domains.keys()) - set(assignment.keys()):
            if len(self.domains[var]) == 0:
                return None
            if len(self.domains[var]) == 1:
                new_inferences[var] = list(self.domains[var])[0]
        return new_inferences


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
