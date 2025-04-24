from utils.pathfinding import find_path
from utils.actions import move

class RescueBot:
    def __init__(self, x, y, bot_id = 1):
        self.name = f"RescueBot-{bot_id}"
        self.x = x
        self.y = y
        self.carrying_survivor = False
        self.phase = "waiting"
        self.target = None
        self.drop_point = (5, 9)
        self.path = []
        self.steps_taken = 0
        self.rescues_done = 0
        self.prev_position = (x, y)


    def receive_task(self, target):
        self.target = target
        self.phase = "go_to_survivor"
        self.path = []

    def act(self, grid, message_bus):
        if self.phase == "waiting":
            print(f"{self.name} is waiting.")
            return

        if self.phase == "go_to_survivor":
            if not self.path:
                self.path = find_path((self.x, self.y), self.target, grid)
            self.follow_path(grid)

            if (self.x, self.y) == self.target:
                from utils.actions import pickup
                pickup(self, grid)
                if self.carrying_survivor:
                    self.phase = "go_to_command"
                    self.path = []

        elif self.phase == "go_to_command":
            if not self.path:
                self.path = find_path((self.x, self.y), self.drop_point, grid)
            self.follow_path(grid)

            if (self.x, self.y) == self.drop_point:
                from utils.actions import drop
                drop(self, grid)
                self.phase = "done"

    def follow_path(self, grid):
        if self.path:
            next_step = self.path.pop(0)
            if (self.x, self.y) != next_step:
                self.steps_taken += 1
            nx, ny = next_step
            dx = nx - self.x
            dy = ny - self.y
            if dx == 1: move(self, "right", grid)
            elif dx == -1: move(self, "left", grid)
            elif dy == 1: move(self, "down", grid)
            elif dy == -1: move(self, "up", grid)
