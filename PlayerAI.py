from Game import Game

#%% PlayerAI
class PlayerAI:
    # constructor
    def __init__(self, Side):
        self.side = Side

    #%% playTurn() method.
    # Make AI actually play a turn, including attacking and moving.
    # Parameter: Game() instance
    def playTurn(self, game:Game):
        print("AI player is playing...")
        # Find if there is any attacking checks
        # If there is, attack
        attackable_dict = game.get_atk_dict()
        if attackable_dict:
            # TODO: Need to be changed into makeAttack()
            game.attack_phase(attackable_dict, self, False)
        # If there is not,
        # Find if there is any movable checks
        else:
            movable_dict = game.get_move_dict()
            # If there is no movable checks,
            # Turn player is defeated, end game
            if not movable_dict:
                game.game_over()
                print("\nShut down Checker Engine.\n")
                return
            # If there is movable checks, move
            # TODO: Need to be changed into makeMove()
            game.move_phase(movable_dict)
        
        # Change turn player
        game.turn_player = 'W' if game.turn_player == 'B' else 'B'

        return

    #%% makeMove() method.
    # Make AI actually move.
    def makeMove(self):
        pass

    #%% makeAttack() method.
    # Make AI actually attack.
    def makeAttack(self):
        pass