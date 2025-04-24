
class DroneEye:
    def __init__(self, x, y):
        self.name = "DroneEye"
        self.x = x
        self.y = y
        
    def scan_area(self, grid):
        survivors = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 'S':
                    survivors.append((x,y))
        return survivors
    
    def act(self, grid, message_bus):
        found = self.scan_area(grid)
        if found:
            message_bus["scan_reports"].extend(found)
            print(f"{self.name} found survivors at: {found}")
        else:
            print(f"{self.name} found no survivors.")
