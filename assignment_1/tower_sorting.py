#!/usr/bin/env python
"""
Name of the author(s):
- Auguste Burlats <auguste.burlats@uclouvain.be>
"""
import time
import sys
from copy import deepcopy
#from search import *
from aima_python3.search import *


#################
# Problem class #
#################
class TowerSorting(Problem):
    def __init__(self, initial_state):
        super().__init__(initial_state)
        self.hashmap = set()

    def actions(self, state):
        # for each tower (source), check if there is at least one disc
        for source in range(state.number):
            if len(state.grid[source]) > 0:
                # for each possible destination
                for dest in range(state.number):
                    # if the action involves a different source and destination
                    # and the destination is not full
                    if source != dest and (len(state.grid[dest]) < state.size):
                        # if the resulting grid is not yet present in the
                        # hashmap, yield the action
                        if hash(self.__intern_result(state, (source, dest))) not in self.hashmap:
                            yield (source, dest)

    def __intern_result(self, state, action):
        # copy the state
        new_state = deepcopy(state)
        # move the disc from the source to the destination
        new_state.grid[action[1]].append(new_state.grid[action[0]].pop())
        # return the new state
        return new_state

    def result(self, state, action):
        new_state = self.__intern_result(state, action)
        # update the move
        new_state.move = f"{action[0]}-{action[1]}"
        # Add the new state to the hashmap
        self.hashmap.add(hash(new_state))
        # return the new state
        return new_state

    def goal_test(self, state):
        # for each tower in the grid verify that all the colors are the same
        for tower in state.grid:
            if len(tower) == state.size:
                for i in range(state.size - 1):
                    if tower[i] != tower[i + 1]:
                        return False
            # if there is a tower that is not yet at its full height, return
            # False
            elif len(tower) > 0:
                return False

        return True


###############
# State class #
###############
class State:
    def __init__(self, number, size, grid, move="Init"):
        self.number = number
        self.size = size
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    def __eq__(self, other):
        return self.grid == other.grid

    def __hash__(self):
        final = 0

        for i in self.grid:
            final += hash(str(i))

        return final


######################
# Auxiliary function #
######################
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)]
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    for tower in initial_grid:
        tower.reverse()

    return number_tower, size_tower, initial_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)

    init_state = State(number, size, initial_grid, "Init")
    problem = TowerSorting(init_state)
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct
        # format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
