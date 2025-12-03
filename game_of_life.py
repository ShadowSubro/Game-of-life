import pygame
import sys
import random

CELL_SIZE = 12
ROWS = 50
COLS = 80
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE + 40
BG_COLOR = (10, 10, 10)
GRID_COLOR = (40, 40, 40)
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
TEXT_COLOR = (200, 200, 200)
INITIAL_FPS = 10

pygame.init()
FONT = pygame.font.SysFont("consolas", 16)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life by shadowsubro")
clock = pygame.time.Clock()

def make_empty_grid(rows, cols):
    return [[0 for i in range(cols)] for _ in range(rows)]

def make_random_grid(rows, cols, p_alive=0.2):
    return [[1 if random.random() < p_alive else 0 for _ in range(cols)] for _ in range(rows)]

def count_neighbours(grid, x, y, rows, cols, wrap=False):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1), (0, 1),
                 (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if wrap:
            nx %= rows
            ny %= cols
        else:
            if not (0 <= nx < rows and 0 <= ny < cols):
                continue
        count += grid[nx][ny]
    return count

def next_generation(grid, rows, cols, wrap=False):
    new = make_empty_grid(rows, cols)
    for i in range(ROWS):
        for j in range(COLS):
            neighbours = count_neighbours(grid, i, j, rows, cols, wrap=wrap)
            if grid[i][j] == 1:
                new[i][j] = 1 if neighbours in (2, 3) else 0
            else:
                new[i][j] = 1 if neighbours == 3 else 0
    return new

def draw_grid(surface, grid, rows, cols, cell_size):
    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            color = ALIVE_COLOR if grid[i][j] == 1 else DEAD_COLOR
            pygame.draw.rect(surface, color, rect)

    # Overlay grid lines for clarity
    for x in range(0, cols * cell_size, cell_size):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, rows * cell_size))
    for y in range(0, rows * cell_size, cell_size):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (cols * cell_size, y))

def render_ui(surface, fps, generation, running, wrap_mode, speed):
    info = f"{'RUNNING' if running else 'PAUSED'}  |  Gen: {generation}  |  FPS target: {speed}  |  Wrap: {'ON' if wrap_mode else 'OFF'}"
    text_surf = FONT.render(info, True, TEXT_COLOR)
    surface.blit(text_surf, (8, ROWS * CELL_SIZE + 8))

    help_lines = "Space: Start/Pause   S: Step   C: Clear   R: Random   Up/Down: Speed   G: Glider   T: Toggle wrap"
    help_surf = FONT.render(help_lines, True, TEXT_COLOR)
    surface.blit(help_surf, (8, ROWS * CELL_SIZE + 24))

def place_pattern(grid, pattern, top_left_x, top_left_y, rows, cols):
    for i, row in enumerate(pattern):
        for j, val in enumerate(row):
            x = top_left_x + i
            y = top_left_y + j
            if 0 <= x < rows and 0 <= y < cols:
                grid[x][y] = val

GLIDER = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
]

def main():
    grid = make_empty_grid(ROWS, COLS)
    running = False
    generation = 0
    fps = INITIAL_FPS
    wrap_mode = False  # if True, edges wrap around (toroidal)
    mouse_down = False
    draw_value = 1  # value to draw while dragging (1 = alive, 0 = dead)

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse interactions: toggle cells by clicking/dragging
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < ROWS * CELL_SIZE:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        # left click toggles to alive, right click toggles to dead
                        if event.button == 1:
                            grid[row][col] = 1
                            draw_value = 1
                        elif event.button == 3:
                            grid[row][col] = 0
                            draw_value = 0
                        mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

            if event.type == pygame.MOUSEMOTION and mouse_down:
                x, y = event.pos
                if y < ROWS * CELL_SIZE:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        grid[row][col] = draw_value

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                elif event.key == pygame.K_c:
                    grid = make_empty_grid(ROWS, COLS)
                    generation = 0
                elif event.key == pygame.K_r:
                    grid = make_random_grid(ROWS, COLS, p_alive=0.2)
                    generation = 0
                elif event.key == pygame.K_s:
                    # step once when paused
                    if not running:
                        grid = next_generation(grid, ROWS, COLS, wrap=wrap_mode)
                        generation += 1
                elif event.key == pygame.K_UP:
                    fps = min(60, fps + 1)
                elif event.key == pygame.K_DOWN:
                    fps = max(1, fps - 1)
                elif event.key == pygame.K_g:
                    # place a glider at mouse pos
                    mx, my = pygame.mouse.get_pos()
                    place_pattern(grid, GLIDER, my // CELL_SIZE, mx // CELL_SIZE, ROWS, COLS)
                elif event.key == pygame.K_t:
                    wrap_mode = not wrap_mode

        # If running, compute next generation
        if running:
            grid = next_generation(grid, ROWS, COLS, wrap=wrap_mode)
            generation += 1

        # Draw
        screen.fill(BG_COLOR)
        draw_grid(screen, grid, ROWS, COLS, CELL_SIZE)
        render_ui(screen, clock.get_fps(), generation, running, wrap_mode, fps)

        pygame.display.flip()

if __name__ == "__main__":
    main()
