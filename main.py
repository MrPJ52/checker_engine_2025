import Game
from time import sleep

GameController = Game.Game()

while True:
    GameController.print_board()

    # Find if there is any attacking checks
    # If there is, attack
    if GameController.get_atk_list():
        GameController.attack()
        print(GameController.get_atk_list())
        
    # If there is not,
    # Find if there is any movable checks
    else:

    # If there is no movable checks,
    # Turn player is defeated, end game

    # If there is movable checks, move
        GameController.move()

    # Change turn player
    GameController.turn_player = 'W' if GameController.turn_player == 'B' else 'B'
    sleep(1)

    # try:
    #     del GameController.checks_list[order]
    # except:
    #     print("Out of range.\n")