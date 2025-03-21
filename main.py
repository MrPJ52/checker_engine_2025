import Game
from time import sleep

GameController = Game.Game()

while True:
    # Print board and turn player
    GameController.print_board()

    # Find if there is any attacking checks
    # If there is, attack
    attackable_dict = GameController.get_atk_dict()
    if attackable_dict:
        GameController.attack(attackable_dict)
        
    # If there is not,
    # Find if there is any movable checks
    else:
        # If there is no movable checks,
        # Turn player is defeated, end game
        movable_dict = GameController.get_move_dict()
        if not(movable_dict):
            GameController.game_over()
            break

        # If there is movable checks, move
        GameController.move(movable_dict)

    # Change turn player
    GameController.turn_player = 'W' if GameController.turn_player == 'B' else 'B'
    sleep(0.5)