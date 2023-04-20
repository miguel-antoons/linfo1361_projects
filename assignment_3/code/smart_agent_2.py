from agent import AlphaBetaAgent
import minimax
import math
from smart_agent import MyAgent as MyAgent2


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """
    max_depth = 3
    n_round = -1
    steps = (4, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    index = 0

    """
    This is the skeleton of an agent to play the Tak game.
    """

    def __init__(self):
        self.last_action = None

    def get_action(self, state, last_action, time_left):
        self.n_round += 1
        print("Round: " + str(self.n_round))
        if math.floor(self.n_round / self.steps[self.index]) == 1:
            self.index += 1
            self.max_depth += 1

        self.last_action = last_action
        # self.time_left = time_left
        # self.initial_time = time.time_ns()

        return minimax.search(state, self)

    """
    TODO : sort results based on evaluation in order to improve speed?
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        parent_enemy_bridges = 0
        if state.cur_player == self.id:
            for position in state.cur_pos[1 - self.id]:
                parent_enemy_bridges += MyAgent2.no_adj_bridges(position, state)

        for action in state.get_current_player_actions():
            new_state = state.copy()
            new_state.apply_action(action)

            if new_state.cur_player == self.id:
                yield action, new_state
            else:
                no_enemy_bridges = 0
                for position in new_state.cur_pos[1 - self.id]:
                    no_enemy_bridges += MyAgent2.no_adj_bridges(position, new_state)

                if no_enemy_bridges < parent_enemy_bridges:
                    yield action, new_state

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        # time.sleep(0.1)
                    
        # if self.max_depth > 50 and (time.time_ns() - self.initial_time) > 300000:
        #     self.max_depth = depth
        #     print("Cutoff at depth: " + str(depth))

        # no_enemy_bridges = 0
        # for position in state.cur_pos[1 - self.id]:
        #     no_enemy_bridges += self.__no_adj_bridges(position, state)

        # print(f"DEPTH : {depth}, CURRENT ENEMY BRIDGES : {no_enemy_bridges}, ENEMY BRIDGES : {self.enemy_bridges}")

        if state.game_over():
            return True
        elif depth >= self.max_depth:
            return True
        # elif state.cur_player != self.id:
        #     no_enemy_bridges = 0
        #     for position in state.cur_pos[1 - self.id]:
        #         no_enemy_bridges += self.__no_adj_bridges(position, state)
        #     if no_enemy_bridges >= self.enemy_bridges:
        #         return True

        # if state.cur_player == self.id:
        #     self.enemy_bridges = 0
        #     for position in state.cur_pos[1 - self.id]:
        #         self.enemy_bridges += self.__no_adj_bridges(position, state)

        return False

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        # if not state.game_over() and len(state.history) < self.max_depth + self.n_round - 1:
        #     # print("HELLO")
        #     return -100
        evaluation = 0
        for position in state.cur_pos[self.id]:
            evaluation += MyAgent2.no_adj_bridges(position, state)
            # evaluation -= self.__no_adj_pawns(position, state, self.id)

        for position in state.cur_pos[1 - self.id]:
            evaluation -= MyAgent2.no_adj_bridges(position, state) if MyAgent2.no_adj_bridges(position, state) > 0 else -3
            # evaluation += self.__no_adj_pawns(position, state, 1 - self.id)

        # for pawn in range(3):
        #     bridges = state.adj_bridges(1 - self.id, pawn)
        #     for bridge in bridges:
        #         if bridges[bridge] is False:
        #             evaluation += 1

        return evaluation
