import pygame

CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 10
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 100  # Extra space for stats

COLORS = {
    '.': (240, 240, 240),
    '#': (80, 80, 80),
    'S': (255, 215, 0),
    'R': (0, 120, 255),
    'T': (255, 105, 180),
    'M': (0, 200, 0),
    'C': (150, 0, 255),
    'D': (100, 200, 255),
    'F': (255, 0, 0)
}

_initialized = False
_screen = None
_font = None

def init_display():
    global _initialized, _screen, _font
    if not _initialized:
        pygame.init()
        _screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("RescueVerse Visualizer")
        _font = pygame.font.SysFont("consolas", 20)
        _initialized = True
        
mode = "auto"

def render_grid(grid, step, reward, rescued, agent_states, agent_states_list):
    global _screen, mode
    if not _initialized:
        init_display()

    wait_next_step = True
    while wait_next_step:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RIGHT:
                    mode = "paused"
                    wait_next_step = False  # go to next step
                elif event.key == pygame.K_SPACE:
                    mode = "auto" if mode == "paused" else "paused"
                elif event.key == pygame.K_LEFT:
                    print("[←] Backward step pressed (not implemented)")  # Future feature

        _screen.fill((30, 30, 30))

        # Draw grid
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                color = COLORS.get(cell, (200, 200, 200))
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(_screen, color, rect)
                pygame.draw.rect(_screen, (200, 200, 200), rect, 1)

        # Stats + instructions
        stats = [
            f"Step: {step}",
            f"Reward: {round(reward, 2)}",
            f"Rescued: {rescued}",
            f"Mode: {mode.upper()} — [→] Next | [SPACE] Toggle | [ESC] Quit"
        ]
        for i, text in enumerate(stats):
            label = _font.render(text, True, (255, 255, 255))
            _screen.blit(label, (10, GRID_HEIGHT * CELL_SIZE + 10 + i * 25))

        # Agent phases
        # Agent stats & phase
        for i, (name, phase) in enumerate(agent_states.items()):
            agent = [a for a in agent_states_list if a.name == name][0]
            label = _font.render(
                f"{name}: {phase} | Rescues: {getattr(agent, 'rescues_done', 0)} | Steps: {getattr(agent, 'steps_taken', 0)}",
                True, (200, 255, 200)
            )
            _screen.blit(label, (300, GRID_HEIGHT * CELL_SIZE + 10 + i * 25))


        pygame.display.flip()

        if mode == "auto":
            pygame.time.wait(800)  # wait 800ms per step
            wait_next_step = False
        elif mode == "paused":
            pygame.time.wait(100)