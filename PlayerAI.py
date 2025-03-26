from random import choice
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
            self.makeAttack(attackable_dict=attackable_dict, game=game)
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
            else:
            # If there is movable checks, move
                self.makeMove(movable_dict, game)
        
        # Change turn player
        game.turn_player = 'W' if game.turn_player == 'B' else 'B'

        return

    #%% makeMove() method.
    # Make AI randomly move in Game instance.
    def makeMove(self, movable_dict:dict, game:Game):
        # Randomly pick a mover and its able move
        moverPos = choice(tuple(movable_dict.keys()))
        destinedPos = choice(movable_dict[moverPos])

        # Calls game.move() method with key and destination
        game.move(startPos=moverPos, destinedPos=destinedPos)
        
        return

    #%% makeAttack() method.
    # Make AI actually attack.
    def makeAttack(self, attackable_dict:dict, game:Game):
        # Randomly pick a attacker and its target
        atkPos = choice(tuple(attackable_dict.keys()))
        targetPos = str(choice(attackable_dict[atkPos]))

        print(f"{atkPos} attacks {targetPos} .")

        # Calls game.attack() method with attacker and target
        game.attack(atkPos=atkPos, targetPos=targetPos)

        return