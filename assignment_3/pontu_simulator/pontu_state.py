import random
from state import State
from copy import deepcopy


DIRECTIONS = ['WEST','NORTH','EAST','SOUTH']


class PontuState(State):

    def __init__(self, size = 5):
        self.cur_player = random.randint(0, 1)
        self.winner = None
        self.timeout_player = None
        self.invalid_player = None
        self.size = size
        # Position of the pawns
        self.cur_pos = [[(i,1) for i in range(1,self.size-1)], [(i,3) for i in range(1,self.size-1)]]
        # Indicate if the pawns are blocked
        self.blocked = [[False for i in range(self.size-2)], [False for i in range(self.size-2)]]
        # Indicate if the bridges are present
        self.h_bridges = [[True for i in range(self.size-1)] for j in range(self.size)]
        self.v_bridges = [[True for i in range(self.size)] for j in range(self.size-1)]
        # Contains all the previous moves
        self.history = []
        # The number of turns already played
        self.turns = 0

    def __eq__(self, other):
        return self.cur_player == other.cur_player and self.cur_pos == other.cur_pos

    def set_timed_out(self, player):
        self.timeout_player = player
        self.winner = 1 - player

    def set_invalid_action(self, player):
        self.invalid_player = player
        self.winner = 1 - player

    """
    Returns the position of the requested pawn ((x, y) position on the board (i.e. in multiples of 100))
    """

    def get_pawn_position(self, player, pawn):
        return self.cur_pos[player][pawn]

    """
    Returns whether the pawn is blocked
    """

    def is_pawn_blocked(self, player, pawn):
        return self.blocked[player][pawn]

    """
    Return a deep copy of this state.
    """

    def copy(self):
        cp = PontuState()
        cp.cur_player = self.cur_player
        cp.winner = self.winner
        cp.timeout_player = self.timeout_player
        cp.invalid_player = self.invalid_player
        cp.cur_pos = deepcopy(self.cur_pos)
        cp.blocked = deepcopy(self.blocked)
        cp.h_bridges = deepcopy(self.h_bridges)
        cp.v_bridges = deepcopy(self.v_bridges)
        cp.history = deepcopy(self.history)
        cp.turns = self.turns
        return cp

    """
    Return true if and only if the game is over (game ended, player timed out or made invalid move).
    """

    def game_over(self):
        if self.winner != None:
            return True
        return self.game_over_check()

    """
    Checks if a player succeeded to win the game, i.e. move 4 pawns to the other side and back again.
    """

    def game_over_check(self):
        for i in range(2):
            for j in range(self.size-2):
                if not self.blocked[i][j]:
                    self.pawn_blocked_check(i,j)
        if sum(self.blocked[0]) >= 3:
            self.winner = 1
            return True
        elif sum(self.blocked[1]) >= 3:
            self.winner = 0
            return True
        else:
            return False

    """
    Return the index of the current player.
    """

    def get_cur_player(self):
        return self.cur_player

    """
    Checks if a given action is valid.
    """

    def is_action_valid(self, action):
        actions = self.get_current_player_actions()
        return action in actions

    """
    Get all the actions that the current player can perform.
    """

    def get_current_player_actions(self):
        actions = []
        for i in range(self.size-2):
            if not self.blocked[self.cur_player][i]:
                    adj_bridges = self.adj_bridges(self.cur_player,i)
                    adj_pawns = self.adj_pawns(self.cur_player,i)
                    for dir in range(4):
                        if adj_bridges[dir] and not adj_pawns[dir]:
                            for y in range(len(self.h_bridges)):
                                for x in range(len(self.h_bridges[y])):
                                    if self.h_bridges[y][x]:
                                        actions.append((i,DIRECTIONS[dir],'h',x,y))
                            for y in range(len(self.v_bridges)):
                                for x in range(len(self.v_bridges[y])):
                                    if self.v_bridges[y][x]:
                                        actions.append((i,DIRECTIONS[dir],'v',x,y))
        if len(actions) == 0:
            for y in range(len(self.h_bridges)):
                for x in range(len(self.h_bridges[y])):
                    if self.h_bridges[y][x]:
                        actions.append((None, None, 'h', x, y))
            for y in range(len(self.v_bridges)):
                for x in range(len(self.v_bridges[y])):
                    if self.v_bridges[y][x]:
                        actions.append((None, None, 'v', x, y))
        return actions

    """
    Check if a pawn is blocked.
    """
    def pawn_blocked_check(self,player,pawn):
        adj_bridges = self.adj_bridges(player, pawn)
        if sum(adj_bridges) == 0:
            self.blocked[player][pawn] = True

    """
    Check the presence of the adjacent bridges
    """
    def adj_bridges(self,player,pawn):
        pos = self.cur_pos[player][pawn]
        bridges = []
        #Check west bridge
        if pos[0] >= 1:
            bridges.append(self.h_bridges[pos[1]][pos[0]-1])
        else:
            bridges.append(False)
        # Check north bridge
        if pos[1] >= 1:
            bridges.append(self.v_bridges[pos[1]-1][pos[0]])
        else:
            bridges.append(False)
        # Check east bridge
        if pos[0] < self.size-1:
            bridges.append(self.h_bridges[pos[1]][pos[0]])
        else:
            bridges.append(False)
        # Check south bridge
        if pos[1] < self.size-1:
            bridges.append(self.v_bridges[pos[1]][pos[0]])
        else:
            bridges.append(False)
        return bridges

    """
        Check if they are pawns adjacent
    """

    def adj_pawns(self, player, pawn):
        pos = self.cur_pos[player][pawn]
        pawns = []
        # Check west island
        west_pawn = False
        if pos[0] >= 1:
            for player in self.cur_pos:
                for (x,y) in player:
                    if pos == (x+1,y):
                        west_pawn = True
        pawns.append(west_pawn)
        # Check north island
        north_pawn = False
        if pos[1] >= 1:
            for player in self.cur_pos:
                for (x, y) in player:
                    if pos == (x, y+1):
                        north_pawn = True
        pawns.append(north_pawn)
        # Check east island
        east_pawn = False
        if pos[0] >= 1:
            for player in self.cur_pos:
                for (x, y) in player:
                    if pos == (x-1, y):
                        east_pawn = True
        pawns.append(east_pawn)
        # Check south island
        south_pawn = False
        if pos[0] >= 1:
            for player in self.cur_pos:
                for (x, y) in player:
                    if pos == (x, y-1):
                        south_pawn = True
        pawns.append(south_pawn)
        return pawns

    """
    Applies a given action to this state. It assume that the actions is
    valid. This must be checked with is_action_valid.
    """

    def apply_action(self, action):
        (pawn, d, b, x_b, y_b) = action
        if action[0] is not None:
            (x,y) = self.cur_pos[self.cur_player][pawn]
            if d == 'WEST':
                self.cur_pos[self.cur_player][pawn] = (x-1,y)
            elif d == 'NORTH':
                self.cur_pos[self.cur_player][pawn] = (x, y-1)
            elif d == 'EAST':
                self.cur_pos[self.cur_player][pawn] = (x+1, y)
            elif d == 'SOUTH':
                self.cur_pos[self.cur_player][pawn] = (x, y+1)
        if b == 'h':
            self.h_bridges[y_b][x_b] = False
        elif b == 'v':
            self.v_bridges[y_b][x_b] = False

        self.turns += 1
        self.history.append(action)
        self.cur_player = 1 - self.cur_player

    """
    Return the scores of each players.
    """

    def get_scores(self):
        if self.winner == None:
            return (0, 0)
        elif self.winner == 0:
            return (1, 0)
        return (0, 1)

    """
    Get the winner of the game. Call only if the game is over.
    """

    def get_winner(self):
        return self.winner

    """
    Return the information about the state that is given to students.
    Usually they have to implement their own state class.
    """

    def get_state_data(self):
        pass
