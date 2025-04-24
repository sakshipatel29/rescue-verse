from utils.actions import move, heal

class MedicAgent:
    def __init__(self, x, y):
        self.name = "MedicAgent"
        self.x = x
        self.y = y
        self.med_kits = 1
        self.target = None
        self.phase = "waiting"

    def receive_task(self, target):
        self.target = target
        self.phase = "go_to_patient"

    def act(self, grid, message_bus):
        if message_bus.get("delivered_kits"):
            print(f"{self.name} received a med kit!")
            self.med_kits += 1
            message_bus["delivered_kits"] = False
        
        if self.phase == "waiting":
            print(f"{self.name} is waiting for assignment.")
            return

        if self.phase == "go_to_patient":
            self.move_toward(self.target, grid)
            if (self.x, self.y) == self.target:
                if self.med_kits > 0:
                    heal(self, grid)
                    self.med_kits -= 1
                    self.phase = "done"
                else:
                    print(f"{self.name} needs med kit! Requesting...")
                    message_bus["medic_requests"] = [(self.x, self.y)]

        elif self.phase == "done":
            print(f"{self.name} finished healing.")

    def move_toward(self, target, grid):
        tx, ty = target
        if self.x < tx:
            move(self, "right", grid)
        elif self.x > tx:
            move(self, "left", grid)
        elif self.y < ty:
            move(self, "down", grid)
        elif self.y > ty:
            move(self, "up", grid)
