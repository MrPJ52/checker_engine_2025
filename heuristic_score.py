from Game import Game

class ScoreFunction:
    def __init__(self):
        self.game_cnt = 0
        self.game_score_list = list()
    
    def run_game(self):
        newGame = Game()
        game_board = newGame.play_game()
        