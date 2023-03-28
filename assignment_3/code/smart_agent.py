from agent import AlphaBetaAgent
import minimax
import math


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """
    player_index = None

    """
    This is the skeleton of an agent to play the Tak game.
    """
    def get_action(self, state, last_action, time_left):
        if self.player_index is None:
            self.player_index = state.cur_player
        self.max_score = None
        self.last_action = last_action
        self.time_left = time_left
        return minimax.search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        for action in state.get_current_player_actions():
            new_state = state.copy()
            new_state.apply_action(action)
            yield (action, new_state)

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        # evaluation = self.evaluate(state)
        if state.game_over():
            return True
        # elif self.max_score is not None and evaluation <= self.max_score:
        #     return True
        elif depth > 2:
            return True

        return False

    def __no_adj_bridges(self, pos, state):
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

    def __no_adj_pawns(self, pos, state, player):
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

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        evaluation = 0
        for position in state.cur_pos[self.player_index]:
            evaluation += self.__no_adj_bridges(position, state)
            evaluation -= self.__no_adj_pawns(position, state, self.player_index)

        for position in state.cur_pos[1 - self.player_index]:
            evaluation -= self.__no_adj_bridges(position, state)
            evaluation += self.__no_adj_pawns(position, state, 1 - self.player_index)

        # for pawn in range(3):
        #     bridges = state.adj_bridges(1 - self.id, pawn)
        #     for bridge in bridges:
        #         if bridges[bridge] is False:
        #             evaluation += 1

        return evaluation
