class CommandCenter:
    def __init__(self):
        self.name = "CommandCenter"
        self.known_survivors = []
        self.assigned_targets = set()

    def act(self, grid, message_bus):
        # Get fresh scan reports
        reports = message_bus.get("scan_reports", [])

        # Add unassigned survivors to task list
        for coord in reports:
            if coord not in self.known_survivors and coord not in self.assigned_targets:
                self.known_survivors.append(coord)

        # Assign survivors to available RescueBots
        available_bots = [
            agent for agent in message_bus.get("agents", [])
            if agent.name.startswith("RescueBot") and agent.phase == "waiting"
        ]

        while self.known_survivors and available_bots:
            survivor = self.known_survivors.pop(0)
            bot = available_bots.pop(0)
            bot.receive_task(survivor)
            self.assigned_targets.add(survivor)
            print(f"{self.name} assigned {bot.name} to survivor at {survivor}")
