#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Auguste Burlats <auguste.burlats@uclouvain.be>"""
from search import *
import time


class AtomPlacement(Problem):
    already_visited = set()

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def successor(self, current_state):
        for first_edge, second_edge in current_state.edges:
            if current_state.sites[first_edge] != current_state.sites[second_edge]:
                new_state = current_state.__copy__()
                new_state.sites[first_edge], new_state.sites[second_edge] = new_state.sites[second_edge], new_state.sites[first_edge]

                if str(new_state.sites) not in self.already_visited:
                    yield None, new_state

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def value(self, current_state):
        result = 0
        for first_edge, second_edge in current_state.edges:
            result += current_state.energy_matrix[current_state.sites[first_edge]][current_state.sites[second_edge]]

        return result


class State:

    def __init__(self, n_sites, types, edges, energy_matrix, sites=None):
        self.k = len(types)
        self.types = types
        self.n_sites = n_sites
        self.n_edges = len(edges)
        self.edges = edges
        self.energy_matrix = energy_matrix
        if sites is None:
            self.sites = self.build_init()
        else:
            self.sites = sites

    # an init state building is provided here but you can change it at will
    def build_init(self):
        sites = []
        for atom_type, quantity in enumerate(self.types):
            for i in range(quantity):
                sites.append(atom_type)

        return sites

    def __str__(self):
        s = ''
        for v in self.sites:
            s += ' ' + str(v)
        return s

    def __copy__(self):
        return State(self.n_sites, self.types, self.edges, self.energy_matrix, self.sites.copy())


def read_instance(instance_file):
    file = open(instance_file)
    line = file.readline()
    n_sites = int(line.split(' ')[0])
    k = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    edges = []
    file.readline()

    n_types = [int(val) for val in file.readline().split(' ')]
    if sum(n_types) != n_sites:
        print('Invalid instance, wrong number of sites')
    file.readline()

    energy_matrix = []
    for i in range(k):
        energy_matrix.append([int(val) for val in file.readline().split(' ')])
    file.readline()

    for i in range(n_edges):
        edges.append([int(val) for val in file.readline().split(' ')])

    return n_sites, n_types, edges, energy_matrix


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100):
    current = LSNode(problem, problem.initial, 0)
    best = current
    no_steps = 0

    for step in range(limit):
        max_successor = None
        for successor in current.expand():
            if max_successor is None:
                max_successor = successor
            if successor.value() < max_successor.value():
                max_successor = successor

        current = max_successor
        problem.already_visited.add(str(current.state.sites))

        if current.value() < best.value():
            best = current
            no_steps = step

    return best, no_steps


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance("instances/i10.txt")
    init_state = State(info[0], info[1], info[2], info[3])
    ap_problem = AtomPlacement(init_state)
    # print('Initial value = ', ap_problem.value(init_state))
    step_limit = 200
    start_time = time.time()
    node, nb_steps = maxvalue(ap_problem)
    print(f"Time taken : {time.time() - start_time} seconds")
    state = node.state
    print(f"Node value : {-ap_problem.value(state)}")
    print(f"Number of steps : {nb_steps}")
    # print('End value = ', node.value())
