import numpy as np
from env.rescueverse_map import RescueVerseMap
from utils.actions import move, pickup, drop, heal, scan

class RescueVerseEnv:
    def __init__(self):
        self.map = RescueVerseMap()
        self.agents = []  # will contain instances of RescueBot, MedicAgent, etc.
        self.message_bus = {
            "scan_reports": [],
            "to_rescuebot": [],
            "to_supplybot": []
        }
        self.total_reward = 0

    def reset(self):
        self.map = RescueVerseMap()
        self.total_reward = 0

    def step(self):
        step_reward = 0

        for agent in self.agents:
            if not hasattr(agent, 'act'):
                continue

            # Check if the agent can move
            if hasattr(agent, 'x') and hasattr(agent, 'y'):
                old_x, old_y = agent.x, agent.y
                agent.act(self.map.grid, self.message_bus)

                # Reward: Movement without work
                if (agent.x, agent.y) == (old_x, old_y):
                    step_reward -= 0.1

                # Reward: RescueBot drops survivor at C
                if hasattr(agent, 'carrying_survivor') and agent.carrying_survivor is False:
                    if self.map.grid[agent.y][agent.x] == 'C':
                        step_reward += 10  # rescued

            else:
                # Stationary agents like CommandCenter
                agent.act(self.map.grid, self.message_bus)

            # Penalty: Survivor not rescued
            survivors_remaining = any('S' in row for row in self.map.grid)
            if not survivors_remaining:
                step_reward -= 10  # no survivors left but not rescued

            # Medic heals
            if hasattr(agent, 'med_kits') and agent.med_kits < 1:
                step_reward += 2  # medkit used properly

            # Wasting resource
            if hasattr(agent, 'med_kits') and agent.med_kits == 0:
                step_reward -= 3

        self.total_reward += step_reward
        return self.total_reward

    def render(self):
        self.map.render()
        print(f"Current Reward: {self.total_reward}")