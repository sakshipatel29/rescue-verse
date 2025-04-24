
class MedicAgent:
    def __init__(self,x,y):
        self.name = "MedicAgent"
        self.x = x
        self.y = y
        self.med_kits = 1
        self.target = None
        
    def receive_task(self, task):
        self.target = task
        
    def act(self, grid, message_bus):
        if self.target:
            print(f"{self.name} moving toward {self.target} to heal.")
        else:
            print(f"{self.name} waiting for patient.")
            
