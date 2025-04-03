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
            newGame.print_board()

            P2.playTurn(game=newGame)
            if newGame.game_is_over:
                return newGame.board
            newGame.print_board()
        
        return

    def score_board(self, stdSide, target_board:list):
        w_center = 1.3
        w_advanced = 1.5
        w_left_moves = 1.2
        # In case of weight of number of check or King,
        # the notation in Game.board(1 or 2) is weight by itself.

        score_sum = 0

        for i in range(len(target_board)):
            tile = target_board[i]
            # Convert index to coordination
            y = int((i+1)/4)
            x = (i+1)%4 - (y%2)

            # Judge center
            if (2 <= x) and (x <= 5) and (2 <= y) and (y <= 5):
                tile *= w_center
            # Judge advanced
            if (((y >= 6) and (stdSide == "B")) or ((y <= 1) and (stdSide == "W"))):
                tile *= w_advanced
            # Judge left moves
            # TODO: Connect with Game.find_moves() to get weight of left moves.
            

            score_sum += tile
        
        return score_sum

# Debugging.
testInst = ScoreFunction()
board = testInst.run_game()
print(board)