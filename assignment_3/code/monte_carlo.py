from pontu_tools import *
from smart_agent import MyAgent as MyAgent2
import math
import csv


class Node:
    def __init__(self, parent, state: PontuState, step: int):
        self.parent = parent
        self.state: PontuState = state
        self.children: list = []
        self.n_visits: int = 0
        self.first_player_total_percentage: float = 0.0
        self.step = step

    def get_children(self):
        if self.state.game_over():
            return []

        if len(self.children) == 0:
            self.children = self.__calculate_children()

        return self.children

    def get_utc(self, c=1.5):
        return (
            (self.first_player_total_percentage / self.n_visits)
            + (c * math.sqrt(math.log(self.parent.n_visits) / self.n_visits))
        )

    def __calculate_children(self):
        children = []
        parent_enemy_bridges = 0

        # calculate number of enemy bridges for parent state
        for position in self.state.cur_pos[1 - self.state.cur_player]:
            parent_enemy_bridges += MyAgent2.no_adj_bridges(position, self.state)

        # for every possible action
        for action in self.state.get_current_player_actions():
            # create a new state
            new_state = self.state.copy()
            new_state.apply_action(action)

            # calculate number of enemy bridges for new state
            no_enemy_bridges = 0
            for position in new_state.cur_pos[new_state.cur_player]:
                no_enemy_bridges += MyAgent2.no_adj_bridges(position, new_state)

            if no_enemy_bridges < parent_enemy_bridges:
                children.append(Node(self, new_state, self.step + 1))

        return children


def play_game_2(game_n, initial_state):
    agent0 = "random_agent"
    agent1 = "random_agent"
    time_out = 900.0
    # first = '0'
    display_gui = False

    agent0 = getattr(__import__(agent0), 'MyAgent')()
    agent0.set_id(0)
    agent1 = getattr(__import__(agent1), 'MyAgent')()
    agent1.set_id(1)
    res = play_game(initial_state, [agent0.get_name(), agent1.get_name()], [agent0, agent1], time_out, display_gui)

    return res[0]


def simulate_game(initial_state: PontuState, no_reruns: int):
    no_wins = 0
    for i in range(no_reruns):
        if play_game_2(i, initial_state) == 0:
            no_wins += 1

    return (no_wins / no_reruns) * 100


def backpropagate(node: Node, win_percentage: float):
    node.n_visits += 1
    node.first_player_total_percentage += win_percentage

    if node.parent is not None:
        backpropagate(node.parent, win_percentage)


def monte_carlo():
    pass
