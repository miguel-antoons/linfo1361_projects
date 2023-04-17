from agent import AlphaBetaAgent
import minimax
from pontu_state import PontuState
# import time
import queue as Q


class Successor:
    def __init__(self, action, state, evaluation, reversed=True):
        self.action = action
        self.state = state
        self.evaluation = evaluation
        self.reversed = reversed
        self.children = Q.Queue()

    def __lt__(self, other_successor) -> bool:
        if self.reversed:
            return self.evaluation > other_successor.evaluation
        return self.evaluation < other_successor.evaluation

    def __le__(self, other_successor) -> bool:
        if self.reversed:
            return self.evaluation >= other_successor.evaluation
        return self.evaluation <= other_successor.evaluation

    def __eq__(self, other_successor) -> bool:
        """self == obj."""
        return self.evaluation == other_successor.evaluation

    def __ne__(self, other_successor) -> bool:
        """self != obj."""
        return self.evaluation != other_successor.evaluation

    def __gt__(self, other_successor) -> bool:
        if self.reversed:
            return self.evaluation < other_successor.evaluation
        return self.evaluation > other_successor.evaluation

    def __ge__(self, other_successor) -> bool:
        if reversed:
            return self.evaluation <= other_successor.evaluation
        return self.evaluation >= other_successor.evaluation

    def response(self) -> tuple:
        return self.action, self.state

    def add_children(self, child) -> None:
        self.children.put(child)

    def get_children(self) -> Q.Queue:
        return self.children.get()

    def has_children(self) -> bool:
        return not self.children.empty()


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """
    max_depth = 4
    n_round = -1
    link_weights = (-4, -3, 1, 4, 6)
    steps = (3, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    index = 0
    start_successors: list = []
    next_candidates = {}
    start_node: Successor = None

    """
    This is the skeleton of an agent to play the Tak game.
    """

    def __init__(self):
        self.last_action = None
        self.last_hash = None

    def get_action(self, state: PontuState, last_action: tuple, time_left: int) -> tuple:
        self.n_round += 1
        self.last_hash = None

        self.last_action = last_action
        self.__find_starter()

        if self.n_round == self.steps[self.index]:
            self.index += 1
            self.max_depth += 1

        best_action = minimax.search(state, self)
        self.__find_candidate_nodes(best_action, state.copy())
        return best_action

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state: PontuState) -> list:
        self.store_nodes(state)
        reversed = True
        if state.cur_player != self.id:
            reversed = False

        if self.start_node is not None and self.start_node.has_children():
            successors = self.start_node.get_children()
            print("HELLO")
        else:
            successors = self.__get_worthy_children(state, reversed)

        children = Q.Queue()
        if (len(state.history) == 2 and state.history[-1] != self.last_action) or (len(state.history) > 2 and ((state.cur_player == (1 - self.id) and state.history[-2] != self.last_action) or (state.cur_player == self.id and state.history[-1] != self.last_action))):
            self.next_candidates[self.last_hash][-1].add_children(children)

        counter = 0
        while not successors.empty() and counter < 10:
            if reversed:
                counter += 1
            temp = successors.get()

            if len(state.history) == 1 or (len(state.history) > 1 and state.history[-2] == self.last_action and state.cur_player == 1 - self.id):
                self.next_candidates[self.last_hash].append(temp)

            if (len(state.history) == 2 and state.history[-1] != self.last_action) or (len(state.history) > 2 and ((state.cur_player == (1 - self.id) and state.history[-2] != self.last_action) or (state.cur_player == self.id and state.history[-1] != self.last_action))):
                children.put(temp)

            yield temp.response()

    def __get_worthy_children(self, state: PontuState, reversed: bool) -> Q.PriorityQueue:
        worthy_children = Q.PriorityQueue()
        parent_enemy_bridges = 0

        # calculate number of enemy bridges for parent state
        for position in state.cur_pos[1 - state.cur_player]:
            parent_enemy_bridges += self.__no_adj_bridges(position, state)

        # for every possible action
        for action in state.get_current_player_actions():
            # create a new state
            new_state = state.copy()
            new_state.apply_action(action)

            # calculate number of enemy bridges for new state
            no_enemy_bridges = 0
            for position in new_state.cur_pos[new_state.cur_player]:
                no_enemy_bridges += self.__no_adj_bridges(position, new_state)

            if no_enemy_bridges < parent_enemy_bridges:
                worthy_children.put(
                    Successor(action, new_state, self.evaluate(new_state), reversed)
                )

        return worthy_children

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state: PontuState, depth: int) -> bool:
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
            evaluation += self.link_weights[no_escapes['bridges']]

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
            evaluation -= self.link_weights[no_escapes['bridges']]

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

    def __no_adj_bridges(self, pos: tuple, state: PontuState) -> int:
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

    def __no_adj_pawns(self, pos: tuple, state: PontuState, player: int) -> int:
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

    def __no_escape(self, position: tuple, state: PontuState) -> object:
        no_escape = {}
        no_escape['bridges'] = self.__no_adj_bridges(position, state)
        no_escape['al_pawns'] = self.__no_adj_pawns(position, state, self.id)
        no_escape['en_pawns'] = self.__no_adj_pawns(position, state, 1 - self.id)
        no_escape['escapes'] = no_escape['bridges'] - no_escape['al_pawns'] - no_escape['en_pawns']
        return no_escape

    def store_nodes(self, state: PontuState) -> bool:
        if len(state.history) == 1 or (len(state.history) > 1 and state.history[-2] == self.last_action and state.cur_player == 1 - self.id):
            self.last_hash = hash(str(state.history[-1]))
            self.next_candidates[self.last_hash] = []
            return True

        return False

    def __find_candidate_nodes(self, action: tuple, state: PontuState) -> None:
        if not self.next_candidates:
            return

        state.apply_action(action)
        self.start_successors = self.next_candidates[hash(str(state.history[-1]))]
        self.next_candidates = {}

    def __find_starter(self) -> None:
        self.start_node = None

        if len(self.start_successors) == 0:
            return

        for successor in self.start_successors:
            if successor.state.history[-1] == self.last_action:
                self.start_node = successor
                return

        self.start_successors = []
