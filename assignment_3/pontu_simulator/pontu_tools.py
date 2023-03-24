from pontu_state import *
from pontu_gui import *
import traceback

def make_match(init_state, agents, time, display, logger):
    names = [a.get_name() for a in agents]
    if agents[0].id == 0:
        return play_game(init_state, names, agents, time, display, logger)
    else:
        agents.reverse()
        return play_game(init_state, names, agents, time, display, logger)

def play_game(init_state, names, players, total_time, display, logger):
    # create the initial state
    state = init_state
    # initialize the time left for each player
    time_left = [total_time for i in range(len(players))]
    action = None
    last_action = None
    gui = None
    if display:
        gui = GUIState()

    if logger != None:
        logger.write_initial(init_state)


    # loop until the game is over
    while not state.game_over():
        cur_player = state.get_cur_player()
        if display:
            gui.display_state(state)
            pygame.display.flip()
        try:
            action = players[cur_player].get_action(state, last_action, time_left)
        except Exception as e:
            trace = traceback.format_exc().split('\n')
            exception = trace[len(trace) - 2]
            # set that the current player crashed
            crashed = cur_player
            # write that the current player crashed
            if logger != None:
                logger.write_log(str(cur_player) + ' crashed (' + str(e) + ')')
            break
        else:
            # check if the action is valid
            try:
                if state.is_action_valid(action):
                    # the action is valid so we can apply the action to the state
                    # write the action of the current player on the log
                    if logger != None:
                        logger.write_action(cur_player, action)
                    state.apply_action(action)
                    last_action = action
                else:
                    print('invalid ' + str(action))
                    # set that the current player gave an invalid action
                    invalidaction = cur_player
                    if logger != None:
                        logger.write_log(str(cur_player) + ' invalid action')
                    break
            except Exception:
                # set that the current player gave an invalid action
                invalidaction = cur_player
                state.set_invalid_action(cur_player)
                if logger != None:
                    logger.write_log(str(cur_player) + ' could not apply action')
                break

    gui.display_winner(state)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)