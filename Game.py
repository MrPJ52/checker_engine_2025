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
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.game_is_over = False
        self.turn_player = 'B'
        # checks_list = { str([x, y]) : Check instance }
        # Can act as following:
        # keys() = list of checks' position, values() = list of actual pieces
        self.checks_list = dict()

        # Create Checks for normal games
        for x in range(0, 8, 2):
            for y in range(3):
                self.checks_list[str([x+(1-y%2), y])] = Check([x+(1-y%2), y], "B")
        
        for x in range(0, 8, 2):
            for y in range(3):
                self.checks_list[str([x+(y%2), 7-y])] = Check([x+(y%2), 7-y], "W")
        
        # Create Checks for debugging
        # self.checks_list[str([1, 0])] = Check([1, 0], "B")
        # self.checks_list[str([5, 0])] = Check([5, 0], "B")
        # self.checks_list[str([2, 7])] = Check([2, 7], "W")
        # self.checks_list[str([6, 7])] = Check([6, 7], "W")

        #Create Checks for debugging game_over()
        # self.checks_list[str([1, 0])] = Check([1, 0], "B")
    
    #%% print_board() method.
    # Print board through console.
    def print_board(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        for piece in self.checks_list.values():
            self.board[piece.pos[1]][piece.pos[0]] = piece.notation
        
        # TODO: May need Optimazation
        print("    0   1   2   3   4   5   6   7")
        for y in range(8):
            print(f"{y}  ", end="")
            for x in range(8):
                if self.board[y][x] == 0:
                    print("|__|", end="")
                else:
                    print("|" + self.board[y][x] + "|", end="")
            print()
        
        print(f"It is {self.turn_player}'s turn.\n")
    
    #%% move_debug method.
    # Method to move check in any location.
    # Used to debug and test.
    def move_debug(self):
        print("Initiate debug move. If you want to skip this turn, enter SKIP.")
        try:
            pos_start = str(list(map(int, input("Position of check you want to move (input as x,y): ").split(","))))
            pos_target = list(map(int, input("Position of tile you want to move to (input as x,y): ").split(",")))
        except:
            return

        # Find check in start position
        if pos_start in self.checks_list.keys():
            self.checks_list[pos_start].move(pos_target)
            
            sleep(0.5)

            # Delete original_position:check and add new_position:check
            self.checks_list[str(pos_target)] = self.checks_list.pop(pos_start)
            # Check if it is promoted
            self.check_promotion(str(pos_target))
            # if moved, end the method
            return
        
        print("There is no check in start position.\n")
        return

    # TODO: there was an error about attack algorithm.
    # After move_debug(), one attackable check ignored it.
    # Couldn't find the reason, but might be fixed later.
    #%% find_targets() method.
    # Find if a check has attacking target.
    # Parameter: str(Position of attacker)
    def find_targets(self, checkPos:str):
        check = self.checks_list[checkPos]
        target_list = list()
        for posible_move in check.moves:
            pos_atked = str([check.pos[i] + posible_move[i] for i in range(2)])
            try:
                # Check if there is an enemy check in pos_atked
                # and the position across the enemy is empty or out of bound
                if (self.checks_list[pos_atked].side != check.side) \
                and (str([check.pos[1] + 2*posible_move[1], check.pos[0] + 2*posible_move[0]]) in self.checks_list.keys()) \
                and (0 <= check.pos[0] + 2*posible_move[0] <= 7) and (0 <= check.pos[1] + 2*posible_move[1] <= 7):
                    target_list.append(pos_atked)
            except:
                pass

        # Return [list of str(position of target)]
        if target_list:
            return target_list
        else:
            return None
    
    #%% get_atk_dict() method.
    # Find if there is any piece attacking another piece.
    def get_atk_dict(self):
        # Returns Dictionary as following:
        # { str(Position of attacker): [list of str(target position)] }
        atk_check_dict = dict()
        for check in self.checks_list.values():
            if check.side == self.turn_player:
                targets = self.find_targets(str(check.pos))
                if targets:
                    try:
                        for target in targets:
                            atk_check_dict[(str(check.pos))].append(str(target))
                    except:
                        atk_check_dict[(str(check.pos))] = targets
        
        return atk_check_dict
    
    #%% attack_phase() method.
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
        
        sleep(0.5)

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
        sleep(0.5)

        # Call attack() method and get return value
        movePos = self.attack(atkPos=atkPos, targetPos=targetPos)

        # print board so that user can notice how that moved
        self.print_board()
        sleep(0.5)

        # check if the attacker has to be promoted
        # if promoted, end attack_phase()
        if self.check_promotion(str(movePos)):
            return

        # call find_targets(position of attacker) to find if there is more target be able to attack.
        # if target found, return attack_phase({ str(attacker's position) : [list of its targets] }, True)
        # if no target was found, end attack_phase()
        more_targets = self.find_targets(str(movePos))
        if more_targets:
            GUI.draw_pieces()
            sleep(0.5)
            return self.attack_phase({str(movePos): more_targets}, GUI, True)
        else:
            return
            
    #%% attack() method.
    # Move attacker and delete target.
    # Parameter: str(attacker's pos), str(target's position)
    def attack(self, atkPos:str, targetPos:str):
        # Move attacker's position
        for possible_move in self.checks_list[atkPos].moves:
            if str([self.checks_list[atkPos].pos[i] + possible_move[i] for i in range(2)]) == targetPos:
                movePos = [self.checks_list[atkPos].pos[i] + 2*possible_move[i] for i in range(2)]
                break

        self.checks_list[str(movePos)] = self.checks_list.pop(atkPos)
        self.checks_list[str(movePos)].move(movePos)
        sleep(0.5)

        # Call target.captured() method of target to print in console, and delete target
        self.checks_list.pop(targetPos).captured()
        sleep(0.5)

        # Return movePos (position of attacker after attack)
        return movePos

    #%% get_move_dict() method.
    # Find if there is any movable space.
    def get_move_dict(self):
        # Find movable checks
        # dictionary as following:
        # { str(movable checks' position) : [list of movable blanks] }
        mover_check_dict = dict()
        for check in self.checks_list.values():
            if check.side == self.turn_player:
                # Check all possible moves
                for posible_move in check.moves:
                    pos_move = [check.pos[i] + posible_move[i] for i in range(2)]
                    try:
                        # Check if pos_move is empty and not out of bound
                        if (not (str(pos_move) in self.checks_list.keys() )) \
                        and (0 <= check.pos[0] + posible_move[0] <= 7) and (0 <= check.pos[1] + posible_move[1] <= 7):
                            try:
                                mover_check_dict[(str(check.pos))].append(pos_move)
                            except:
                                mover_check_dict[(str(check.pos))] = [pos_move]

                    except:
                        pass
        
        # Return dictionary of movable places' position
        if mover_check_dict:
            return mover_check_dict
        else:
            return None

    #%% move_phase() method.
    # Proceed move phase and control it.
    # Parameter: return of get_move_dict()
    def move_phase(self, movable_dict):
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
        self.check_promotion(str(destinedPos))

        return
    
    #%% move() method.
    # Move check from start position to destined position.
    # Parameter: str(start position), destined position
    def move(self, startPos:str, destinedPos:list):
        self.checks_list[startPos].move(destinedPos)
        self.checks_list[str(destinedPos)] = self.checks_list.pop(startPos)

        return
    
    #%% check_promotion() method.
    # Find whether the check has to promote.
    # Parameter: str(position of check)
    def check_promotion(self, checkPos:str):
        if (self.checks_list[checkPos].side == "B" and self.checks_list[checkPos].pos[1] == 7) \
            or (self.checks_list[checkPos].side == "W" and self.checks_list[checkPos].pos[1] == 0):
            # Promotion : Create a King in the same position and delete original Check
            self.checks_list[checkPos] = King(self.checks_list[checkPos].pos, self.checks_list[checkPos].side)
            # if promoted, return True so that other method can notice
            return True

    #%% game_over() method.
    def game_over(self):
        self.game_is_over = True
        print(f"There is no check left or possible moves for {self.turn_player}.\n")
        winner = "B" if (self.turn_player == "W") else "W"

        print(f"\n{winner} winned!\n")

        return
    