import pygame
import random
from collections import deque

# Ініціалізація pygame
pygame.init()

# Розміри вікна
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FINISH_COLOR = (128, 0, 128)  # Фіолетовий для фінішу

# Ігрове вікно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

# Таймер
clock = pygame.time.Clock()
FPS = 10

# Генерація лабіринту з випадковими стінами
def generate_maze(grid_width, grid_height):
    maze = [[1 if random.random() < 0.3 else 0 for _ in range(grid_width)] for _ in range(grid_height)]
    maze[0][0] = 0  # Старт пакмена
    maze[grid_height - 1][grid_width - 1] = 0  # Фініш
    return maze

# BFS для перевірки прохідності лабіринту
def is_path_exists(maze, start, goal):
    queue = deque([start])
    visited = set([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and (nx, ny) not in visited and maze[nx][ny] == 0:
                queue.append((nx, ny))
                visited.add((nx, ny))
    return False

# Рух гравця
def move_player(pos, direction, maze):
    x, y = pos
    dx, dy = direction
    new_pos = (x + dx, y + dy)
    if 0 <= new_pos[0] < len(maze) and 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] == 0:
        return new_pos
    return pos

# Малювання лабіринту
def draw_maze(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            color = BLACK if cell == 1 else WHITE
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Малювання гравця, привидів і фінішу
def draw_player(pos):
    pygame.draw.circle(screen, YELLOW, (pos[1] * CELL_SIZE + CELL_SIZE // 2, pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

def draw_ghosts(ghosts):
    for ghost in ghosts:
        pygame.draw.circle(screen, RED, (ghost[1] * CELL_SIZE + CELL_SIZE // 2, ghost[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

def draw_finish(finish):
    pygame.draw.rect(screen, FINISH_COLOR, (finish[1] * CELL_SIZE, finish[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
# BFS для руху привидів
def bfs(maze, start, goal):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and (nx, ny) not in came_from and maze[nx][ny] == 0:
                queue.append((nx, ny))
                came_from[(nx, ny)] = current
    return []

# Головна функція
def main():
    while True:
        maze = generate_maze(GRID_WIDTH, GRID_HEIGHT)
        if is_path_exists(maze, (0, 0), (GRID_HEIGHT - 1, GRID_WIDTH - 1)):
            break  # Перевірка, чи є шлях від старту до фінішу

    player_pos = (0, 0)
    finish_pos = (GRID_HEIGHT - 1, GRID_WIDTH - 1)
    ghosts = [(GRID_HEIGHT - 1, 0), (0, GRID_WIDTH - 1)]
    direction = (0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = (-1, 0)
                elif event.key == pygame.K_DOWN:
                    direction = (1, 0)
                elif event.key == pygame.K_LEFT:
                    direction = (0, -1)
                elif event.key == pygame.K_RIGHT:
                    direction = (0, 1)

        # Рух пакмена
        player_pos = move_player(player_pos, direction, maze)

        # Рух привидів
        for i, ghost in enumerate(ghosts):
            path = bfs(maze, ghost, player_pos)
            if len(path) > 1:
                ghosts[i] = path[1]

        # Перевірка програшу
        if player_pos in ghosts:
            print("Game Over! You were caught by a ghost.")
            running = False

        # Перевірка виграшу
        if player_pos == finish_pos:
            print("Congratulations! You reached the finish!")
            running = False

        # Малювання
        screen.fill(WHITE)
        draw_maze(maze)
        draw_player(player_pos)
        draw_ghosts(ghosts)
        draw_finish(finish_pos)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
