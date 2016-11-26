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

