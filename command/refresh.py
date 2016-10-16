import challonge
import config
from database.common import Table

challonge.set_credentials(config.challonge_id, config.challonge_api_key)

ft = Table('fg_tournament')
for row in ft.select('refresh = %s', (True, )):
    t = challonge.tournaments.show(row['challo_url'])
    ct = Table('challo_tournament')
    ct.delete('id = %s', (t['id'],))

    cp = Table('challo_participant')
    cp.delete('tournament_id = %s', (t['id'],))
    participants = []
    for p in challonge.participants.index(t['id']):
        participants.append(p['id'])
        cp.insert([p['id'], t['id'], p['name'], p['final-rank']])

    cm = Table('challo_match')
    cm.delete('tournament_id = %s', (t['id'],))
    groups = {}
    matches = challonge.matches.index(t['id'], participant_id=45832630)

    ids = []
    for m in matches:
        p1 = m['player1-id']
        p2 = m['player2-id']
        if p1 and p1 not in ids and p1 not in participants:
            ids.append(p1)
        if p2 and p2 not in ids and p2 not in participants:
            ids.append(p2)

    id_dictionary = dict(zip(sorted(ids), sorted(participants)))

    for m in matches:
        p1 = m['player1-id']
        p2 = m['player2-id']
        winner = m['winner-id']
        group_id = m['group-id'] if m['group-id'] is not None else 0
        r = m['round']
        if group_id not in groups:
            groups[group_id] = (r, r)

        if r < groups[group_id][0]:
            groups[group_id] = (r, groups[group_id][1])

        if r > groups[group_id][1]:
            groups[group_id] = (groups[group_id][0], r)

        if p1 in id_dictionary:
            p1 = id_dictionary[p1]

        if p2 in id_dictionary:
            p2 = id_dictionary[p2]

        if winner in id_dictionary:
            winner = id_dictionary[winner]

        if winner is not None and int(winner) > 0:
            cm.insert([
                m['id'], t['id'], m['round'], p1, p2, winner, m['scores-csv'], group_id
            ])

    cg = Table('challo_group')
    cg.delete('tournament_id = %s', (t['id'],))
    i = 65
    for group_id, rounds in groups.items():
        if group_id == 0:
            name = 'Main Tournament'
        else:
            name = 'Group {0}'.format(chr(i))
            i += 1
        cg.insert([group_id if group_id is not None else 0, t['id'], rounds[0], rounds[1], name])

    ct.insert([t['id'], t['name'], t['started-at'], t['tournament-type'], t['full-challonge-url']])

    ft.update(row['id'], {('refresh', False), ('challo_id', t['id'])})
    # ft.update(row['id'], {('challo_id', t['id'])})
