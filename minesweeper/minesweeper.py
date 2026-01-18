import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if len(self.cells) == self.count:
            for cell in self.cells:
                mines.add(cell)
        return mines


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()
        if self.count == 0:
            for cell in self.cells:
                safes.add(cell)
        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell) #Mark cell as a move
        
        self.mark_safe(cell) #Mark cell as safe
        
        a, b = cell
        neighbouring_cells = list()
        directions = [(1, 1), (1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (-1, -1), (-1, 0)]
        for i, j in directions:
            if 0 <= a + i < 8 and 0 <= b + j < 8:
                neighbouring_cells.append((a + i, b + j)) #Finds neighbouring cells

        cells_to_remove = set()
        for cell1 in neighbouring_cells:
            if cell1 in self.mines:
                cells_to_remove.add(cell1)
                count -= 1  # Adjust count for known mines
            elif cell1 in self.safes or cell1 in self.moves_made:
                cells_to_remove.add(cell1)

        # Now remove cells outside the loop
        neighbouring_cells = [cell for cell in neighbouring_cells if cell not in cells_to_remove]

        new_sentence = Sentence(set(neighbouring_cells), count)
        self.knowledge.append(new_sentence) #Adds new sentence to knowledge base

        self.update2()
        self.infer()
        self.knowledge = [s for s in self.knowledge if s.cells]
        
    def update2(self):
        '''
        Update self.mines and self.safes
        '''
        for sentence in self.knowledge:
            self.mines.update(sentence.known_mines())
            self.safes.update(sentence.known_safes()) #Updates self.mines and self.safes
    ''' 
    def infer(self):
        
        Add any new sentences that can be inferred
        
        keep_going = False
        for sentence in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence != sentence2:
                    if (sentence.cells).issubset(sentence2.cells):
                        self.knowledge.append(Sentence(sentence2.cells - sentence.cells, sentence2.count - sentence.count))
                        if Sentence(sentence.cells, sentence.count) in self.knowledge:
                            self.knowledge.remove(Sentence(sentence2.cells, sentence2.count))
                        keep_going = True
                    if (sentence2.cells).issubset(sentence.cells):
                        self.knowledge.append(Sentence(sentence.cells - sentence2.cells, sentence.count - sentence2.count)) 
                        if Sentence(sentence.cells, sentence.count) in self.knowledge:
                            self.knowledge.remove(Sentence(sentence.cells, sentence.count))
                        keep_going = True
        if keep_going == True:
            self.infer()
    '''
    def infer(self):
        """
        Add any new sentences that can be inferred.
        Uses a loop to ensure that new sentences are added until no more can be inferred.
        """
        
        new_inferences = True
        
        while new_inferences:
            new_inferences = False
            new_sentences = []

            # Go through all pairs of sentences
            for sentence in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence != sentence2:
                        # Check if sentence is a subset of sentence2
                        if sentence.cells.issubset(sentence2.cells):
                            inferred_cells = sentence2.cells - sentence.cells
                            inferred_count = sentence2.count - sentence.count
                            inferred_sentence = Sentence(inferred_cells, inferred_count)
                            
                            if inferred_sentence not in self.knowledge and inferred_sentence not in new_sentences:
                                new_sentences.append(inferred_sentence)
                                new_inferences = True
                                
                        # Check if sentence2 is a subset of sentence
                        elif sentence2.cells.issubset(sentence.cells):
                            inferred_cells = sentence.cells - sentence2.cells
                            inferred_count = sentence.count - sentence2.count
                            inferred_sentence = Sentence(inferred_cells, inferred_count)
                            
                            if inferred_sentence not in self.knowledge and inferred_sentence not in new_sentences:
                                new_sentences.append(inferred_sentence)
                                new_inferences = True

            # Add new sentences to knowledge
            self.knowledge.extend(new_sentences)

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

            # Update known mines and safes
            self.update2()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        legal_moves = set() 
        directions = [(1, 1), (1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (-1, -1), (-1, 0)]

        for cell in self.moves_made:
            a, b = cell
            neighbouring_cells = list()
            for i, j in directions:
                if 0 <= a + i < 8 and 0 <= b + j < 8:
                    neighbouring_cells.append((a + i, b + j))
            for cell1 in neighbouring_cells:
                if cell1 in self.moves_made:
                    neighbouring_cells.remove(cell1)
            legal_moves.update(set(neighbouring_cells))
        
        for move in legal_moves:
            if (move in self.safes) and (move not in self.moves_made):
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        legal_moves = set() 
        directions = [(1, 1), (1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (-1, -1), (-1, 0)]

        for cell in self.moves_made:
            a, b = cell
            neighbouring_cells = list()
            for i, j in directions:
                if 0 <= a + i < 8 and 0 <= b + j < 8:
                    neighbouring_cells.append((a + i, b + j))
            for cell1 in neighbouring_cells:
                if cell1 in self.moves_made:
                    neighbouring_cells.remove(cell1)
            legal_moves.update(set(neighbouring_cells))
        
        for move in legal_moves:
            if move not in self.mines:
                return move
        return None