from agent import AlphaBetaAgent
import minimax
from pontu_state import PontuState
# import time
# import queue as Q


class Successor:
    def __init__(self, action, state, evaluation):
        self.action = action
        self.state = state
        self.evaluation = evaluation
        # self.children = Q.Queue()

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
        else:
            self.__replace(new_node)
            self.__find_least()

        if new_node.evaluation > self.max_value:
            self.max_value = new_node.evaluation

        if new_node.evaluation < self.min_value:
            self.min_value = new_node.evaluation

    def get(self) -> list:
        self.nodes.sort(reverse=self.gt_first)

        responses = []
        for node in self.nodes:
            responses.append(node.response())

        return responses

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
    max_depth = 4
    n_round = -1
    link_weights_2 = (-6, -2, 1, 3, 4)
    link_weights = (-4, -3, 1, 4, 6)
    steps = (2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    index = 0
    # start_successors: list = []
    # next_candidates = {}
    # start_node: Successor = None

    def __init__(self):
        self.last_action = None
        self.last_hash = None

    def get_action(self, state: PontuState, last_action: tuple, time_left: int) -> tuple:
        self.n_round += 1
        self.last_hash = None

        self.last_action = last_action
        # self.__find_starter()

        if self.n_round == self.steps[self.index]:
            self.index += 1
            self.max_depth += 1

        best_action = minimax.search(state, self)
        # self.__find_candidate_nodes(best_action, state.copy())
        return best_action

    def successors(self, state: PontuState) -> list:
        """
        The successors function must return (or yield) a list of
        pairs (a, s) in which an is the action played to reach the
        state s.
        """
        # self.store_nodes(state)
        maximizing_player = True
        if state.cur_player != self.id:
            maximizing_player = False

        successors = self.__get_worthy_children(state, maximizing_player)

        return successors

    def __get_worthy_children(self, state: PontuState, maximizing_player: bool) -> list:
        worthy_children = BestNodes(max_length=15, gt_first=maximizing_player)
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

    def cutoff(self, state: PontuState, depth: int) -> bool:
        """
        The cutoff function returns true if the alpha-beta/minimax
        search has to stop and false otherwise.
        """
        if state.game_over():
            return True
        elif depth >= self.max_depth:
            return True

        return False

    def evaluate(self, state) -> int:
        evaluation = 0

        # score of own pawns
        for position in state.cur_pos[self.id]:
            no_escapes = self.__no_escape(position, state)
            evaluation += self.link_weights[no_escapes['escapes']] * 100
            evaluation += self.link_weights_2[no_escapes['bridges']]

            # if no_escapes['bridges'] == 0:
            #     evaluation -= 10
            # if no_escapes['escapes'] == 0:
            #     evaluation -= 5
            # elif no_escapes['escapes'] == 1:
            #     evaluation -= 5
            # elif no_escapes['escapes'] == 4:
            #     evaluation += 2
            # elif no_escapes['escapes'] == 2:
            #     if no_escapes['en_pawns'] == 0:
            #         evaluation -= 1
            #     # elif no_escapes['en_pawns'] == 1:
            #     #     evaluation += 0
            #     # elif no_escapes['en_pawns'] >= 2:
            #     #     evaluation += 2
            # else:
            #     if no_escapes['en_pawns'] == 1:
            #         evaluation += 3
            #     elif no_escapes['en_pawns'] == 0:
            #         evaluation += 1

        # score of enemy pawns
        for position in state.cur_pos[1 - self.id]:
            no_escapes = self.__no_escape(position, state)
            evaluation -= self.link_weights[no_escapes['escapes']] * 100
            evaluation -= self.link_weights_2[no_escapes['bridges']]

            # if no_escapes['bridges'] == 0:
            #     evaluation += 10
            # if no_escapes['escapes'] == 0:
            #     evaluation += 5
            # elif no_escapes['escapes'] == 1:
            #     evaluation += 5
            # elif no_escapes['escapes'] == 4:
            #     evaluation -= 2
            # elif no_escapes['escapes'] == 2:
            #     if no_escapes['al_pawns'] == 0:
            #         evaluation += 1
            #     # elif no_escapes['en_pawns'] == 1:
            #     #     evaluation -= 0
            #     # elif no_escapes['al_pawns'] >= 2:
            #     #     evaluation -= 2
            # else:
            #     if no_escapes['al_pawns'] == 1:
            #         evaluation -= 3
            #     elif no_escapes['al_pawns'] == 0:
            #         evaluation -= 1

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

    # def store_nodes(self, state: PontuState) -> bool:
    #     if len(state.history) == 1 or (
    #             len(state.history) > 1 and state.history[-2] == self.last_action and state.cur_player == 1 - self.id):
    #         self.last_hash = hash(str(state.history[-1]))
    #         self.next_candidates[self.last_hash] = []
    #         return True
    #
    #     return False
    #
    # def __find_candidate_nodes(self, action: tuple, state: PontuState) -> None:
    #     if not self.next_candidates:
    #         return
    #
    #     state.apply_action(action)
    #     self.start_successors = self.next_candidates[hash(str(state.history[-1]))]
    #     self.next_candidates = {}
    #
    # def __find_starter(self) -> None:
    #     self.start_node = None
    #
    #     if len(self.start_successors) == 0:
    #         return
    #
    #     for successor in self.start_successors:
    #         if successor.state.history[-1] == self.last_action:
    #             self.start_node = successor
    #             return
    #
    #     self.start_successors = []
