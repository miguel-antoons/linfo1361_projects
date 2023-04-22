from agent import AlphaBetaAgent
from pontu_state import PontuState
import time
from typing import *
# import time
# import queue as Q


class Successor:
    def __init__(self, action, state, evaluation):
        self.action = action
        self.state = state
        self.evaluation = evaluation
        self.children = []

    def __lt__(self, other_successor) -> bool:
        return self.evaluation < other_successor.evaluation

    def __le__(self, other_successor) -> bool:
        return self.evaluation <= other_successor.evaluation

    def __eq__(self, other_successor) -> bool:
        """self == obj."""
        return self.evaluation == other_successor.evaluation

    def __ne__(self, other_successor) -> bool:
        """self != obj."""
        return self.evaluation != other_successor.evaluation

    def __gt__(self, other_successor) -> bool:
        return self.evaluation > other_successor.evaluation

    def __ge__(self, other_successor) -> bool:
        return self.evaluation >= other_successor.evaluation

    def response(self) -> tuple:
        return self.action, self.state

    # def add_children(self, child) -> None:
    #     self.children.put(child)
    #
    # def get_children(self) -> Q.Queue:
    #     return self.children.get()
    #
    # def has_children(self) -> bool:
    #     return not self.children.empty()


def search(successor: Successor, player):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    player -- a concrete instance of class AlphaBetaPlayer
    """
    inf = float("inf")

    def max_value(current_successor: Successor, alpha, beta, depth):
        if player.cutoff(current_successor, depth):
            return current_successor.evaluation, None
        val = -inf
        return_successor = None

        if len(current_successor.children) == 0:
            children = player.successors(current_successor)
        else:
            children = current_successor.children

        for max_child in children:
            v, _ = min_value(max_child, alpha, beta, depth + 1)
            if v > val:
                val = v
                return_successor = max_child

                if v >= beta:
                    return v, max_child
                alpha = max(alpha, v)
        return val, return_successor

    def min_value(current_successor, alpha, beta, depth):
        if player.cutoff(current_successor, depth):
            return current_successor.evaluation, None
        val = inf
        return_successor = None

        if len(current_successor.children) == 0:
            children = player.successors(current_successor)
        else:
            children = current_successor.children

        for min_child in children:
            v, _ = max_value(min_child, alpha, beta, depth + 1)
            if v < val:
                val = v
                return_successor = min_child

                if v <= alpha:
                    return v, min_child
                beta = min(beta, v)
        return val, return_successor

    _, best_successor = max_value(successor, -inf, inf, 0)
    return best_successor


class BestNodes:
    def __init__(self, max_length: int, gt_first: bool = True):
        self.max_length = max_length
        self.gt_first = gt_first
        self.nodes = []
        self.max_value = float('-inf')
        self.min_value = float('inf')

    def insert(self, new_node: Successor) -> None:
        if self.max_value == self.min_value and self.max_value == new_node.evaluation:
            self.nodes.append(new_node)
            return
        elif len(self.nodes) < self.max_length:
            self.nodes.append(new_node)
        elif self.gt_first and new_node.evaluation <= self.min_value:
            return
        elif not self.gt_first and new_node.evaluation >= self.max_value:
            return
        else:
            self.__replace(new_node)
            self.__find_least()

        if new_node.evaluation > self.max_value:
            self.max_value = new_node.evaluation

        if new_node.evaluation < self.min_value:
            self.min_value = new_node.evaluation

    def get(self) -> list:
        self.nodes.sort(reverse=self.gt_first)

        return self.nodes

    def __replace(self, new_node: Successor) -> None:
        if self.gt_first:
            boundary = self.min_value
        else:
            boundary = self.max_value

        if boundary == new_node.evaluation:
            return

        for i in range(len(self.nodes)):
            if self.nodes[i].evaluation == boundary:
                self.nodes[i] = new_node
                return

    def __find_least(self) -> None:
        if self.gt_first:
            self.min_value = float('inf')
            for node in self.nodes:
                if node.evaluation < self.min_value:
                    self.min_value = node.evaluation
        else:
            self.max_value = float('-inf')
            for node in self.nodes:
                if node.evaluation > self.max_value:
                    self.max_value = node.evaluation


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """
    max_depth = 1
    game_time = 220 / 10
    time_left = None
    start_time = None
    n_round = -1
    link_weights_2 = (-6, -2, 1, 3, 4)
    link_weights = (-4, -3, 1, 4, 6)
    next_round_successors = []
    # steps = (6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    # index = 0

    def __init__(self):
        self.last_action = None
        self.last_hash = None

    def get_action(self, state: PontuState, last_action: tuple, time_left: int) -> tuple:
        self.n_round += 1
        print(f"Round {self.n_round}")
        self.max_depth = 2
        # self.last_hash = None
        self.time_left = time_left
        self.start_time = time.time()

        start_successor = self.__find_start_successor(state)

        # self.__find_starter()

        # if self.n_round == self.steps[self.index]:
        #     self.index += 1
        #     self.max_depth += 1

        return self.__get_best_action(state, start_successor)
        # self.__find_candidate_nodes(best_action, state.copy())

    def __find_start_successor(self, state: PontuState) -> Union[Successor, None]:
        for successor in self.next_round_successors:
            if successor.state.history[-1] == state.history[-1]:
                return successor

        return None

    def __get_best_action(self, state: PontuState, start_successor: Union[Successor, None]) -> tuple:
        best_action: Union[Successor, None] = None

        if start_successor is not None:
            first_successor = start_successor
        else:
            first_successor = Successor(None, state, self.evaluate(state))
        same_counter = 0

        while time.time() - self.start_time < self.game_time and same_counter < 5:
            # print(self.max_depth)
            self.max_depth += 1
            temp_action = search(first_successor, self)

            if time.time() - self.start_time < self.game_time:
                best_action = temp_action

            if best_action == temp_action:
                same_counter += 1
            else:
                same_counter = 0

        self.next_round_successors = best_action.children

        return best_action.action

    def successors(self, successor: Successor) -> list:
        """
        The successors function must return (or yield) a list of
        pairs (a, s) in which an is the action played to reach the
        state s.
        """
        # self.store_nodes(state)
        maximizing_player = True
        if successor.state.cur_player != self.id:
            maximizing_player = False

        successors = self.__get_worthy_children(successor.state, maximizing_player)
        successor.children = successors

        return successors

    def __get_worthy_children(self, state: PontuState, maximizing_player: bool) -> list:
        worthy_children = BestNodes(max_length=11, gt_first=maximizing_player)
        parent_enemy_bridges = 0

        # calculate number of enemy bridges for parent state
        for position in state.cur_pos[1 - state.cur_player]:
            parent_enemy_bridges += self.no_adj_bridges(position, state)

        # for every possible action
        for action in state.get_current_player_actions():
            # create a new state
            new_state = state.copy()
            new_state.apply_action(action)

            # calculate number of enemy bridges for new state
            no_enemy_bridges = 0
            for position in new_state.cur_pos[new_state.cur_player]:
                no_enemy_bridges += self.no_adj_bridges(position, new_state)

            if no_enemy_bridges < parent_enemy_bridges:
                worthy_children.insert(
                    Successor(action, new_state, self.evaluate(new_state))
                )

        return worthy_children.get()

    def cutoff(self, successor: Successor, depth: int) -> bool:
        """
        The cutoff function returns true if the alpha-beta/minimax
        search has to stop and false otherwise.
        """
        if successor.state.game_over():
            return True
        elif depth >= self.max_depth:
            return True
        elif time.time() - self.start_time >= self.game_time:
            return True

        return False

    def evaluate(self, state) -> int:
        evaluation = 0

        # score of own pawns
        for position in state.cur_pos[self.id]:
            no_escapes = self.__no_escape(position, state)
            evaluation += self.link_weights[no_escapes['escapes']]
            evaluation += self.link_weights_2[no_escapes['bridges']]

        # score of enemy pawns
        for position in state.cur_pos[1 - self.id]:
            no_escapes = self.__no_escape(position, state)
            evaluation -= self.link_weights[no_escapes['escapes']]
            evaluation -= self.link_weights_2[no_escapes['bridges']]

        return evaluation

    @staticmethod
    def no_adj_bridges(pos: tuple, state: PontuState) -> int:
        no_bridges = 0
        # Check west bridge
        if pos[0] >= 1 and state.h_bridges[pos[1]][pos[0] - 1]:
            no_bridges += 1
        # Check north bridge
        if pos[1] >= 1 and state.v_bridges[pos[1] - 1][pos[0]]:
            no_bridges += 1
        # Check east bridge
        if pos[0] < state.size - 1 and state.h_bridges[pos[1]][pos[0]]:
            no_bridges += 1
        # Check south bridge
        if pos[1] < state.size - 1 and state.v_bridges[pos[1]][pos[0]]:
            no_bridges += 1

        return no_bridges

    @staticmethod
    def __no_adj_pawns(pos: tuple, state: PontuState, player: int) -> int:
        no_pawns = 0
        # Check west island
        if pos[0] >= 1:
            for (x, y) in state.cur_pos[player]:
                if pos == (x + 1, y) and state.h_bridges[pos[1]][pos[0] - 1]:
                    no_pawns += 1
        # Check north island
        if pos[1] >= 1:
            for (x, y) in state.cur_pos[player]:
                if pos == (x, y + 1) and state.v_bridges[pos[1] - 1][pos[0]]:
                    no_pawns += 1
        # Check east island
        if pos[0] < state.size - 1:
            for (x, y) in state.cur_pos[player]:
                if pos == (x - 1, y) and state.h_bridges[pos[1]][pos[0]]:
                    no_pawns += 1
        # Check south island
        if pos[1] < state.size - 1:
            for (x, y) in state.cur_pos[player]:
                if pos == (x, y - 1) and state.v_bridges[pos[1]][pos[0]]:
                    no_pawns += 1

        return no_pawns

    def __no_escape(self, position: tuple, state: PontuState) -> dict:
        no_escape = {
            'bridges': self.no_adj_bridges(position, state),
            'al_pawns': self.__no_adj_pawns(position, state, self.id),
            'en_pawns': self.__no_adj_pawns(position, state, 1 - self.id)
        }
        no_escape['escapes'] = no_escape['bridges'] - no_escape['al_pawns'] - no_escape['en_pawns']
        return no_escape
