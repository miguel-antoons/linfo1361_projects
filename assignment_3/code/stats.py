from pontu_tools import *
import csv


def play_game_2(game_n, initial_state):
    agent0 = "random_agent"
    agent1 = "random_agent"
    time_out = 900.0
    # first = '0'
    display_gui = False

    # initial_state = PontuState()
    # if first is not None:
    #     initial_state.cur_player = first
    agent0 = getattr(__import__(agent0), 'MyAgent')()
    agent0.set_id(0)
    agent1 = getattr(__import__(agent1), 'MyAgent')()
    agent1.set_id(1)
    res = play_game(initial_state, [agent0.get_name(), agent1.get_name()], [agent0, agent1], time_out, display_gui)
    # write_csv(agent0.moves, res[0], game_n)
    # write_csv(agent1.moves, res[0], game_n)

    return res[0]


def write_csv(data, winner, game_n):
    with open('stats.csv', 'a') as f:
        writer_2 = csv.writer(f)
        for item in data:
            writer_2.writerow((
                game_n,
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[5],
                item[6],
                item[7],
                item[8],
                winner
            ))


if __name__ == '__main__':
    with open('stats.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow((
            'game_n',
            'id',
            'began',
            'round',
            'al_bridges',
            'al_pawns',
            'en_pawns',
            'al_escapes',
            'en_escapes',
            'en_bridges',
            'winner'
        ))

    game_n = 0
    while True:
        game_n += 1
        play_game_2(game_n)
