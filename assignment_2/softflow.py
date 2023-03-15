from search import *
# from aima_python3.search import *
from copy import deepcopy
import sys
# import time

#################
# Problem class #
#################


class SoftFlow(Problem):

    def __init__(self, initial):
        goal = dict()
        start = dict()
        self.visited = set()
        self.tot_goals = 0

        for row in initial.grid:
            for cell in row:
                if 48 <= ord(cell) <= 57:
                    # add all the possible positions for the goal to the array
                    goal[ord(cell) % 48] = []
                    goal[ord(cell) % 48].append((initial.grid.index(row) - 1, row.index(cell)))
                    goal[ord(cell) % 48].append((initial.grid.index(row) + 1, row.index(cell)))
                    goal[ord(cell) % 48].append((initial.grid.index(row), row.index(cell) - 1))
                    goal[ord(cell) % 48].append((initial.grid.index(row), row.index(cell) + 1))
                    goal[ord(cell) % 48].append((initial.grid.index(row), row.index(cell)))
                    self.tot_goals += 1
                elif 97 <= ord(cell) <= 106:
                    start[ord(cell) % 97] = (initial.grid.index(row), row.index(cell))

        initial.current_positions = start
        super().__init__(initial, goal)

    def actions(self, state):
        for current in self.goal.keys():
            current_row = state.current_positions[current][0]
            current_col = state.current_positions[current][1]

            # check if a goal ha not already been reached before making an action on that cable
            if state.current_positions[current] not in self.goal[current]:
                # up move
                if current_row - 1 >= 0 and state.grid[current_row - 1][current_col] == " ":
                    if self.__intern_result(state, (current_row - 1, current_col, current)) not in self.visited:
                        yield (current_row - 1, current_col, current)
                # left move
                if current_col - 1 >= 0 and state.grid[current_row][current_col - 1] == " ":
                    if self.__intern_result(state, (current_row, current_col - 1, current)) not in self.visited:
                        yield (current_row, current_col - 1, current)
                # down move
                if current_row + 1 < state.nbr and state.grid[current_row + 1][current_col] == " ":
                    if self.__intern_result(state, (current_row + 1, current_col, current)) not in self.visited:
                        yield (current_row + 1, current_col, current)
                # right move
                if current_col + 1 < state.nbc and state.grid[current_row][current_col + 1] == " ":
                    if self.__intern_result(state, (current_row, current_col + 1, current)) not in self.visited:
                        yield (current_row, current_col + 1, current)

    def __intern_result(self, state, action):
        # calculate the impact of a move on an existing state and return the new state hash
        new_state = deepcopy(state)
        new_state.current_positions[action[2]] = (action[0], action[1])
        return hash(new_state)

    def result(self, state, action):
        new_state = deepcopy(state)

        current_row = state.current_positions[action[2]][0]
        current_col = state.current_positions[action[2]][1]

        # retain the letter to be user
        letter = new_state.grid[current_row][current_col]
        # apply the action on the grid and update the current position of the cable
        new_state.grid[current_row][current_col] = str(action[2])
        new_state.current_positions[action[2]] = (action[0], action[1])

        # if the goal has not been reached, put the letter back on the grid
        if (action[0], action[1]) not in self.goal[action[2]]:
            new_state.grid[action[0]][action[1]] = letter
        # else, remove the letter from the grid and increment the number of goals reached
        else:
            new_state.grid[action[0]][action[1]] = str(action[2])
            new_state.n_goals += 1

        # add the new state to the visited set
        self.visited.add(hash(new_state))

        return new_state

    def goal_test(self, state):
        # returns True if all the goals are reached
        return self.tot_goals == state.n_goals

    def h(self, node):
        # calculate the manhattan distance between the current position of the cable and the goal
        # do this for all the cables and sum the results
        h = 0

        for key in self.goal.keys():
            h += (
                abs(self.goal[key][-1][0] - node.state.current_positions[key][0])
                + abs(self.goal[key][-1][1] - node.state.current_positions[key][1])
            )

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
        self.current_positions = dict() # current position of each cable
        self.n_goals = 0 # number of goals reached

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        return self.current_positions == other_state.current_positions

    def __hash__(self):
        return hash(str(self.current_positions))

    def __lt__(self, other):
        return self.n_goals > other.n_goals

    def from_string(string):
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))


# Launch the search
problem = SoftFlow.load(sys.argv[1])

# start_timer = time.perf_counter()
node = astar_search(problem)
# end_timer = time.perf_counter()

# example of print
path = node.path()

# print("* Execution time:\t", str(end_timer - start_timer))
print('Number of moves: ', str(node.depth))
for n in path:
    # assuming that the _str_ function of state outputs the correct format
    print(n.state)
    print()
