from Game import Game
from PlayerAI import PlayerAI

class ScoreFunction:
    def __init__(self):
        self.game_cnt = 0
        self.game_score_list = list()
    
    def run_game(self):
        newGame = Game()
        P1 = PlayerAI('B')
        P2 = PlayerAI('W')

        while (not newGame.game_is_over):
            P1.playTurn(game=newGame)
            if newGame.game_is_over:
                return newGame.board
            P2.playTurn(game=newGame)
            if newGame.game_is_over:
                return newGame.board
        
        return

    def score_board(self, stdSide, target_board:list):
        w_center = 0.3
        w_advanced = 1.5
        w_left_moves = 0.2
        # In case of weight of number of check or King,
        # the notation in board(1 or 2) is weight by itself.

        score_sum = 0

        for i in range(len(target_board)):
            tile = target_board[i]
            # Transit from index to coordination
            y = int((i+1)/4)
            x = (i+1)%4 - (y%2)
            # Judge center
            if (2 <= x) and (x <= 5) and (2 <= y) and (y <= 5):
                tile *= w_center
            # Judge advanced
            if (((y >= 6) and (stdSide == "B")) or ((y <= 1) and (stdSide == "W"))):
                tile *= w_advanced
            
            score_sum += tile
        
        return score_sum

# Debugging.
testInst = ScoreFunction()
board = testInst.run_game()
print(board)