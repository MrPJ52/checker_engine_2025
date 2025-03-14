class Check:
    def __init__(self, Pos, Side): #체커의 위치와 편을 인수로 받음
        self.pos = Pos #[x, y]
        self.side = Side
        if self.side == "B":
            self.moves = [[1, 1], [-1, 1]]
        else:
            self.moves = [[1, -1], [-1, -1]]
        self.notation = self.side + "M"
    
    def captured(self):
        print("\nCheck in position" + str(self.pos) + " is captured.\n")
    
    def move(self, Target):
        print(f"{self.pos} moved to {Target} .\n")
        self.pos = Target



class King(Check):
    def __init__(self, Pos, Side):
        super().__init__(Pos, Side)
        self.moves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        self.notation = self.side + "K"
        print("Check in position" + str(self.pos) + " has been promoted to King.\n")