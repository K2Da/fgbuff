from database.common import Table
from model.Pool import Pool

pool = Pool.init_for_create_rel()
cp = Table('challo_participant')
cp.update_all([('player_id', None)])

i = 0
for participant in pool.participants.values():
    found = []
    for player in pool.players.values():
        if player.maybe(participant.name):
            cp.update_with_tournament_id(participant.tournament_id, participant.id, [('player_id', player.id)])
            found.append(player.name)
            i += 1

    if len(found) > 1:
        print('duplicated candidate for {0} : {1} = {2}'.format(participant.tournament.name, participant.name, ','.join(found)))

print("participants {0}".format(i))

