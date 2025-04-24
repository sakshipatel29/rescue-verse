
class RescueBot:
    def __init__(self, x, y):
        self.name = "RescueBot"
        self.x = x
        self.y = y
        self.carrying_survivor = False
        self.target = None # (x, y) coordinate of survivor
        
    def receive_task(self, task):
        self.target = task
    
    def act(self, grid, message_bus):
        if self.target:
            print(f"{self.name} moving towards {self.target}.")
        else
            print(f"{self.name} waiting for assignment.")
            
            