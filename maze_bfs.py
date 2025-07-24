import random
import time
import os
from collections import deque

WIDTH, HEIGHT = 50, 50

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy//2][x + dx//2] = 0
                carve(nx, ny)

    start_x = random.randrange(1, width, 2)
    start_y = random.randrange(1, height, 2)
    maze[start_y][start_x] = 0
    carve(start_x, start_y)
    return maze, (start_x, start_y)

def print_maze(maze, path=set(), frontier=set(), start=None, end=None):
    for y, row in enumerate(maze):
        line = ''
        for x, cell in enumerate(row):
            if (x,y) == start:
                line += 'S '
            elif (x,y) == end:
                line += 'E '
            elif (x,y) in path:
                line += '* '
            elif (x,y) in frontier:
                line += '? '
            elif cell == 1:
                line += '█ '
            else:
                line += '. '
        print(line)
    print()

def neighbors(pos, maze):
    x,y = pos
    for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
            if maze[ny][nx] == 0:
                yield (nx, ny)

def bfs(maze, start, end, delay=0.05):
    queue = deque()
    queue.append([start])
    visited = set([start])

    while queue:
        path = queue.popleft()
        current = path[-1]

        frontier = {p[-1] for p in queue}
        clear_console()
        print_maze(maze, set(path), frontier, start, end)
        time.sleep(delay)

        if current == end:
            return path

        for nxt in neighbors(current, maze):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(path + [nxt])
    return None

if __name__ == "__main__":
    maze, start = generate_maze(WIDTH, HEIGHT)
    free_cells = [(x,y) for y,row in enumerate(maze) for x,cell in enumerate(row) if cell == 0 and (x,y) != start]
    end = random.choice(free_cells)

    print("The size of the generated maze:", WIDTH, "x", HEIGHT)
    print("begin:", start, "end:", end)
    time.sleep(2)

    path = bfs(maze, start, end, delay=0.05)
    if path:
        clear_console()
        print_maze(maze, set(path), set(), start, end)
        print("找Find the path! Length:", len(path))
    else:
        print("no solution")
