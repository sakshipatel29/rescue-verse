class RescueVerseMap:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = self.create_empty_grid()
        self.place_initial_objects()
        
    def create_empty_grid(self):
        return [['.' for _ in range(self.width)] for _ in range(self.height)]
    
    def place_initial_objects(self):
        self.grid[0][4] = '#'  # Obstacle
        self.grid[0][6] = 'S'  # Survivor
        self.grid[3][2] = 'F'  # First Aid
        self.grid[5][5] = 'R'  # RescueBot
        self.grid[7][5] = 'T'  # SupplyBot
        self.grid[7][6] = 'M'  # Medic
        self.grid[8][1] = 'D'  # DroneEye
        self.grid[9][5] = 'C'  # CommandCenter
        
    def render(self):
        print("\n=== RescueVerse World Map ===")
        
        for row in self.grid:
            print(' '.join(row))
            
        print("==============================\n")
            
    def get_symbol_at(self, x, y):
        return self.grid[y][x]  # y is row and x is column
    
    def set_symbol_at(self, x, y, symbol):
        self.grid[y][x] = symbol