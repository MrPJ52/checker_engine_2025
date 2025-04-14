from game import Game
from player_bot import PlayerBot
from time import sleep

# As a first step of AI Engine,
# I chose to use simple heuristics function and MiniMax algorithm using it.
# After making board tree and searching method,
# I'll make Q-Learning method: Q(s, a)
# that means Sum of expected reward(Q) when action is taken(a) in a given situation(s).
# In MiniMax algorithm, s is board, a is set of weights.
# And after that, I will use deep learning to predict value of Q(s, a)
# and update weights set.

#%% ScoreFunction class.
class ScoreFunction:
    def __init__(self):
        self.game_cnt = 0
        self.game_score_list = list()
        self.boards_list = list()
        # Weights
        # In case of weight of number of check or King,
        # the notation in Game.board(1 or 2) is weight by itself.
        self.weight_list = [1.6, 1.2, 1.2]
        # For now, each weights means center, advanced, and left moves.
    
    # TODO: Running function have to be separated from ScoreFunction.
    def run_game(self):
        newGame = Game()
        # Set sleep time of Game shorter.
        newGame.sleep_time = 0
        P1 = PlayerBot('B')
        P2 = PlayerBot('W')

        turn_cnt = 0
        # Set max turn count.
        turn_cnt_max = 50
        # Play until one game ends or hit specific turn count.
        while (True):
            P1.playTurn(game=newGame)
            if newGame.game_is_over or turn_cnt >= turn_cnt_max:
                break
            newGame.print_board()
            turn_cnt += 1

            P2.playTurn(game=newGame)
            if newGame.game_is_over or turn_cnt >= turn_cnt_max:
                break
            newGame.print_board()
            turn_cnt += 1

        self.game_cnt += 1
        print(f"Took {turn_cnt} turns.")
        sleep(1)

        self.boards_list.append(newGame.board)
        return newGame.board

    def score_board(self, target_board:list):
        score_sum = 0

        # To find if there are only one side pieces,
        # Check if every pieces are in the same side with very first piece.
        first_tile = target_board[0]
        winner = first_tile
        for i in range(len(target_board)):
            # Find first tile that is NOT 0 (which means there is a piece)
            if first_tile == 0:
                first_tile = target_board[i]
                winner = first_tile
                continue
            else:
                pass

            # Check each tile and whether it is empty or there is enemy.
            # If there is enemy in tile, winner = 0, then break.
            if target_board[i] == 0:
                continue
            elif first_tile*target_board[i] < 0:
                winner = 0
                break
        # If there is winner, return massively big score.
        if (winner != 0):
            return 10000 if (winner > 0) else -10000


        for i in range(len(target_board)):
            tile = target_board[i]

            # Convert 1D index to 2D coordination
            y = i//4
            x = ((i%4)*2 + 1) - (y%2)

            # Judge center
            if (2 <= x) and (x <= 5) and (2 <= y) and (y <= 5):
                tile *= self.weight_list[0]
            # Judge advanced: only for men, not for king.
            if (((y >= 6) and (tile == -1)) or ((y <= 1) and (tile == 1))):
                tile *= self.weight_list[1]
            # Judge left moves
            # TODO: Connect with Game.find_moves() to get weight of left moves.
            

            score_sum += tile
        
        return score_sum

# Debugging.
testInst = ScoreFunction()

# Create games and score them.
while(testInst.game_cnt < 10):
    board = testInst.run_game()
    print(board)

print("---------------------------------")
print("---------------------------------")

for board in testInst.boards_list:
    print(board)
    game_sample = Game()
    game_sample.import_board(board, 'W')
    game_sample.print_board()
    print("Score of this board is " + str(testInst.score_board(board)) + ".\n")


# Testing board scoring.
# board = [-1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# print(board)
# print(testInst.score_board(board))