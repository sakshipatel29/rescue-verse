from env.rescueverse_env import RescueVerseEnv
from agents.rescue_bot import RescueBot
from agents.drone_eye import DroneEye
from agents.command_center import CommandCenter
from agents.medic_agent import MedicAgent
from agents.supply_bot import SupplyBot

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

    # Simulation loop
    for step in range(15):
        print(f"\n--- Step {step + 1} ---")
        env.render()

        # DroneEye → scan survivors
        drone.act(env.map.grid, env.message_bus)
        
        env.message_bus["agents"] = env.agents

        # CommandCenter → assign RescueBot and MedicAgent
        commander.act(env.map.grid, env.message_bus)

        if env.message_bus["to_rescuebot"]:
            rescue_bot.receive_task(env.message_bus["to_rescuebot"].pop(0))

        if env.message_bus["to_medic"]:
            medic.receive_task(env.message_bus["to_medic"].pop(0))

        # Agents take turns
        medic.act(env.map.grid, env.message_bus)
        supply.act(env.map.grid, env.message_bus)
        for agent in env.agents:
            if agent.name.startswith("RescueBot"):
                agent.act(env.map.grid, env.message_bus)

        reward = env.step()
        print(f"Total Reward: {reward}")

if __name__ == "__main__":
    main()
