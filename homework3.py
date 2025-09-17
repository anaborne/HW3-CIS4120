############################################################
# CIS 521: Homework 3
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
from queue import PriorityQueue
import math

############################################################

student_name = "Immanuel Anaborne"

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board = []
    num = 1
    for r in range(rows):
        row = []
        for c in range(cols):
            if r == rows - 1 and c == cols - 1:
                row.append(0)
            else:
                row.append(num)
                num += 1
        board.append(row)
    return TilePuzzle(board)


class TilePuzzle(object):
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0
        self.empty_tile = self.find_empty_tile()

    def find_empty_tile(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    return (r, c)
        return None

    def get_board(self):
        return [row[:] for row in self.board]

    def perform_move(self, direction):
        match_direction = self.match_direction(direction)
        if not match_direction:
            return False
        dr, dc = match_direction
        er, ec = self.empty_tile
        new_r, new_c = er + dr, ec + dc
        if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
            self.board[er][ec], self.board[new_r][new_c] = (
                self.board[new_r][new_c],
                self.board[er][ec],
            )
            self.empty_tile = (new_r, new_c)
            return True
        return False

    def match_direction(self, direction):
        if direction == "up":
            return -1, 0
        elif direction == "down":
            return 1, 0
        elif direction == "left":
            return 0, -1
        elif direction == "right":
            return 0, 1
        else:
            raise ValueError(f"Unknown direction: {direction}")

    def scramble(self, num_moves):
        directions = ["up", "down", "left", "right"]
        for _ in range(num_moves):
            possible_moves = []
            for direction in directions:
                dr, dc = self.match_direction(direction)
                er, ec = self.empty_tile
                new_r, new_c = er + dr, ec + dc
                if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                    possible_moves.append(direction)
            if possible_moves:
                self.perform_move(random.choice(possible_moves))

    def is_solved(self):
        expected = [
            [
                (r * self.cols + c + 1) % (self.rows * self.cols)
                for c in range(self.cols)
            ]
            for r in range(self.rows)
        ]
        return self.board == expected

    def copy(self):
        new_board = [row[:] for row in self.board]
        return TilePuzzle(new_board)

    def successors(self):
        directions = ["up", "down", "left", "right"]
        for direction in directions:
            dr_dc = self.match_direction(direction)
            if not isinstance(dr_dc, tuple):
                continue
            dr, dc = dr_dc
            er, ec = self.empty_tile
            new_r, new_c = er + dr, ec + dc
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                new_puzzle = self.copy()
                new_puzzle.perform_move(direction)
                yield (direction, new_puzzle)

    # Required
    def find_solutions_iddfs(self):
        def iddfs_collect(puzzle, limit, moves, visited, results):
            board_tuple = tuple(tuple(row) for row in puzzle.board)
            if board_tuple in visited:
                return
            if puzzle.is_solved():
                results.append(moves)
                return
            if limit == 0:
                return
            visited.add(board_tuple)
            for direction, new_puzzle in puzzle.successors():
                iddfs_collect(
                    new_puzzle,
                    limit - 1,
                    moves + [direction],
                    visited,
                    results,
                )
            visited.remove(board_tuple)

        depth = 0
        while True:
            results = []
            iddfs_collect(self, depth, [], set(), results)
            if results:
                for sol in results:
                    yield sol
                return
            depth += 1

    # Required
    def find_solution_a_star(self):

        def manhattan(board):
            dist = 0
            for r in range(self.rows):
                for c in range(self.cols):
                    val = board[r][c]
                    if val == 0:
                        continue
                    goal_r = (val - 1) // self.cols
                    goal_c = (val - 1) % self.cols
                    dist += abs(r - goal_r) + abs(c - goal_c)
            return dist

        start_board = tuple(tuple(row) for row in self.board)
        frontier = PriorityQueue()

        frontier.put((manhattan(self.board), 0, [], start_board, self.copy()))
        visited = set()
        visited.add(start_board)

        while not frontier.empty():
            priority, cost, path, board_tuple, puzzle = frontier.get()
            if puzzle.is_solved():
                return path
            for direction, new_puzzle in puzzle.successors():
                new_board_tuple = tuple(tuple(row) for row in new_puzzle.board)
                if new_board_tuple in visited:
                    continue
                visited.add(new_board_tuple)
                g = cost + 1
                h = manhattan(new_puzzle.board)
                frontier.put(
                    (g + h, g, path + [direction], new_board_tuple, new_puzzle)
                )
        return None


############################################################
# Section 2: Grid Navigation
############################################################


def find_path(start, goal, scene):

    rows = len(scene)
    cols = len(scene[0]) if rows > 0 else 0

    def in_bounds(p):
        r, c = p
        return 0 <= r < rows and 0 <= c < cols

    if not in_bounds(start) or not in_bounds(goal):
        return None
    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None
    if start == goal:
        return [start]

    neighbors = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    ]

    def euclid(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    frontier = PriorityQueue()
    counter = 0
    g_cost = {start: 0.0}
    came_from = {}

    frontier.put((euclid(start, goal), 0.0, counter, start))

    while not frontier.empty():
        f, g, _, current = frontier.get()

        if g > g_cost.get(current, float("inf")) + 1e-12:
            continue

        if current == goal:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path.reverse()
            return path

        for dr, dc in neighbors:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            if not in_bounds(neighbor):
                continue
            if scene[nr][nc]:
                continue

            step_cost = math.hypot(dr, dc)
            tentative_g = g + step_cost

            if tentative_g + 1e-12 < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = tentative_g
                came_from[neighbor] = current
                counter += 1
                frontier.put(
                    (
                        tentative_g + euclid(neighbor, goal),
                        tentative_g,
                        counter,
                        neighbor,
                    )
                )

    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def solve_distinct_disks(length, n):
    if n > length or n <= 0 or length <= 0:
        return None

    start = tuple((i + 1) if i < n else 0 for i in range(length))

    goal_pos = {k: length - k for k in range(1, n + 1)}
    goal = tuple(
        (n - (i - (length - n))) if i >= length - n else 0
        for i in range(length)
    )
    if start == goal:
        return []

    def heuristic(state):
        h = 0
        for idx, val in enumerate(state):
            if val == 0:
                continue
            target = goal_pos[val]
            dist = abs(idx - target)
            h += (dist + 1) // 2
        return h

    def successors(state):
        for i, v in enumerate(state):
            if v == 0:
                continue
            for j in (i - 1, i + 1):
                if 0 <= j < length and state[j] == 0:
                    new = list(state)
                    new[j], new[i] = new[i], 0
                    yield (i, j), tuple(new)
            for j, mid in ((i - 2, i - 1), (i + 2, i + 1)):
                if 0 <= j < length and state[j] == 0 and state[mid] != 0:
                    new = list(state)
                    new[j], new[i] = new[i], 0
                    yield (i, j), tuple(new)

    frontier = PriorityQueue()
    counter = 0
    g_cost = {start: 0}
    frontier.put((heuristic(start), 0, counter, start, []))
    counter += 1

    while not frontier.empty():
        f, g, _, state, path = frontier.get()
        if state == goal:
            return path
        if g > g_cost.get(state, float("inf")) + 1e-12:
            continue
        for move, succ in successors(state):
            ng = g + 1
            if ng + 1e-12 < g_cost.get(succ, float("inf")):
                g_cost[succ] = ng
                h = heuristic(succ)
                counter += 1
                frontier.put((ng + h, ng, counter, succ, path + [move]))
    return None


############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
10
"""

feedback_question_2 = """
It was difficult debugging subtle logic errors \
in the A* algorithm implementation. I had some trouble figuring out \
the path finding, especially with the priority queue.
"""

feedback_question_3 = """
I liked that the assignment provided a hands-on opportunity to implement \
and visualize classic search algorithms. The GUI components made it more  \
interactive and helped with debugging.
"""
