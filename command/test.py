from model.Pool import Pool
from operator import attrgetter
from util.glicko2 import Rate, WIN, LOSE
import cProfile


def calc():
    pool = Pool.init_for_ratings()
    rates = {player['id']: Rate(1500, 200, 0.06) for player in pool.fg_player}
    history = {player['id']: [] for player in pool.fg_player}

    for t in sorted(pool.tournaments.values(), key=attrgetter('end_at_desc'), reverse=True):
        o = {index: rate.copy() for index, rate in rates.items()}
        m = {index: [] for index in rates.keys()}

        for match in t.matches:
            fg1 = match.player1.player.id
            fg2 = match.player2.player.id

            if fg1 != 0 and fg2 != 0:
                w1, w2 = match.p1_win_count, match.p2_win_count
                m[fg1].extend([(o[fg2], WIN) for _ in range(w1)] + [(o[fg2], LOSE) for _ in range(w2)])
                m[fg2].extend([(o[fg1], WIN) for _ in range(w2)] + [(o[fg1], LOSE) for _ in range(w1)])

        for index, rate in rates.items():
            if m[index]:
                rate.add_match(m[index])
                history[index].append((t.date_string, str(rate.rating)))

    for pair in sorted(rates.items(), key=lambda x: x[1].mu, reverse=True):
        index, rate = pair[0], pair[1]
        if rate.rd < 50:
            print(pool.players[index].name + "\t" + str(int(rate.rating)) + "\t" + str(int(rate.rd)))
            # for his in history[index]:
                # print(his[0] + " : " + his[1])

cProfile.run('calc()')
