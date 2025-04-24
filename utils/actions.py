def move(agent, direction, grid):
    dx, dy = 0, 0
    if direction == "up":
        dy = -1
    elif direction == "down":
        dy = 1
    elif direction == "left":
        dx = -1
    elif direction == "right":
        dx = 1

    new_x = agent.x + dx
    new_y = agent.y + dy

    if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
        destination = grid[new_y][new_x]

        # Define allowed cells: empty '.', survivor 'S', or command center 'C'
        allowed = ['.', 'S', 'C']

        if destination in allowed:
            # Clear old position
            grid[agent.y][agent.x] = '.'
            agent.x, agent.y = new_x, new_y
            grid[agent.y][agent.x] = agent.name[0]
            print(f"{agent.name} moved to ({agent.x}, {agent.y})")
        else:
            print(f"{agent.name} blocked at ({new_x}, {new_y}) - {destination}")
    else:
        print(f"{agent.name} tried to move out of bounds.")

        
def pickup(agent, grid):
    # Assume survivor is at target (the agent's task)
    if not agent.carrying_survivor:
        print(f"{agent.name} picked up a survivor at ({agent.x}, {agent.y})!")
        agent.carrying_survivor = True
        if hasattr(agent, "rescues_done"):
            agent.rescues_done += 1
        # Optional: Remove S from map if it's still there
        if grid[agent.y][agent.x] == 'S':
            grid[agent.y][agent.x] = agent.name[0]


def drop(agent, grid):
    if agent.carrying_survivor and grid[agent.y][agent.x] == 'C':
        agent.carrying_survivor = False
        print("{agent.name} dropped the survivor at Command Center.")
        
def heal(agent, grid):
    if grid[agent.y][agent.x] == 'S' and agent.med_kits > 0:
        print(f"{agent.name} healed a survivor at ({agent.x}, {agent.y}).")
        agent.med_kits -= 1
        
def scan(grid):
    found = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'S':
                found.append((x, y))
    return found
            
            