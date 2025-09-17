############################################################
# CIS 521: Homework 3
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
from queue import PriorityQueue

############################################################

student_name = "Immanuel Anaborne"

############################################################
# Section 1: Tile Puzzle
############################################################

def __init__(self, board):
    self.board = board
    self.rows = len(board)
    self.cols = len(board[0]) if self.rows > 0 else 0
    self.empty_tile = self.find_empty_tile()




def get_board(self):
    return [row[:] for row in self.board]


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
            self.board[er][ec], self.board[new_r][new_c] = self.board[new_r][new_c], self.board[er][ec]
            self.empty_tile = (new_r, new_c)
            return True
        return False

    def match_direction(self, direction):
        match direction:
            case 'up':
                dr, dc = -1, 0
            case 'down':
                dr, dc = 1, 0
            case 'left':
                dr, dc = 0, -1
            case 'right':
                dr, dc = 0, 1
            case _:
                return False

    def scramble(self, num_moves):
        directions = ['up', 'down', 'left', 'right']
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
        expected = [[(r * self.cols + c + 1) % (self.rows * self.cols) for c in range(self.cols)] for r in range(self.rows)]
        return self.board == expected

    def copy(self):
        new_board = [row[:] for row in self.board]
        return TilePuzzle(new_board)

    def successors(self):
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            dr_dc = self.match_direction(direction)
            if not dr_dc:
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
        def iddfs_helper(puzzle, limit, moves, visited):
            if puzzle.is_solved():
                yield moves
                return
            if limit == 0:
                return
            board_tuple = tuple(tuple(row) for row in puzzle.board)
            visited.add(board_tuple)
            for direction, new_puzzle in puzzle.successors():
                new_board_tuple = tuple(tuple(row) for row in new_puzzle.board)
                if new_board_tuple not in visited:
                    yield from iddfs_helper(new_puzzle, limit - 1, moves + [direction], visited)
            visited.remove(board_tuple)

        depth = 0
        while True:
            visited = set()
            yield from iddfs_helper(self, depth, [], visited)
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
        # (priority, moves_so_far, board_tuple, puzzle_obj)
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
                frontier.put((g + h, g, path + [direction], new_board_tuple, new_puzzle))
        return None

############################################################
# Section 2: Grid Navigation
############################################################


def find_path(start, goal, scene):
    pass

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def solve_distinct_disks(length, n):
    pass

############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
