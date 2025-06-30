from game import Game
from heuristic_score import ScoreFunction
from player_bot import PlayerBot
from board_tree import BoardNod, BoardTree

class PlayerBotMinimax(PlayerBot):
    def __init__(self, Side, depth):
        PlayerBot.__init__(self, Side)
        self.depth = depth
    
    # Override playTurn() method.
    def playTurn(self, game:Game):
        # Find best move using BoardTree.find_best()
        current_board_tree = BoardTree(BoardNod(game.board, game.turn_player))
        current_board_tree.expand_tree(targetDepth=self.depth)

        next_move = current_board_tree.find_best()
        next_move[0][0](game, next_move[0][1], next_move[0][2])

        game.turn_player = 'W' if game.turn_player == 'B' else 'B'

        return

if (__name__ == "__main__"):
    game = Game()
    Wp = PlayerBotMinimax('W', 3)
    Bp = PlayerBotMinimax('B', 2)

    max_turn_cnt = 30
    turn_cnt = 0
    while(not game.game_is_over and turn_cnt < max_turn_cnt):
        Wp.playTurn(game)
        game.print_board()
        Bp.playTurn(game)
        game.print_board()

        turn_cnt += 1
    
    print(ScoreFunction.score_board(game.board, game.turn_player))
