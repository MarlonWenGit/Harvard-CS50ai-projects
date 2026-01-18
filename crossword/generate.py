import sys

from crossword import *

import copy

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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        variables = copy.deepcopy(self.domains)
        for variable in variables:
            for word in variables[variable]:
                if variable.length != len(word):
                    self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlaps = self.crossword.overlaps
        i, j = overlaps[x, y]
        revision = False
        domains = copy.deepcopy(self.domains[x])
        domains2 = copy.deepcopy(self.domains[y])
        for word in domains:
            possible_value = False
            for word2 in domains2:
                if word[i] == word2[j]:
                    possible_value = True
            if possible_value == False:
                self.domains[x].remove(word)
                revision = True
        return revision


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = list()
            for variable in self.domains:
                for variable2 in self.domains:
                    if variable != variable2 and variable2 in self.crossword.neighbors(variable):
                        queue.append((variable, variable2))
        else:
            queue = copy.deepcopy(arcs)
                    
        while queue != list():
            (x, y) = queue[0]
            queue.remove((x, y))
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True
    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        complete = True
        for variable in assignment:
            if len(assignment[variable]) == 0:
                complete = False
        for variable2 in self.crossword.variables:
            if variable2 not in assignment:
                complete = False
        return complete
    

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        consistent = True
        words = []
        for variable in assignment:
            word = assignment[variable]
            if word in words:
                consistent = False
            words.append(word)
            if len(word) != variable.length:
                consistent = False
            for variable2 in assignment:
                if variable2 in self.crossword.neighbors(variable):
                    i, j = self.crossword.overlaps[variable, variable2]
                    if assignment[variable][i] != assignment[variable2][j]:
                        consistent = False
        
        return consistent
    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        least_constraining_values = list()
        dictionary = dict()
        
        for word in self.domains[var]:
            count = 0
            for neighbour in self.crossword.neighbors(var):
                if neighbour not in assignment:
                    for word2 in self.domains[neighbour]:
                        i, j = self.crossword.overlaps[var, neighbour]
                        if word == word2:
                            count += 1
                        elif assignment[var][i] != assignment[neighbour][j]:
                            count += 1
            dictionary[word] = count
        sorted_dictionary = sorted(dictionary.items(), key = lambda x : x[1])
        for pair in sorted_dictionary:
            least_constraining_values.append(pair[0])
        return least_constraining_values
    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        current = 99999
        current_v = None

        for variable in self.domains:
            if variable not in assignment:
                remaining_values = len(self.domains[variable])
                if remaining_values < current:
                    current = min(current, remaining_values)
                    current_v = variable
                elif remaining_values == current:
                    if len(self.crossword.neighbors(current_v)) < len(self.crossword.neighbors(variable)):
                        current_v = variable
        return current_v
    

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]
        return False


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
