from agent import AlphaBetaAgent
import minimax
import math
import queue as Q


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """
    max_depth = 2
    n_round = -1
    steps = (2, 5, 8, 11, 13, 14, 15, 16, 17, 18, 19, 20)
    index = 0

    """
    This is the skeleton of an agent to play the Tak game.
    """
    def get_action(self, state, last_action, time_left):
        self.n_round += 1
        # DEBUG
        # if self.n_round > 0:
        #     raise Exception("History not empty")
        if self.n_round == self.steps[self.index]:
            self.index += 1
            self.max_depth += 1

        self.last_action = last_action

        return minimax.search(state, self)

    """
    TODO : sort results based on evaluation in order to improve speed?
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        reversed = True
        if state.cur_player != self.id:
            reversed = False

        first_choice = Q.PriorityQueue()
        # second_choice = Q.PriorityQueue()
        # third_choice = Q.PriorityQueue()
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

            # calculate number of bridges for new state
            bridges = 0
            for position in new_state.cur_pos[1 - new_state.cur_player]:
                bridges += self.__no_adj_bridges(position, new_state)

            if no_enemy_bridges < parent_enemy_bridges:
                # DEBUG
                # print("ACCEPTED")
                # print(new_state.cur_pos[self.id])
                # print(f"  H_BRIDGES : {new_state.h_bridges}")
                # print(f"  V_BRIDGES : {new_state.v_bridges}")
                # print(f"  NO_ENEMY_BRIDGES : {no_enemy_bridges}")
                # print(f"  PARENT_BRIDGES : {parent_enemy_bridges}")
                # print("\n")
                first_choice.put(
                    Successor(action, new_state, self.evaluate(new_state), reversed)
                )

        while not first_choice.empty():
            # choic = first_choice.get()
            # if state.cur_player == self.id and last_evaluation < choic.evaluation:
            #     print("    ALERT")

            # print(f"  CHOICE : {choic.response()}, {self.evaluate(choic.state)}")

            # last_evaluation = choic.evaluation
            # print(f"  CHOICE : {choic}")
            # breakpoint()
            yield first_choice.get().response()

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        if state.game_over():
            return True
        elif depth >= self.max_depth:
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

    def __no_escape(self, position, state):
        no_escape = {}
        no_escape['bridges'] = self.__no_adj_bridges(position, state)
        no_escape['al_pawns'] = self.__no_adj_pawns(position, state, self.id)
        no_escape['en_pawns'] = self.__no_adj_pawns(position, state, 1 - self.id)
        no_escape['escapes'] = no_escape['bridges'] - no_escape['al_pawns'] - no_escape['en_pawns']
        return no_escape

    def __no_adj_of_adj_bridges(self, adj_bridges, state, player):
        no_adj_of_adj = 0
        for adj_bridge in adj_bridges:
            if adj_bridge is True:
                if adj_bridge.key == 'NORTH':
                    no_adj_of_adj += self.__no_adj_bridges((adj_bridge.x, adj_bridge.y - 1), state)

                if adj_bridge.key == 'SOUTH':
                    no_adj_of_adj += self.__no_adj_bridges((adj_bridge.x, adj_bridge.y + 1), state)

                if adj_bridge.key == 'EAST':
                    no_adj_of_adj += self.__no_adj_bridges((adj_bridge.x + 1, adj_bridge.y), state)

                if adj_bridge.key == 'WEST':
                    no_adj_of_adj += self.__no_adj_bridges((adj_bridge.x - 1, adj_bridge.y), state)

        return no_adj_of_adj

    def evaluate(self, state):
        evaluation = 0
        #(f"LAST ACTION : {state.history[-1]}")

        # score of own pawns
        for position in state.cur_pos[self.id]:
            no_escapes = self.__no_escape(position, state)
            # DEBUG
            # print(f"{position} bridges : {no_escapes['bridges']}")
            # print(f"{position} al_pawns : {no_escapes['al_pawns']}")
            # print(f"{position} en_pawns : {no_escapes['en_pawns']}")
            # print(f"{position} escapes : {no_escapes['escapes']}")

            if no_escapes['bridges'] == 0:
                evaluation -= 5
            elif no_escapes['escapes'] == 0:
                evaluation -= 3
            elif no_escapes['escapes'] == 1:
                evaluation -= 2
            elif no_escapes['escapes'] == 4:
                evaluation += 2
            elif no_escapes['escapes'] == 2:
                if no_escapes['en_pawns'] == 0:
                    evaluation -= 1
                # elif no_escapes['en_pawns'] == 1:
                #     evaluation += 0
                elif no_escapes['en_pawns'] == 2:
                    evaluation += 2
            else:
                if no_escapes['en_pawns'] == 1:
                    evaluation += 3
                elif no_escapes['en_pawns'] == 0:
                    evaluation += 1

            # DEBUG
            # print("KING EVALUATION: " + str(evaluation))
            # print('\n')

        # score of enemy pawns
        for position in state.cur_pos[1 - self.id]:
            no_escapes = self.__no_escape(position, state)
            # DEBUG
            # print(f"{position} bridges : {no_escapes['bridges']}")
            # print(f"{position} al_pawns : {no_escapes['al_pawns']}")
            # print(f"{position} en_pawns : {no_escapes['en_pawns']}")
            # print(f"{position} escapes : {no_escapes['escapes']}")

            if no_escapes['bridges'] == 0:
                evaluation += 5
            elif no_escapes['escapes'] == 0:
                evaluation += 3
            elif no_escapes['escapes'] == 1:
                evaluation += 2
            elif no_escapes['escapes'] == 4:
                evaluation -= 2
            elif no_escapes['escapes'] == 2:
                if no_escapes['al_pawns'] == 0:
                    evaluation += 1
                # elif no_escapes['en_pawns'] == 1:
                #     evaluation -= 0
                elif no_escapes['al_pawns'] == 2:
                    evaluation -= 2
            else:
                if no_escapes['al_pawns'] == 1:
                    evaluation -= 3
                elif no_escapes['al_pawns'] == 0:
                    evaluation -= 1

            # DEBUG
            # print("ENEMY EVALUATION: " + str(evaluation))
            # print('\n')

        return evaluation

    # """
    # The evaluate function must return an integer value
    # representing the utility function of the board.
    # """
    # def evaluate(self, state):
    #     evaluation = 0
    #     for position in state.cur_pos[self.id]:
    #         adj_bridges = self.__no_adj_bridges(position, state)
    #         evaluation += self.link_weight[adj_bridges]
    #         evaluation -= self.__no_adj_pawns(position, state, self.id)

    #         # if there are two or more evacuation bridges for the current pawn
    #         # give a score of 2
    #         if adj_bridges - self.__no_adj_pawns(position, state, 1 - self.id) >= 2:
    #             evaluation += 2
    #         else:
    #             evaluation -= 2

    #     for position in state.cur_pos[1 - self.id]:
    #         adj_bridges = self.__no_adj_bridges(position, state)
    #         evaluation -= self.link_weight[adj_bridges]
    #         evaluation += self.__no_adj_pawns(position, state, 1 - self.id)

    #         # if there are two or more evacuation bridges for the current enemy's pawn
    #         # give a score of -2
    #         if adj_bridges - self.__no_adj_pawns(position, state, self.id) >= 2:
    #             evaluation -= 2
    #         else:
    #             evaluation += 2

    #     return evaluation


class Successor:
    def __init__(self, action, state, evaluation, reversed=True):
        self.action = action
        self.state = state
        self.evaluation = evaluation
        self.reversed = reversed

    def __lt__(self, other_successor):
        if self.reversed:
            return self.evaluation > other_successor.evaluation
        return self.evaluation < other_successor.evaluation

    def __le__(self, other_successor):
        if self.reversed:
            return self.evaluation >= other_successor.evaluation
        return self.evaluation <= other_successor.evaluation

    def __eq__(self, other_successor):
        """self == obj."""
        return self.evaluation == other_successor.evaluation

    def __ne__(self, other_successor):
        """self != obj."""
        return self.evaluation != other_successor.evaluation

    def __gt__(self, other_successor):
        if self.reversed:
            return self.evaluation < other_successor.evaluation
        return self.evaluation > other_successor.evaluation

    def __ge__(self, other_successor):
        if reversed:
            return self.evaluation <= other_successor.evaluation
        return self.evaluation >= other_successor.evaluation

    def response(self):
        return (self.action, self.state)
