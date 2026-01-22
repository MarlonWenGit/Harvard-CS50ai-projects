# About

A collection of projects completed as part of **Harvard’s CS50: Introduction to Artificial Intelligence with Python**.

These projects cover core AI ideas such as:
- Search
- Probability
- Optimisation
- Propositional logic
- Basic machine learning

All projects are implemented in **Python** to better understand how these techniques work in practice.

---

## Image Recognition AI

Recognises types of road signs and classifies them into one of **43 categories** using a convolutional neural network (CNN).

---

## Masked Language Model

Predicts a *masked* word in a sentence using an **attention-based model**.

---

## Tic Tac Toe

A Tic Tac Toe game built with **Pygame**, where you play against a **perfect AI** using the **Minimax algorithm with alpha–beta pruning**.

### How to run
1. Install Pygame: https://www.pygame.org/wiki/GettingStarted  
2. Download and unzip the files  
3. Run `runner.py`

---

## Minesweeper

A Minesweeper game built with **Pygame**, featuring a perfect AI that always plays the optimal move using **propositional logic**.

### How to run
1. Install Pygame: https://www.pygame.org/wiki/GettingStarted  
2. Download and unzip the files  
3. Run `runner.py`

---

## Knights and Knaves Puzzle

A showcase of how **propositional logic** can be used to solve classic logic puzzles, such as the Knights and Knaves problem.

Run `puzzle.py` to find the solutions to the puzzles below:

- **Puzzle 0**  
  A says: *"I am both a knight and a knave."*

- **Puzzle 1**  
  A says: *"We are both knaves."*  
  B says nothing.

- **Puzzle 2**  
  A says: *"We are the same kind."*  
  B says: *"We are of different kinds."*

- **Puzzle 3**  
  A says either *"I am a knight"* or *"I am a knave"* (you do not know which).  
  B says: *"A said 'I am a knave'."*  
  B also says: *"C is a knave."*  
  C says: *"A is a knight."*

---

## Nim Game

In the game **Nim**, there are several piles, each containing some number of objects. Players take turns removing any number of objects from a single non-empty pile.  
**Whoever removes the last object loses.**

This project uses **Q-learning** to train an AI that learns and plays the optimal strategy.

### How to run
1. Download the ZIP file  
2. Extract the ZIP file  
3. Install Python (if not already installed)  
4. Run `play.py`

---

## Degrees

This program finds the **shortest path between two actors** by choosing a sequence of movies that connects them.

For example, the shortest path between **Jennifer Lawrence** and **Tom Hanks** is 2:
- Jennifer Lawrence starred with Kevin Bacon in *X-Men: First Class*
- Kevin Bacon starred with Tom Hanks in *Apollo 13*

### Data
The `data` folder contains information about:
- Movies (`movie_id`, title, year)
- People (`person_id`, name, birth)
- Stars (`person_id`, `movie_id`)

The dataset is not exhaustive, but you may extend it if desired.

### How to run
1. Download all files  
2. Ensure you are in the correct directory (using `cd`)  
3. Run `degrees.py` with Python  

### How to use
- When prompted, type the names of **two actors**
- A list of available actors can be found in the `data` folder
