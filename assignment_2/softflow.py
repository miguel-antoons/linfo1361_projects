from search import *
#from aima_python3.search import *
from copy import deepcopy
import sys
#from time import sleep

#################
# Problem class #
#################


class SoftFlow(Problem):
    already_find = set()
    previous_state = set()

    def __init__(self, initial):
        goal = dict()
        start = dict()

        for row in initial.grid:
            for cell in row:
                if 48 <= ord(cell) <= 57:
                    goal[ord(cell) % 48] = []
                    goal[ord(cell) % 48].append((initial.grid.index(row), row.index(cell)))
                    goal[ord(cell) % 48].append((initial.grid.index(row) - 1, row.index(cell)))
                    goal[ord(cell) % 48].append((initial.grid.index(row) + 1, row.index(cell)))
                    goal[ord(cell) % 48].append((initial.grid.index(row), row.index(cell) - 1))
                    goal[ord(cell) % 48].append((initial.grid.index(row), row.index(cell) + 1))
                elif 97 <= ord(cell) <= 106:
                    start[ord(cell) % 97] = (initial.grid.index(row), row.index(cell))

        initial.current_positions = start
        super().__init__(initial, goal)

    def actions(self, state):
        for current in self.goal.keys():
            current_row = state.current_positions[current][0]
            current_col = state.current_positions[current][1]

            if state.current_positions[current] not in self.goal[current]:
                # up
                if current_row - 1 >= 0 and state.grid[current_row - 1][current_col] == " ":
                    yield (current_row - 1, current_col, current)
                # down
                if current_row + 1 < state.nbr and state.grid[current_row + 1][current_col] == " ":
                    yield (current_row + 1, current_col, current)
                # left
                if current_col - 1 >= 0 and state.grid[current_row][current_col - 1] == " ":
                    yield (current_row, current_col - 1, current)
                # right
                if current_col + 1 < state.nbc and state.grid[current_row][current_col + 1] == " ":
                    yield (current_row, current_col + 1, current)

    def result(self, state, action):
        new_state = deepcopy(state)

        current_row = state.current_positions[action[2]][0]
        current_col = state.current_positions[action[2]][1]

        letter = new_state.grid[current_row][current_col]
        new_state.grid[current_row][current_col] = str(action[2])
        new_state.current_positions[action[2]] = (action[0], action[1])

        if (action[0], action[1]) not in self.goal[action[2]]:
            new_state.grid[action[0]][action[1]] = letter
        else:
            new_state.grid[action[0]][action[1]] = str(action[2])

        return new_state

    def goal_test(self, state):
        for key in self.goal.keys():
            if state.current_positions[key] not in self.goal[key]:
                return False

        return True

    def h(self, node):
        h = 0

        for key in self.goal.keys():
            t = (
                abs(self.goal[key][0][0] - node.state.current_positions[key][0])
                + abs(self.goal[key][0][1] - node.state.current_positions[key][1])
            )
            if t <= 0:
                h -= 3
            else:
                h += t

        return h

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()

        state = State.from_string(''.join(lines))
        return SoftFlow(state)


###############
# State class #
###############
class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.current_positions = dict()

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        return self.current_positions == other_state.current_positions

    def __hash__(self):
        return hash(str(self.current_positions))

    def __lt__(self, other):
        return hash(self) < hash(other)

    def from_string(string):
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))


# Launch the search
problem = SoftFlow.load(sys.argv[1])

node = astar_search(problem)

# example of print
path = node.path()

print('Number of moves: ', str(node.depth))
for n in path:
    # assuming that the _str_ function of state outputs the correct format
    print(n.state)
    print()
