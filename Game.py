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
    
    def move_check(self):
        pos_start = str(list(map(int, input("Position of check you want to move (input as x,y): ").split(","))))
        pos_target = list(map(int, input("Position of tile you want to move to (input as x,y): ").split(",")))

        # Find check in start position
        if pos_start in self.checks_list.keys():
            # if check is attacking, call attack() method
            # if (str(pos_target) in self.checks_list.keys() \
            # and self.checks_list[str(pos_target)].side != self.checks_list[pos_start].side):
            #     self.attack(pos_start, pos_target)
            #     return
            

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
    
    def get_atk_list(self):
    # Find if there is any piece attacking another piece
    # Returns Dictionary as following:
    # str(Position of attacker): [list of str(target position)]
        atk_check_dict = dict()
        for check in self.checks_list.values():
            if check.side == self.turn_player:
                for posible_move in check.moves:
                    pos_atk = str([check.pos[i] + posible_move[i] for i in range(2)])
                    try:
                        # check if there is an enemy check in pos_atk
                        # and the position across the enemy is empty
                        if (self.checks_list[pos_atk].side != check.side) \
                        and (self.board[check.pos[1] + 2*posible_move[1]][check.pos[0] + 2*posible_move[0]] == 0):
                            # save in atk_check_dict
                            try:
                                atk_check_dict[(str(check.pos))].append(pos_atk)
                            except:
                                atk_check_dict[(str(check.pos))] = [pos_atk]
                    except:
                        pass
        
        return atk_check_dict

    def promote(self, pos_target):
        pass

    def attack(self, pos_start, pos_target):
        print("attack method has been called.\n")
