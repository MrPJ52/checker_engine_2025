from game import Game
from heuristic_score import ScoreFunction
from copy import deepcopy

class BoardNod:
    def __init__(self, board:list, turn_player:str):
        self.board_present = board
        self.turn_player = turn_player
        self.score = ScoreFunction.score_board(self.board_present, self.turn_player)
        
        # How children is saved: Dictionary.
        # Dict[tuple(move/attack method, startPos, endPos)] = Node.
        self.children_dict = dict()
    
    def get_children(self):
        game = Game()
        game.import_board(self.board_present, self.turn_player)
        # Console out for debugging.
        # game.print_board()

        if (game.get_atk_dict()) :
            move_dict = game.get_atk_dict()
            for atkPos in move_dict.keys():
                for targetPos in move_dict[atkPos]:
                    game_new = deepcopy(game)
                    game_new.sleep_time = 0

                    game_new.set_board()
                    game_new.attack(atkPos, targetPos)
                    game_new.turn_player = 'W' if (game_new.turn_player == 'B') else 'B'

                    # Create key: (method, startPosition, endPosition)
                    action = tuple([Game.attack, atkPos, targetPos])
                    self.children_dict[action] = BoardNod(game_new.board, game_new.turn_player)

            return

        move_dict = game.get_move_dict()
        for startPos in move_dict.keys():
            for destinedPos in move_dict[startPos]:
                game_new = deepcopy(game)
                game_new.sleep_time = 0

                game_new.move(startPos, destinedPos)
                game_new.set_board()
                game_new.turn_player = 'W' if (game_new.turn_player == 'B') else 'B'

                # Create Key
                action = tuple([Game.move, startPos, destinedPos])
                self.children_dict[action] = BoardNod(game_new.board, game_new.turn_player)
        
        return


class BoardTree:
    def __init__(self, root_nod:BoardNod):
        self.root = root_nod
    
    def expand_tree(self, node = None, depth:int = 0, targetDepth:int = 0):
        if (node == None):
            node = self.root
        
        if (depth > targetDepth):
            return
        
        node.get_children()
        for key in node.children_dict.keys():
            # Console out for debugging.
            print("--" * depth + f"{node.children_dict[key].turn_player}, {key[0].__name__}, {key[1:]}: {node.children_dict[key].score:.4f}")

            # expand from each child
            self.expand_tree(node.children_dict[key], depth=depth+1, targetDepth=targetDepth)
        
        return
    
    # TODO: Make function to choose min/max score nod among a nod's children.
    # May need DFS.
    def find_best(self):
        pass


# Debugging.
if (__name__ == "__main__"):
    myGame = Game()
    myRoot = BoardNod(myGame.board, myGame.turn_player)

    myTree = BoardTree(myRoot)

    myTree.expand_tree(targetDepth=3)
