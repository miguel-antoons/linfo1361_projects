import random
from agent import Agent
from smart_agent import MyAgent as MyAgent2


class MyAgent(Agent):
    def __init__(self):
        self.moves = []
        self.round = 0
        self.began = 0
        self.winner = None

    def get_action(self, state, last_action, time_left):
        if last_action is None:
            self.began = 1
        self.round += 1
        actions = state.get_current_player_actions()
        parent_enemy_bridges = 0
        # calculate number of enemy bridges for parent state
        for position in state.cur_pos[1 - state.cur_player]:
            parent_enemy_bridges += MyAgent2.no_adj_bridges(position, state)

        best_actions = []
        for action in actions:
            # create a new state
            new_state = state.copy()
            new_state.apply_action(action)

            # calculate number of enemy bridges for new state
            no_enemy_bridges = 0
            for position in new_state.cur_pos[new_state.cur_player]:
                no_enemy_bridges += MyAgent2.no_adj_bridges(position, new_state)

            if no_enemy_bridges < parent_enemy_bridges:
                best_actions.append(action)
        best_action = random.choice(best_actions)

        new_state = state.copy()
        new_state.apply_action(best_action)

        stats = self.total_stats(new_state)
        self.moves.append((
            self.id,
            self.began,
            self.round,
            stats['al_bridges'],
            stats['al_pawns'],
            stats['en_pawns'],
            stats['al_escapes'],
            stats['en_escapes'],
            stats['en_bridges']
        ))

        return best_action
  
    def get_name(self):
        return 'random agent'

    def get_stats(self, position: tuple, state) -> dict:
        no_escape = {
            'bridges': MyAgent2.no_adj_bridges(position, state),
            'al_pawns': MyAgent2.no_adj_pawns(position, state, self.id),
            'en_pawns': MyAgent2.no_adj_pawns(position, state, 1 - self.id)
        }
        no_escape['escapes'] = no_escape['bridges'] - no_escape['al_pawns'] - no_escape['en_pawns']
        return no_escape

    def total_stats(self, state) -> dict:
        total = {
            'al_bridges': 0,
            'al_pawns': 0,
            'en_pawns': 0,
            'al_escapes': 0,
            'en_escapes': 0,
            'en_bridges': 0
        }
        for position in state.cur_pos[self.id]:
            stats = self.get_stats(position, state)
            total['al_bridges'] += stats['bridges']
            total['al_pawns'] += stats['al_pawns']
            total['en_pawns'] += stats['en_pawns']
            total['al_escapes'] += stats['escapes']

        for position in state.cur_pos[1 - self.id]:
            stats = self.get_stats(position, state)
            total['en_bridges'] += stats['bridges']
            total['en_escapes'] += stats['escapes']
        return total
