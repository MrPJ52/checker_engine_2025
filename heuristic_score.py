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
# and update NN's weights.

#%% ScoreFunction class.
class ScoreFunction:
    # Weights: set as static variance of ScoreFuction
    # In case of weight of number of check or King,
    # the notation in Game.board(1 or 2) is weight by itself.
    weight_list = [1.61, 1.41, 1.21, 1.19]
    # For now, each weights means center(center and around), advanced, and left moves.

    # Constructor
    def __init__(self):
        self.game_cnt = 0
        self.game_score_list = list()
        self.boards_list = list()
        
    # run_game() method.
    # Generate a whole game run by both side playerBot.
    # Parameter: Max turn count.
    # Return: generated Game object
    def run_game(self, turn_cnt_max:int):
        newGame = Game()
        # Set sleep time of Game shorter.
        newGame.sleep_time = 0
        P1 = PlayerBot('B')
        P2 = PlayerBot('W')

        turn_cnt = 0

        # Play until one game ends or hit specific turn count.
        while (turn_cnt < turn_cnt_max):
            if (turn_cnt % 2 - 1):
                P1.playTurn(game=newGame)
                if newGame.game_is_over:
                    break
                newGame.print_board()
                turn_cnt += 1
            else:
                P2.playTurn(game=newGame)
                if newGame.game_is_over:
                    break
                newGame.print_board()
                turn_cnt += 1

        self.game_cnt += 1
        print(f"Took {turn_cnt} turns.")
        sleep(1)

        self.boards_list.append(newGame.board)
        return newGame

    # score_board() static method.
    # Gets board in form of 1D array and score it.
    # Parameter: board in form of 1D array
    # Return: score of the board
    @staticmethod
    def score_board(target_board:list, turn_player:str):
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

            if (tile == 0):
                continue

            # Convert 1D index to 2D coordination
            y = i//4
            x = ((i%4)*2 + 1) - (y%2)
            coord = (x, y)

            # Judge center
            if (2 <= x) and (x <= 5) and (2 <= y) and (y <= 5):
                tile *= ScoreFunction.weight_list[0]
            elif (1 <= x) and (x <= 6) and (1 <= y) and (y <= 6):
                tile *= ScoreFunction.weight_list[0]
            # Judge advanced: only for men, not for king.
            if (((y >= 6) and (tile == -1)) or ((y <= 1) and (tile == 1))):
                tile *= ScoreFunction.weight_list[1]
            # Judge left moves
            # TODO: Connect with Game.find_moves() to get weight of left moves.      
            game = Game()
            game.import_board(target_board, turn_player)
            if (coord in game.checks_list.keys()):
                score_sum += len(game.find_moves(game.checks_list[coord])) * ScoreFunction.weight_list[3] * tile / abs(tile)

            score_sum += tile
        
        return score_sum

#%% Debugging.
if (__name__ == "__main__"):
    testInst = ScoreFunction()

    # Create games and score them.
    while(testInst.game_cnt < 1):
        board = testInst.run_game(19).board
        print(board)

    print("---------------------------------")
    print("---------------------------------")

    for board in testInst.boards_list:
        print(board)
        game_sample = Game()
        game_sample.import_board(board, 'W')
        game_sample.print_board()
        print("Score of this board is " + str(ScoreFunction.score_board(board, game_sample.turn_player)) + ".\n")


# Testing board scoring.
# board = [-1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# print(board)
# print(testInst.score_board(board))