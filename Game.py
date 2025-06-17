from checkersClass import Check, King
from time import sleep

'''
Board index notation

  0 1 2 3 4 5 6 7 x
0 . . . . . . . .
1 . . . . . . . .
2 . . . . . . . .
3 . . . . . . . .
4 . . . . . . . .
5 . . . . . . . .
6 . . . . . . . .
7 . . . . . . . .
y

'''

#%% Game class: overall game system of checker.
class Game:
    # initial setting
    def __init__(self):
        self.board = [0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0]
        self.game_is_over = False
        # To change sleep time
        self.sleep_time = 0.5
        self.turn_player = 'B'
        # checks_list = { str([x, y]) : Check instance }
        # Can act as following:
        # keys() = list of checks' position, values() = list of actual pieces
        # TODO: Change the keys into tuple: doesn't need to parce str into list.
        self.checks_list = dict()

        # Create Checks for normal games
        for x in range(0, 8, 2):
            for y in range(3):
                self.checks_list[tuple([x+(1-y%2), y])] = Check([x+(1-y%2), y], "B")
        
        for x in range(0, 8, 2):
            for y in range(3):
                self.checks_list[tuple([x+(y%2), 7-y])] = Check([x+(y%2), 7-y], "W")
        
        # Create Checks for debugging
        # self.checks_list[str([1, 0])] = Check([1, 0], "B")
        # self.checks_list[str([5, 0])] = Check([5, 0], "B")
        # self.checks_list[str([2, 7])] = Check([2, 7], "W")
        # self.checks_list[str([6, 7])] = Check([6, 7], "W")

        #Create Checks for debugging game_over()
        # self.checks_list[str([1, 0])] = Check([1, 0], "B")

        # Initially set board by set_board()
        self.set_board()
    
    # set_board() method.
    # Set the board situation as 1D list, according to self.checks_list.
    def set_board(self):
        self.board = [ 0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,0]
        for check in self.checks_list.values():
            # Set notation
            # + for White, - for Black
            numNotation = 1 if (check.side == "W") else -1
            # 1 for normal check, 2 for King
            numNotation *= (2 if ("K" in check.notation) else 1)

            x = check.pos[0]
            y = check.pos[1]
            # position as [x, y] --> [x//2 + y*4] in 1D array
            idx = x//2 + y*4
            self.board[idx] = numNotation
        
        return
    
    # import_board() method.
    # Import board in form of 1D Array.
    # Set the Game object including board according to input information.
    # Basically do the opposite to set_board().
    def import_board(self, board_in:list, turn_player_in:str):
        # Reset game infos
        self.board = board_in
        self.turn_player = turn_player_in
        self.checks_list = dict()

        # Create new Check object and fill it into self.checks_list
        for i in range(len(self.board)):
            tile = self.board[i]
            # If tile is empty, continue
            if (tile == 0):
                continue

            # Convert 1D index to 2D coordination
            y = i//4
            x = ((i%4)*2 + 1) - (y%2)

            # Reset self.checks_list with checks info
            side = 'B' if tile < 0 else 'W'
            pos = [x, y]
            if (tile == 2 or tile == -2):
                self.checks_list[tuple(pos)] = King(pos, side)
            else:
                self.checks_list[tuple(pos)] = Check(pos, side)

        return

    # print_board() method.
    # Print board through console.
    def print_board(self):
        self.set_board()
        
        print("    0   1   2   3   4   5   6   7")
        for y in range(8):
            print(f"{y} ", end="")
            for x in range(8):
                # Pass the white square
                if ((x+y) % 2 == 0):
                    print("|__|", end="")
                    continue

                if self.board[x//2 + y*4] != 0:
                    print("|{0:>2}|".format(self.board[x//2 + y*4]), end="")
                else:
                    print("|__|", end="")
            print()

        return
    
    
    # move_debug method.
    # Method to move check in any location.
    # Used to debug and test.
    def move_debug(self):
        print("Initiate debug move. If you want to skip this turn, enter SKIP.")
        try:
            pos_start = tuple(map(int, input("Position of check you want to move (input as x,y): ").split(",")))
            pos_target = tuple(map(int, input("Position of tile you want to move to (input as x,y): ").split(",")))
        except:
            return

        # Find check in start position
        if pos_start in self.checks_list.keys():
            self.checks_list[pos_start].move(pos_target)
            
            sleep(self.sleep_time)

            # Delete original_position:check and add new_position:check
            self.checks_list[pos_target] = self.checks_list.pop(pos_start)
            # Check if it is promoted
            self.check_promotion(pos_target)
            # if moved, end the method
            return
        
        print("There is no check in start position.\n")
        return

    # TODO: there was an error about attack algorithm.
    # After move_debug(), one attackable check ignored it.
    # Couldn't find the reason, but might be fixed later.
    
    # find_targets() method.
    # Find if a check has attacking target.
    # Parameter: Tuple of Position of attacker
    def find_targets(self, checkPos:tuple):
        check = self.checks_list[checkPos]
        target_list = list()
        for posible_move in check.moves:
            pos_atked = tuple([check.pos[i] + posible_move[i] for i in range(2)])
            try:
                # Check if there is an enemy check in pos_atked
                # and the position across the enemy is empty or out of bound
                if (self.checks_list[pos_atked].side != check.side) \
                and (tuple([check.pos[0] + 2*posible_move[0], check.pos[1] + 2*posible_move[1]]) not in self.checks_list.keys()) \
                and (0 <= check.pos[0] + 2*posible_move[0] <= 7) and (0 <= check.pos[1] + 2*posible_move[1] <= 7):
                    target_list.append(pos_atked)
            except:
                pass

        # Return [list of [Tuple of position of target]]
        if target_list:
            return target_list
        else:
            return None
    
    # get_atk_dict() method.
    # Find if there is any piece attacking another piece.
    def get_atk_dict(self):
        atk_check_dict = dict()
        for check in self.checks_list.values():
            if check.side == self.turn_player:
                targets = self.find_targets(tuple(check.pos))
                if targets:
                    try:
                        for target in targets:
                            atk_check_dict[tuple(check.pos)].append(target)
                    except:
                        atk_check_dict[tuple(check.pos)] = targets
        
        # Returns Dictionary as following:
        # { str(Position of attacker): [list of tuple(target position)] }
        return atk_check_dict
    
    # attack_phase() method.
    # Proceed attack phase and control it.
    # Parameter: Dictionary that is result of get_atk_dict, CheckersGUI object(In tkinter_GUI.py),
    # and boolean to check player has already attacked
    def attack_phase(self, atk_dict:dict, GUI, alreadyAtked=False):
        # get attackers list from atk_dict
        atking_list = list(atk_dict.keys())
        # if it is first attack, choose which one to attack
        if (not alreadyAtked):
            print("Attackable checks are:")
            for i in range(len(atking_list)):
                print(f"{i}: {atking_list[i]} -> {atk_dict[atking_list[i]]}")
            
            print("Choose which one to start attack_phase(Input nth): ", end="")
            atkPosNum = int(input())
            # if input is -1, call move_debug() and return
            if (atkPosNum == -1):
                self.move_debug()
                return
            atkPos = atking_list[atkPosNum]
        # if already attacked, attacker is automatically set
        else:
            atkPos = list(atk_dict.keys())[0]
        
        sleep(self.sleep_time)

        # If attacker has one and only target, choose it automatically
        if len(atk_dict[atkPos]) == 1:
            targetPos = atk_dict[atkPos][0]
        #If attacker has multiple targets, choose which one to attack
        else:
            print("This attacker has following targets: ")
            for i in range(len(atk_dict[atkPos])):
                print(f"{i}: {atk_dict[atkPos][i]}")
            print("Choose the target(Input nth): ", end = "")

            targetPosNum = int(input())
            targetPos = atk_dict[atkPos][targetPosNum]
        

        print(f"Check in position {atkPos} attacks {targetPos}.")
        sleep(self.sleep_time)

        # Call attack() method and get return value
        movePos = self.attack(atkPos=atkPos, targetPos=targetPos)

        # print board so that user can notice how that moved
        self.print_board()
        sleep(self.sleep_time)

        # check if the attacker has to be promoted
        # if promoted, end attack_phase()
        # if self.check_promotion(str(movePos)):
        #     return

        # call find_targets(position of attacker) to find if there is more target be able to attack.
        # if target found, return attack_phase({ str(attacker's position) : [list of its targets] }, True)
        # if no target was found, end attack_phase()
        more_targets = self.find_targets(movePos)
        if more_targets:
            GUI.draw_pieces()
            sleep(self.sleep_time)
            return self.attack_phase({str(movePos): more_targets}, GUI, True)
        else:
            return
    
    # attack() method.
    # Move attacker and delete target.
    # Parameter: str(attacker's pos), str(target's position)
    def attack(self, atkPos:tuple, targetPos:tuple):
        # Move attacker's position
        for possible_move in self.checks_list[atkPos].moves:
            if tuple([self.checks_list[atkPos].pos[i] + possible_move[i] for i in range(2)]) == targetPos:
                movePos = tuple([self.checks_list[atkPos].pos[i] + 2*possible_move[i] for i in range(2)])
                break

        self.checks_list[movePos] = self.checks_list.pop(atkPos)
        self.checks_list[movePos].move(movePos)
        sleep(self.sleep_time)

        # Call target.captured() method of target to print in console, and delete target
        self.checks_list.pop(targetPos).captured()
        sleep(self.sleep_time)

        ###### TODO: For now PlayerBot is using only attack() method, not attack_phase() method.
        # BUT Promotion while attack and chain attack is only implemented in attack_phase().
        # They needed to be moved in attack() method, so that Bots can do the same.

        # check if the attacker has to be promoted
        # if promoted, end attack_phase()
        if self.check_promotion(movePos):
            return movePos

        # Return movePos (position of attacker after attack)
        return movePos

    # get_move_dict() method.
    # Find if there is any movable space.
    def get_move_dict(self):
        # Find movable checks
        # dictionary as following:
        # { str(movable checks' position) : [list of movable blanks] }
        mover_check_dict = dict()
        for check in self.checks_list.values():
            # TODO: Create find_moves() method and separate codes below.
            # Return each mover's possible moves as list.
            # This is for get separated method used in scoring board.
            if check.side == self.turn_player:
                # Check all possible moves
                for posible_move in check.moves:
                    pos_move = tuple([check.pos[i] + posible_move[i] for i in range(2)])

                    # Check if pos_move is empty and not out of bound
                    if (not (pos_move in self.checks_list.keys() )) \
                    and (0 <= pos_move[0] <= 7) and (0 <= pos_move[1] <= 7):
                        try:
                            mover_check_dict[tuple(check.pos)].append(pos_move)
                        except:
                            mover_check_dict[tuple(check.pos)] = [pos_move]
        
        # Return dictionary of movable places' position
        return mover_check_dict


    # move_phase() method.
    # Proceed move phase and control it.
    # Parameter: return of get_move_dict()
    def move_phase(self, movable_dict:dict):
        #if there is no move possible, end the game
        if not(movable_dict):
            self.game_over()
            return
        
        # In the mover_check_dict, choose which one to actually move this time
        mover_list = list(movable_dict.keys())
        print("Movable checks are:")
        for i in range(len(mover_list)):
            print(f"{i}: {mover_list[i]} -> {movable_dict[mover_list[i]]}")
            
        print("Choose which one to move(Input nth): ", end="")
        moverPosNum = int(input())

        # if input is -1, call move_debug() and return
        if (moverPosNum == -1):
            self.move_debug()
            return
        
        moverPos = mover_list[moverPosNum]

        # If mover has one and only possible move, choose it automatically
        if len(movable_dict[moverPos]) == 1:
            destinedPos = movable_dict[moverPos][0]
        #If mover has multiple moves, choose which one to go
        else:
            print("This mover has following possible moves: ")
            for i in range(len(movable_dict[moverPos])):
                print(f"{i}: {movable_dict[moverPos][i]}")
            print("Choose the target(Input nth): ", end = "")

            destinedPosNum = int(input())
            destinedPos = movable_dict[moverPos][destinedPosNum]

        # Call move() method
        self.move(startPos=moverPos, destinedPos=destinedPos)
        

        # check if the mover has to be promoted
        # self.check_promotion(str(destinedPos))

        return
    
    # move() method.
    # Move check from start position to destined position.
    # Parameter: str(start position), destined position
    def move(self, startPos:tuple, destinedPos:tuple):
        self.checks_list[startPos].move(destinedPos)
        self.checks_list[destinedPos] = self.checks_list.pop(startPos)

        sleep(self.sleep_time)

        # check if the mover has to be promoted
        self.check_promotion(destinedPos)

        return
    
    # check_promotion() method.
    # Find whether the check has to promote.
    # Parameter: str(position of check)
    def check_promotion(self, checkPos:tuple):
        if (self.checks_list[checkPos].side == "B" and self.checks_list[checkPos].pos[1] == 7) \
            or (self.checks_list[checkPos].side == "W" and self.checks_list[checkPos].pos[1] == 0):
            # Promotion : Create a King in the same position and delete original Check
            self.checks_list[checkPos] = King(self.checks_list[checkPos].pos, self.checks_list[checkPos].side)
            # if promoted, return True so that other method can notice
            return True
        else:
            return False

    # game_over() method.
    # TODO: Condition to judge game over should be updated.
    def game_over(self):
        self.game_is_over = True
        print(f"There is no check left or possible moves for {self.turn_player}.\n")
        winner = "B" if (self.turn_player == "W") else "W"

        print(f"\n{winner} winned!\n")

        return

    # play_game() method.
    # Run a whole game and Returns self.board.
    def play_game(self):
        while (not self.game_is_over):
            self.print_board()

            print(f"\nIt is {self.turn_player}'s turn.\n")
            # Find if there is any attacking checks
            # If there is, attack
            attackable_dict = self.get_atk_dict()
            if attackable_dict:
                self.attack_phase(attackable_dict, self, False)
            # If there is not,
            # Find if there is any movable checks
            else:
                movable_dict = self.get_move_dict()
                # If there is no movable checks,
                # Turn player is defeated, end game
                # TODO: Update game over condition.
                if not movable_dict:
                    self.game_over()
                    print("\nShut down Checker Engine.\n")
                    return self.board
                # If there is movable checks, move
                self.move_phase(movable_dict)
            
            # Change turn player
            self.turn_player = 'W' if self.turn_player == 'B' else 'B'
        
        return
    
    # Only for dealing with error about GUI when running this file.
    def draw_pieces(self):
        return

#%% For debugging playing in this file.
# if __name__ == "__main__":
#     myGame = Game()
#     board = myGame.play_game()
#     print(board)

#%% To debug import_board().
if __name__ == "__main__":
    myGame = Game()
    board = [0 for _ in range(32)]
    board[8] = 1
    board[23] = -1
    board = [ -1,-1,-1,-1,
            -1,-1,-1,-1,
            -1,-1,-1,-1,
            0,0,0,0,
            0,0,0,0,
            1,1,1,1,
            1,1,1,1,
            1,1,1,1]

    print(board)
    myGame.import_board(board_in=board, turn_player_in='W')
    result = myGame.play_game()