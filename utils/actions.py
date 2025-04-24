def move(agent, direction, grid):
    dx, dy =  0, 0
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
        if grid[new_y][new_x] == '.':
            #Move agent
            grid[agent.y][agent.x] = '.'
            agent.x, agent.y = new_x, new_y
            grid[agent.y][agent.x] = agent.name[0]
            print(f"{agent.name} moved to ({agent.x}, {agent.y}).")
        else:
            print(f"{agent.name} blocked at ({new_x}, {new_y}).")
    else: 
        print(f"{agent.name} cannot move outside grid bounds.")
        
def pickup(agent, grid):
    if grid[agent.y][agent.x] == 'S' and not agent.carrying_survivor:
        agent.carrying_survivor = True
        print("{agent.name} picked up a survivor.")
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
            
            