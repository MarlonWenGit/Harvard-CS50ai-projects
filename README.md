# About

A collection of projects I completed as part of Harvard’s CS50 Introduction to Artificial Intelligence with Python. The projects cover core AI ideas like search, probability, optimisation, and basic machine learning, all implemented in Python to better understand how these techniques work in practice.

## Image-recognition-AI
Recognises types of road-signs and classifies them into one of 43 categories using a complex convolutional neural network.

## Masked-Language-Model
Predicts a 'masked' word in a sentence using the attention model.

## Tic-Tac-Toe-
Tic Tac Toe game (pygame) where you play against a perfect AI using the Minimax algorithm with alpha-beta pruning.

How to run:

Install pygame https://www.pygame.org/wiki/GettingStarted.
Download and unzip files
Run runner.py

## Minesweeper
Minesweeper game (pygame) with a perfect AI that will always play the best move using propositional logic.

How to run:

Install pygame https://www.pygame.org/wiki/GettingStarted.
Download and unzip files
Run runner.py

## Knights-and-Knaves-puzzle
Showcase of how propositional logic might be used to solve various problems such as the famous knights and knaves puzzle. Run puzzle.py file to find the solutions to the puzzles shown below:

Puzzle 0 A says "I am both a knight and a knave."

Puzzle 1 A says "We are both knaves." B says nothing.

Puzzle 2 A says "We are the same kind." B says "We are of different kinds."

Puzzle 3 A says either "I am a knight." or "I am a knave.", but you don't know which. B says "A said 'I am a knave'." B says "C is a knave." C says "A is a knight."

## Nim-game
In the game Nim, there are some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from any one non-empty pile. Whoever removes the last object loses.

Uses the Q-learning algorithm to train an AI that plays the optimal move.

DOWNLOAD INSTRUCTIONS:

Download the zip file
Extract the zip file
Install python if not already installed on your machine
Run the play.py program

## Degrees

This program finds the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

The data folder contains a large amount of random data consisting of various movies(movie_id, title, year of release), people(person_id, name, birth) and stars(person_id, movie_id). However, the data does not include every single movie or actor that has ever existed, so if you wish to add to the data, you may choose to do so.

To run the program, download all of the files, make sure the directory is correct (using the cd or change directory command), open the degrees.py file and run it on python.

To use the program, when prompted, type the name of 2 actors (list of actors can be found in the data folder).
