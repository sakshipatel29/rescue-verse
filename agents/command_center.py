class CommandCenter:
    def __init__(self):
        self.name = "CommandCenter"
        self.known_survivors = []
        self.assigned = False

    def act(self, grid, message_bus):
        reports = message_bus.get("scan_reports", [])
        for coord in reports:
            if coord not in self.known_survivors:
                self.known_survivors.append(coord)

        if self.known_survivors and not self.assigned:
            task = self.known_survivors.pop(0)
            message_bus["to_rescuebot"] = [task]
            print(f"{self.name} assigned RescueBot to {task}")
            self.assigned = True
