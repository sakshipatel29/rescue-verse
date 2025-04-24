from utils.actions import move

class SupplyBot:
    def __init__(self, x, y):
        self.name = "SupplyBot"
        self.x = x
        self.y = y
        self.kits = 2
        self.delivery_target = None
        self.phase = "idle"

    def act(self, grid, message_bus):
        if self.phase == "idle" and message_bus.get("medic_requests"):
            self.delivery_target = message_bus["medic_requests"].pop(0)
            self.phase = "deliver"

        if self.phase == "deliver":
            self.move_toward(self.delivery_target, grid)
            if (self.x, self.y) == self.delivery_target:
                self.kits -= 1
                print(f"{self.name} delivered med kit to MedicAgent!")
                message_bus["delivered_kits"] = True
                self.phase = "idle"

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
