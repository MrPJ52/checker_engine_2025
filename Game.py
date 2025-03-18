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


class Game:
    # initial setting
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.game_over = False
        self.turn_player = 'B'
        # str([x, y]) : Check instance
        # Can act as following:
        # keys() = list of checks' position, values() = list of actual pieces
        self.checks_list = dict()

        #Create Checks
        for x in range(0, 8, 2):
            for y in range(3):
                self.checks_list[str([x+(1-y%2), y])] = Check([x+(1-y%2), y], "B")
        
        for x in range(0, 8, 2):
            for y in range(3):
                self.checks_list[str([x+(y%2), 7-y])] = Check([x+(y%2), 7-y], "W")    
    
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
    
    # Method to move check in any location.
    # Used to debug and test.
    def move_debug(self):
        pos_start = str(list(map(int, input("Position of check you want to move (input as x,y): ").split(","))))
        pos_target = list(map(int, input("Position of tile you want to move to (input as x,y): ").split(",")))

        # Find check in start position
        if pos_start in self.checks_list.keys():
            self.checks_list[pos_start].move(pos_target)
            
            sleep(0.5)

            # Promotion : Create a King in the same position and delete original Check
            # TODO : Need to be moved into promote() method
            if (self.checks_list[pos_start].side == "B" and self.checks_list[pos_start].pos[1] == 7) or (self.checks_list[pos_start].side == "W" and self.checks_list[pos_start].pos[1] == 0):

                self.checks_list[pos_start] = King(self.checks_list[pos_start].pos, self.checks_list[pos_start].side)

            # Delete original_position:check and add new_position:check
            self.checks_list[str(pos_target)] = self.checks_list.pop(pos_start)
            # if moved, end the method
            return
        
        print("There is no check in start position.\n")
        return
    
    def get_atk_dict(self):
    # Find if there is any piece attacking another piece
    # Returns Dictionary as following:
    # str(Position of attacker): [list of str(target position)]
        atk_check_dict = dict()
        for check in self.checks_list.values():
            if check.side == self.turn_player:
                # TODO: Separate method for each checks to check the targets
                # It is to re-use the method in attack() method.
                targets = self.find_targets(str(check.pos))
                if targets:
                    try:
                        for target in targets:
                            atk_check_dict[(str(check.pos))].append(str(target))
                    except:
                        atk_check_dict[(str(check.pos))] = targets
        
        return atk_check_dict

    # Parameter: Dictionary that is result of get_atk_dict, Boolean to check player has already attacked
    def attack(self, atk_dict, alreadyAtked):
        if (not alreadyAtked):
            print("Attackable checks are:")
            for pos in atk_dict.keys():
                print(pos, end="  ")
            
            print("Choose which one to start attack(Input nth): ", end="")
            atkPosNum = int(input())
            atkPos = atk_dict.keys()[atkPosNum]

        # If attacker has one and only target, choose it automatically
        if len(atk_dict[atkPos]) == 1:
            targetPos = atk_dict[atkPos][0]
        
        #If attacker has multiple targets, choose which one to attack
        else:
            print("This attacker has following targets: ")
            for targetPos in atk_dict[atkPos]:
                print(targetPos, end="  ")
            print("Choose the target(Input nth): ", end = "")

            targetPosNum = int(input())
            targetPos = atk_dict[atkPos][targetPosNum]
        

        print(f"Check in position {atkPos} attacks {targetPos}")
        # Call captured() method of target and delete it
        self.checks_list.pop(targetPos).captured()

    # Parameter: str(Position of attacker)
    def find_targets(self, checkPos):
        check = self.checks_list[checkPos]
        for posible_move in check.moves:
            pos_atk = str([check.pos[i] + posible_move[i] for i in range(2)])
            try:
                # check if there is an enemy check in pos_atk
                # and the position across the enemy is empty
                if (self.checks_list[pos_atk].side != check.side) \
                and (self.board[check.pos[1] + 2*posible_move[1]][check.pos[0] + 2*posible_move[0]] == 0):
                    try:
                        target_list.append(pos_atk)
                    except:
                        target_list = [pos_atk]
            except:
                pass

            # Return list of str(position of target)
            try:
                return target_list
            except:
                return
        

    def promote(self, pos_target):
        pass