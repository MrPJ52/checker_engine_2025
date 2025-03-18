import Game
from time import sleep

GameController = Game.Game()

while True:
    GameController.print_board()

    # Find if there is any attacking checks
    # If there is, attack
    if GameController.get_atk_dict():
        GameController.attack()
        print(GameController.get_atk_dict())
        
    # If there is not,
    # Find if there is any movable checks
    else:
    # If there is no movable checks,
    # Turn player is defeated, end game
    # TODO: Create method to make player win or lose.

    # If there is movable checks, move
        GameController.move_debug()

    # Change turn player
    GameController.turn_player = 'W' if GameController.turn_player == 'B' else 'B'
    sleep(1)

    # try:
    #     del GameController.checks_list[order]
    # except:
    #     print("Out of range.\n")