import tkinter as tk
import game
from player_bot import PlayerBot
from time import sleep

#%% CheckersGUI class: Overall system including game system
# and GUI control.
class CheckersGUI:
    def __init__(self, root:tk.Tk):
        # Create tkinter instance to open a window, initial setting
        # Argument "root" is tkinter window that this class will send and control.
        self.root = root
        self.root.title("Checker Engine")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.gui_sleep_time = 500
        
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        
        # in CheckersGUI, it has a Game field to run checker game
        self.game = game.Game()

        # methods to draw board and pieces
        self.draw_board()
        self.draw_pieces()
        
        # Input whether the bot is playing or not
        print("If bot is playing, input 'B' or 'W, if both 2, if none 0: ", end="")
        inputSide = str(input().strip())
        # If there is, Create member variable and reset it with PlayerAI instance
        if (inputSide == '2'):
            self.aiPlayer = list((PlayerBot('B'), PlayerBot('W')))
        elif (inputSide != '0'):
            self.aiPlayer = PlayerBot(inputSide)
        
        # 1000ms after CheckersGUI instance is created,
        # start game_loop() method to run self.game
        self.root.after(self.gui_sleep_time, self.game_loop)
    
    #%% draw_board() and draw_pieces() methods.
    def draw_board(self):
        tile_size = 50
        # Draw x-index
        for i in range(9):
            self.canvas.create_rectangle(i * tile_size, tile_size,
                                         (i+1) * tile_size, 2*tile_size,
                                         fill="white")
            if i == 0:
                continue

            self.canvas.create_text(i * tile_size + 25, tile_size + 25, font=("Arial", 20), text = str(i-1))
        
        for row in range(8):
            # Draw y-index
            self.canvas.create_rectangle(0, (row + 2) * tile_size,
                                         tile_size, (row + 3) * tile_size,
                                         fill="white")
            self.canvas.create_text(25, (row + 2) * tile_size + 25, font=("Arial", 20), text = str(row))

            # Draw board
            for col in range(8):
                color = "black" if (row + col) % 2 == 1 else "white"
                self.canvas.create_rectangle((col + 1) * tile_size, (row + 2) * tile_size,
                                             (col + 2) * tile_size, (row + 3) * tile_size,
                                             fill=color)
    
    def draw_pieces(self):
        # everytime this method is called, reset drawn pieces from canvas
        self.canvas.delete("pieces")
        # and re-draw pieces
        tile_size = 50
        for piece in self.game.checks_list.values():
            x, y = piece.pos
            color = "#45312c" if piece.side == "B" else "#c23a39"
            self.canvas.create_oval((x + 1) * tile_size + 10, (y + 2) * tile_size + 10,
                                    (x + 2) * tile_size - 10, (y + 3) * tile_size - 10,
                                    fill=color, outline="white", tags="pieces")
            if piece.notation[1] == "K":
                self.canvas.create_text((x + 1) * tile_size + 26, (y + 2) * tile_size + 25,
                                    font = ("Arial", 10), fill = "white", text = piece.notation, tags="pieces")
    

    #%% game_loop() method.
    # Implemented as recursive method to repeat the turn.
    def game_loop(self):
        # if there are two bots, call aiPlay()
        try:
            if (len(self.aiPlayer) == 2):
                self.aiPlay()
                return
        except:
            pass
        
        if self.game.game_is_over:
            print("\nShut down Checker Engine.\n")
            return
        
        # Print board in console, and draw pieces in tkinter window
        self.game.print_board()
        self.draw_pieces()
        
        print(f"\nIt is {self.game.turn_player}'s turn.\n")
        # If there is AI, call methods from PlayerAI instance.
        try:
            if (self.aiPlayer.side == self.game.turn_player):
                self.aiPlayer.playTurn(self.game)
                return self.root.after(self.gui_sleep_time, self.game_loop)
            # AttributeError will occur if there is no aiPlayer
        except:
            pass

        # Find if there is any attacking checks
        # If there is, attack
        attackable_dict = self.game.get_atk_dict()
        if attackable_dict:
            self.game.attack_phase(attackable_dict, self, False)
        # If there is not,
        # Find if there is any movable checks
        else:
            movable_dict = self.game.get_move_dict()
            # If there is no movable checks,
            # Turn player is defeated, end game
            if not movable_dict:
                self.game.game_over()
                print("\nShut down Checker Engine.\n")
                return
            # If there is movable checks, move
            self.game.move_phase(movable_dict)
        
        # Change turn player
        self.game.turn_player = 'W' if self.game.turn_player == 'B' else 'B'
        self.root.after(self.gui_sleep_time, self.game_loop)
    
    #%% aiPlay() method.
    # Let bots play a whole game and show it.
    def aiPlay(self):
        # Set sleep time shorter
        self.gui_sleep_time = 50
        self.game.sleep_time = 0.05

        if self.game.game_is_over:
            self.root.destroy()
            return
        
        print(f"\nIt is {self.game.turn_player}'s turn.\n")
        # set turn-playing bot
        current_bot = self.aiPlayer[0] if self.game.turn_player == 'B' else self.aiPlayer[1]
        current_bot.playTurn(self.game)

        self.game.print_board()
        self.draw_pieces()

        self.root.after(self.gui_sleep_time, self.aiPlay)

        return

#%% if this file is run directly,
# Create CheckersGUI instance and run
if __name__ == "__main__":
    # Create Tk() window
    root = tk.Tk()
    # Create CheckersGUI instance with argument "root"
    # By the constructor of CheckersGUI, it'll autumatically initiate game_loop()
    app = CheckersGUI(root)
    # Run root to open new window
    root.mainloop()