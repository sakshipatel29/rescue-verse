
class CommandCenter:
    def __init__(self):
        self.known_survivors = []
        self.task_queue = []
    
    def receive_scan_reports(self, reports):
        for r in reports:
            if r not in self.known_survivors:
                self.known_survivors.append(r)
                self.task_queue.append(r)
                
    def assign_task(self, agents):
        while self.task_queue and agents:
            target = self.task_queue.pop(0)
            agent = agents.pop(0)
            agent.receive_task(target)
            print(f"{self.name} assigned {target} to {agent.name}")
            