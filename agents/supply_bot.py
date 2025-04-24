
class SupplyBot:
    def __init__(self, x, y):
        self.name = "SupplyBot"
        self.x = x
        self.y = y
        self.supplies = 2
        self.delivery_target = None
        
    def receive_task(self, task):
        self.delivery_target = task
        
    def act(self, grid, message_bus):
        if self.delivery_target:
            print(f"{self.name} delivering supplies to {self.delivery_target}.")
        else:
            print(f"{self.name} idle.")
        