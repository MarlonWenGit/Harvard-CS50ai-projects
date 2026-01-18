"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None
    x_count = 0
    o_count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            cell = board[i][j]
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    if x_count-o_count == 1:
        return O
    elif x_count-o_count == 0:
        return X
    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            cell = board[i][j]
            if cell == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board2 = copy.deepcopy(board)
    i, j = action
    turn = player(board)

    if board[i][j] != EMPTY:
        raise Exception
    if i > 2 or j > 2:
        raise Exception
    if i < 0 or j < 0:
        raise Exception
    
    board2[i][j] = turn
    return board2


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == board[(i+1) % 3][j] == board[(i+2) % 3][j] and board[i][j] in [X, O]:
                return board[i][j]
            elif board[i][j] == board[i][(j+1) % 3] == board[i][(j+2) % 3] and board[i][j] in [X, O]:
                return board[i][j]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] in [X, O]:
        return board[0][2]
    elif board[0][0] == board[1][1] == board[2][2] and board[0][0] in [X, O]:
        return board[0][0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    board_full = True
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                board_full = False
    if win in [X, O] or board_full == True:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winners = winner(board)
    if winners == X:
        return 1
    elif winners == O:
        return -1
    else:
        return 0


def find_best_score(board, alpha = -float('inf'), beta = float('inf')):
    
    if terminal(board):
        return utility(board)
    
    turn = player(board)
    possible_actions = actions(board)
    
    if turn == X:
        best_score = -float('inf')
        for action in possible_actions:
            score = find_best_score(result(board, action), alpha, beta)
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    
    else:
        best_score = float('inf')
        for action in possible_actions:
            score = find_best_score(result(board, action), alpha, beta)
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return None
    
    possible_actions = actions(board)
    best_score = find_best_score(board)

    for action in possible_actions:
        score = find_best_score(result(board, action))
        if score == best_score:
            optimal_action = action
            return optimal_action