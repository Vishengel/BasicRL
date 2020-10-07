from enum import Enum

class CellStates(Enum):
    EMPTY = 1
    AGENT = 2
    START = 3
    GOAL = 4
    TRAP = 5
    WALL = 6

class Actions(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Agent():
    def __init__(self, pos):
        self.pos = pos

class Cell():
    def __init__(self, pos, init_state):
        self.pos = pos
        self.state = init_state
        self.actions = []
        self.reward = 0

class Environment():

    def __init__(self, grid_file, rewards):
        print("Initializing grid")
        self.rewards = rewards
        self.char_to_state = {'C': CellStates.EMPTY, 'A': CellStates.AGENT, 'S': CellStates.START, 'G': CellStates.GOAL, 'T': CellStates.TRAP, 'W': CellStates.WALL}
        self.state_to_char = self.make_state_to_char()
        self.grid = self.load_grid_from_file(grid_file)
        self.init_actions()
        self.agent = None

    def make_state_to_char(self):
        state_to_char = {}

        for k, v in self.char_to_state.items():
            state_to_char[v] = k

        return state_to_char

    def load_grid_from_file(self, grid_file):
        grid = []

        try:
            gf = open(grid_file)

            for y, line in enumerate(gf):
                line = line.strip("\n")
                row = []

                for x, c in enumerate(line):
                    pos = (x, y)
                    cell = Cell(pos, self.char_to_state[c])

                    if cell.state in self.rewards.keys():
                        cell.reward = self.rewards[cell.state]

                    row.append(cell)

                    if c == self.state_to_char[CellStates.START]:
                        self.start = pos

                grid.append(row)

            gf.close()

        except FileNotFoundError as e:
            print(e)
            exit(0)

        return grid

    def init_actions(self):
        for row in self.grid:
            for cell in row:
                if not self.check_out_of_bounds(cell.pos):
                    neighbors = self.get_neighbors(cell.pos)
                    cell.actions = [dir.name for dir in neighbors]


    def check_out_of_bounds(self, pos):
        x = pos[0]
        y = pos[1]

        if x < 0 or x >= len(self.grid[0]) or y < 0 or y >= len(self.grid) or self.grid[y][x].state == CellStates.WALL:
            return True

        return False

    def get_neighbors(self, pos):
        neighbors = []

        # Up
        if not self.check_out_of_bounds((pos[0], pos[1]-1)):
            neighbors.append(Actions.UP)

        # Right
        if not self.check_out_of_bounds((pos[0]+1, pos[1])):
            neighbors.append(Actions.RIGHT)

        # Down
        if not self.check_out_of_bounds((pos[0], pos[1] + 1)):
            neighbors.append(Actions.DOWN)

        # Left
        if not self.check_out_of_bounds((pos[0]-1, pos[1])):
            neighbors.append(Actions.LEFT)

        return neighbors

    def get_cell(self, pos):
        x = pos[0]
        y = pos[1]

        if self.check_out_of_bounds(pos):
            print("Error: coordinates out of bounds")
            exit(0)

        return self.grid[y][x]

    def print_grid_state(self):
        for row in self.grid:
            for col in row:
                print(self.state_to_char[col.state], end="")
            print()
        print()

if __name__ == "__main__":
    grid_file = "grid.txt"
    grid = Environment(grid_file)