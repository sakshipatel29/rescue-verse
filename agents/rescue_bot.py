from utils.actions import move, pickup, drop

class RescueBot:
    def __init__(self, x, y):
        self.name = "RescueBot"
        self.x = x
        self.y = y
        self.carrying_survivor = False
        self.phase = "waiting"
        self.target = None
        self.drop_point = (5, 9)  # Command center

    def receive_task(self, target):
        self.target = target
        self.phase = "go_to_survivor"

    def act(self, grid, message_bus):
        if self.phase == "waiting":
            print(f"{self.name} is waiting for a task.")

        elif self.phase == "go_to_survivor":
            self.move_toward(self.target, grid)
            if (self.x, self.y) == self.target:
                pickup(self, grid)
                if self.carrying_survivor:
                    self.phase = "go_to_command"

        elif self.phase == "go_to_command":
            self.move_toward(self.drop_point, grid)
            if (self.x, self.y) == self.drop_point:
                drop(self, grid)
                self.phase = "done"

        elif self.phase == "done":
            print(f"{self.name} mission complete.")

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
