from agent import AlphaBetaAgent
import minimax
import math
import queue as Q


class MyAgent(AlphaBetaAgent):
    """
    Agent skeleton. Fill in the gaps.
    """
    max_depth = 3
    n_round = -1
    steps = (2, 5, 8, 11, 13, 14, 15, 16, 17, 18, 19, 20)
    link_weight = (-4, -1, 0, 3, 4)
    index = 0

    """
    This is the skeleton of an agent to play the Tak game.
    """
    def get_action(self, state, last_action, time_left):
        self.n_round += 1
        # DEBUG
        # if self.n_round > 0:
        #     raise Exception("History not empty")
        if math.floor(self.n_round / self.steps[self.index]) == 1:
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
        first_choice = Q.PriorityQueue()
        # second_choice = Q.PriorityQueue()
        # third_choice = Q.PriorityQueue()
        parent_enemy_bridges = 0
        parent_bridges = 0

        # calculate number of enemy bridges for parent state
        for position in state.cur_pos[1 - state.cur_player]:
            parent_enemy_bridges += self.__no_adj_bridges(position, state)

        # calculate number of bridges for parent state
        for position in state.cur_pos[state.cur_player]:
            parent_bridges += self.__no_adj_bridges(position, state)

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
                first_choice.put(Successor(action, new_state, parent_enemy_bridges, no_enemy_bridges, bridges))

        while not first_choice.empty():
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

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        evaluation = 0
        for position in state.cur_pos[self.id]:
            adj_bridges = self.__no_adj_bridges(position, state)
            evaluation += self.link_weight[adj_bridges]
            evaluation -= self.__no_adj_pawns(position, state, self.id)

            # if there are two or more evacuation bridges for the current pawn
            # give a score of 2
            if adj_bridges - self.__no_adj_pawns(position, state, 1 - self.id) >= 2:
                evaluation += 2
            else:
                evaluation -= 2

        for position in state.cur_pos[1 - self.id]:
            adj_bridges = self.__no_adj_bridges(position, state)
            evaluation -= self.link_weight[adj_bridges]
            evaluation += self.__no_adj_pawns(position, state, 1 - self.id)

            # if there are two or more evacuation bridges for the current enemy's pawn
            # give a score of -2
            if adj_bridges - self.__no_adj_pawns(position, state, self.id) >= 2:
                evaluation -= 2
            else:
                evaluation += 2

        return evaluation


class Successor:
    def __init__(self, action, state, parent_enemy_bridges, enemy_bridges, bridges):
        self.parent_enemy_bridges = parent_enemy_bridges
        self.enemy_bridges = enemy_bridges
        self.action = action
        self.state = state
        self.bridges = bridges

    def __lt__(self, other_successor):
        if self.bridges > other_successor.bridges:
            return True

        if self.bridges == other_successor.bridges:
            # if we removed a bridge between to enemy's pawn and the other successor did not
            # then we want to choose the other successor
            if (self.parent_enemy_bridges - self.enemy_bridges) == 2 and (other_successor.parent_enemy_bridges - other_successor.enemy_bridges) == 1:
                return False

            if self.enemy_bridges < other_successor.enemy_bridges:
                return True

        return False

    def response(self):
        return (self.action, self.state)
