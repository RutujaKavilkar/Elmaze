from typing import Tuple, List, Dict
import heapq

Point = Tuple[int, int]


class Grid:
    def __init__(self, width: float, height: float, resolution: float):
        self.resolution = resolution
        self.cols = int(width / resolution)
        self.rows = int(height / resolution)
        self.blocked = set()

    def to_grid(self, x: float, y: float) -> Point:
        return (int(x / self.resolution), int(y / self.resolution))

    def to_world(self, gx: int, gy: int):
        return (gx * self.resolution, gy * self.resolution)

    def in_bounds(self, node: Point) -> bool:
        x, y = node
        return 0 <= x < self.cols and 0 <= y < self.rows

    def is_blocked(self, node: Point) -> bool:
        return node in self.blocked

    def neighbors(self, node: Point):
        x, y = node

        directions = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (1, 1), (-1, -1),
            (1, -1), (-1, 1),
        ]

        for dx, dy in directions:
            nxt = (x + dx, y + dy)
            if self.in_bounds(nxt) and not self.is_blocked(nxt):
                yield nxt


# -------------------------
# Helpers
# -------------------------
def heuristic(a: Point, b: Point):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def direction(a: Point, b: Point):
    return (b[0] - a[0], b[1] - a[1])


# -------------------------
# A* Algorithm (Improved)
# -------------------------
def a_star(grid: Grid, start: Point, goal: Point):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from: Dict[Point, Point] = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in grid.neighbors(current):

            # diagonal cost
            step_cost = 1.4 if (
                abs(neighbor[0] - current[0]) == 1 and
                abs(neighbor[1] - current[1]) == 1
            ) else 1

            # turn penalty
            turn_penalty = 0
            if current in came_from:
                prev = came_from[current]
                if direction(prev, current) != direction(current, neighbor):
                    turn_penalty = 0.3

            tentative = g_score[current] + step_cost + turn_penalty

            if neighbor not in g_score or tentative < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f = tentative + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    return None


# -------------------------
# Blocking
# -------------------------
def block_pads(grid: Grid, pads: List[Tuple[float, float]], radius=0):
    for x, y in pads:
        gx, gy = grid.to_grid(x, y)

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                node = (gx + dx, gy + dy)
                if grid.in_bounds(node):
                    grid.blocked.add(node)


# -------------------------
# Convert Path → Traces
# -------------------------
def path_to_traces(grid: Grid, path: List[Point]):
    traces = []

    for i in range(len(path) - 1):
        x1, y1 = grid.to_world(*path[i])
        x2, y2 = grid.to_world(*path[i + 1])
        traces.append(((x1, y1), (x2, y2)))

    return traces