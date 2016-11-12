from database.common import Table
from model.Pool import Pool

pool = Pool.init_for_create_rel()
cp = Table('challo_participant')
cp.update_all([('player_id', None)])

i = 0
for participant in pool.participants.values():
    for player in pool.players.values():
        if player.maybe(participant.name):
            print("{0} -> {1}".format(participant.name, player.name))
            cp.update_with_tournament_id(participant.tournament_id, participant.id, [('player_id', player.id)])
            i += 1

print("participants {0}".format(i))

pool = Pool.init_for_create_vs()
i = 0
p = {player['id']: (0, 0) for player in pool.fg_player}
for m in pool.matches.values():
    fg1 = m.player1.player.id
    fg2 = m.player2.player.id

    if fg1 != 0 and (m.p1_win or m.p2_win):
        p[fg1] = (p[fg1][0] + 1, p[fg1][1]) if m.p1_win else (p[fg1][0], p[fg1][1] + 1)

    if fg2 != 0 and (m.p1_win or m.p2_win):
        p[fg2] = (p[fg2][0] + 1, p[fg2][1]) if m.p2_win else (p[fg2][0], p[fg2][1] + 1)

for player, wl in p.items():
    Table('fg_player').update(player, [('win', wl[0]), ('lose', wl[1])])

print("vs {0}".format(i))

