from agent import AlphaBetaAgent
import minimax
import math


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """

    """
    This is the skeleton of an agent to play the Tak game.
    """
    def get_action(self, state, last_action, time_left):
        self.max_score = -math.inf
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
        evaluation = self.evaluate(state)
        if depth > 5 or evaluation <= self.max_score or state.game_over():
            return True

        self.max_score = max(self.max_score, evaluation)
        return False

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        evaluation = 0
        for pawn in range(3):
            bridges = state.adj_bridges(1 - self.id, pawn)
            for bridge in bridges:
                if bridges[bridge] is False:
                    evaluation += 1

        return evaluation
