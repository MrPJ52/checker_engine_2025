from Game import Game
from heuristic_score import ScoreFunction

class BoardNod:
    def __init__(self, board:list):
        self.board_present = board
        # action list's length = children number
        self.action_list = list()
    
    # TODO: Make function to score this board.

class BoardTree:
    def __init__(self, first_board:list):
        self.scorer = ScoreFunction()
        self.nod_list = list()
        nod_list.append(BoardNod(first_board))
    
    # TODO: Make function to choose min/max score nod among a nod's children.