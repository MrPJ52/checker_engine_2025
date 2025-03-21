import tkinter as tk
from tkinter_GUI import CheckersGUI

#%% Run main
# Create Tk() window
root = tk.Tk()
# Create CheckersGUI instance with argument "root"
# By the constructor of CheckersGUI, it'll autumatically initiate game_loop()
app = CheckersGUI(root)
# Run root to open new window
root.mainloop()