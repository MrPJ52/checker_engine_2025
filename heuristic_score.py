from game import Game
from player_bot import PlayerBot
from time import sleep

class ScoreFunction:
    def __init__(self):
        self.game_cnt = 0
        self.game_score_list = list()
    
    def run_game(self):
        newGame = Game()
        newGame.sleep_time = 0.05
        P1 = PlayerBot('B')
        P2 = PlayerBot('W')

        turn_cnt = 0

        while (not newGame.game_is_over):
            P1.playTurn(game=newGame)
            if newGame.game_is_over:
                winner = 'W'
                break
            newGame.print_board()
            turn_cnt += 1

            P2.playTurn(game=newGame)
            if newGame.game_is_over:
                winner = 'B'
                break
            newGame.print_board()

            turn_cnt += 1
        
        print(f"Took {turn_cnt} turns, and winner is {winner}.")
        self.game_cnt += 1

        sleep(3)

        return newGame.board

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
while(testInst.game_cnt < 5):
    board = testInst.run_game()
    print(board)