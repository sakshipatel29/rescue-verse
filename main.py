from env.rescueverse_env import RescueVerseEnv
from agents.rescue_bot import RescueBot
from agents.drone_eye import DroneEye
from agents.command_center import CommandCenter
from agents.medic_agent import MedicAgent
from agents.supply_bot import SupplyBot
from visualizer import render_grid

def main():
    env = RescueVerseEnv()

    # Instantiate agents
    rescue1 = RescueBot(x=5, y=5, bot_id=1)
    rescue2 = RescueBot(x=0, y=5, bot_id=2)
    rescue3 = RescueBot(x=9, y=5, bot_id=3)
    drone = DroneEye(x=1, y=8)
    commander = CommandCenter()
    medic = MedicAgent(x=6, y=7)
    supply = SupplyBot(x=5, y=7)

    # Register them
    env.agents = [drone, commander, medic, supply, rescue1, rescue2, rescue3]
    env.message_bus = {
        "scan_reports": [],
        "to_rescuebot": [],
        "to_medic": [],
        "medic_requests": [],
        "delivered_kits": False
    }
    env.message_bus["agents"] = env.agents
    
    rescued_count = 0

    # Simulation loop
    for step in range(15):
        print(f"\n--- Step {step + 1} ---")

        # Count survivors remaining
        survivors_remaining = sum(row.count('S') for row in env.map.grid)
        rescued_count = 3 - survivors_remaining  # Assume 3 total

        # Track agent phases
        agent_states = {}
        for agent in env.agents:
            if agent.name.startswith("RescueBot"):
                agent_states[agent.name] = getattr(agent, "phase", "unknown")

        # 👇 Render with stats
        rescue_bots = [a for a in env.agents if a.name.startswith("RescueBot")]

        render_grid(
            env.map.grid,
            step + 1,
            env.total_reward,
            rescued_count,
            {bot.name: bot.phase for bot in rescue_bots},
            rescue_bots  # 👈 NEW: full agent objects list
        )

        # Run agents
        env.message_bus["agents"] = env.agents
        drone.act(env.map.grid, env.message_bus)
        commander.act(env.map.grid, env.message_bus)

        if env.message_bus["to_rescuebot"]:
            for bot in [a for a in env.agents if a.name.startswith("RescueBot") and a.phase == "waiting"]:
                if env.message_bus["to_rescuebot"]:
                    task = env.message_bus["to_rescuebot"].pop(0)
                    bot.receive_task(task)

        if env.message_bus["to_medic"]:
            medic.receive_task(env.message_bus["to_medic"].pop(0))

        medic.act(env.map.grid, env.message_bus)
        supply.act(env.map.grid, env.message_bus)

        for agent in env.agents:
            if agent.name.startswith("RescueBot"):
                agent.act(env.map.grid, env.message_bus)

        reward = env.step()
        print(f"Total Reward: {reward}")

if __name__ == "__main__":
    main()
