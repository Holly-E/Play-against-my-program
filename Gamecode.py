# -*- coding: utf-8 -*-
"""
Tic-Tac-Toe 

@author: Erickson, Holly

Press Play arrow in upper left corner to start.
To make a move, click in selected box.

To modify game play:
Board size - line 27
Who has first move - line 28(0 = player, 1 = computer)

http://www.codeskulptor.org/#user47_WeXWaMCeAb_28.py
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

player_dict = {
    0: provided.PLAYERO,
    1: provided.PLAYERX
    }


size = 4
player = player_dict[0]

# Constants for Monte Carlo simulator
NTRIALS = 500      # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player

def create_scores(board):
    """
    Helper function to initialize grid of scores (a list of lists) 
    with the same dimensions as the Tic-Tac-Toe board
    """
    dim = board.get_dim()
    score_grid = [[0 for dummy_col in range(dim)] for dummy_row in range(dim)]
    return score_grid

def mc_trial(board, player):
    """
    This function plays a game starting with the given player 
    by making random moves, alternating between players. 
    It returns when the game is over. 
    """
    while board.check_win() == None:   
        next_move = random.choice(board.get_empty_squares())
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
    return

def mc_update_scores(scores, board, player):
    """ 
    The function scores the completed board 
    and update the scores grid. 
    As the function updates the scores grid directly, 
    it does not return anything
    """
    score_math = {
        True: [SCORE_CURRENT, -SCORE_OTHER],
        False:[-SCORE_CURRENT, SCORE_OTHER]
        }
    if board.check_win() == 4:
        return
    else:
        winner = board.check_win() == player
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += score_math[winner][0]
                elif board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] += score_math[winner][1]

def get_best_move(board, scores):
    """
    This function finds all of the empty squares with the maximum score
    and randomly return one of them as a tuple.
    """
    best_move = { "score":[], "square":[] }
  
    for option in board.get_empty_squares():
        option_score = scores[option[0]][option[1]]
        if (best_move["score"] == []) or (best_move["score"] < option_score):
            best_move["score"] = option_score
            best_move["square"] = [(option[0], option[1])]
        elif best_move["score"] == option_score:
            best_move["square"].append((option[0], option[1]))
    if len(best_move["square"]) == 1:
        return best_move["square"][0]
    else: 
        return random.choice(best_move["square"]) 
        

def mc_move(board, player, trials):
    """
    This function uses the Monte Carlo simulation 
    to return a move for the machine player in the form of a tuple.
    """
    scores = create_scores(board)
    
    for dummy in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
    return get_best_move(board, scores)   

      
poc_ttt_gui.run_gui(size, player, mc_move, NTRIALS, False)
