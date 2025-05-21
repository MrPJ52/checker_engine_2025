from game import Game
from heuristic_score import ScoreFunction

class BoardNod:
    def __init__(self, board:list):
        self.board_present = board
        self.score = ScoreFunction.score_board(self.board_present)

        # action list's length = children number
        self.action_list = list()

class BoardTree:
    def __init__(self, first_board:list):
        self.scorer = ScoreFunction()
        self.nod_list = list()
        self.nod_list.append(BoardNod(first_board))
    
    # TODO: Make function to choose min/max score nod among a nod's children.