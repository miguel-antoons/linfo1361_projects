from agent import AlphaBetaAgent
import minimax


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """

    """
    This is the skeleton of an agent to play the Tak game.
    """
    def get_action(self, state, last_action, time_left):
        self.last_action = last_action
        self.time_left = time_left
        return minimax.search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        actions = state.get_current_player_actions()
        for action in actions:
            new_state = state.copy()
            new_state.apply_action(action)
            yield action, new_state
        

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        if state.game_over():
            return True
        if depth == 1:
            return True
        return False

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        number = 0
        for pawn in range(3):
            bridges = state.adj_bridges(1 - self.id, pawn)
            for bridge in bridges:
                if bridges[bridge] == False:
                    number += 1
                    
        return number