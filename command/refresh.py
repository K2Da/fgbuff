import challonge
import config
from command.smash import SmashLoader
from database.common import Table

challonge.set_credentials(config.challonge_id, config.challonge_api_key)

ft = Table('fg_tournament')
for row in ft.select('refresh = %s', (True, )):
    if row['source'] == 'smash':
        l = SmashLoader(row)
        l.import_data()
    else:
        t = challonge.tournaments.show(row['challo_url'])

        cp = Table('challo_participant')
        cp.delete('tournament_id = %s', (row['id'],))
        participants = []
        for p in challonge.participants.index(t['id']):
            participants.append(p['id'])
            cp.insert([p['id'], row['id'], p['name'], p['final-rank']])

        cm = Table('challo_match')
        cm.delete('tournament_id = %s', (row['id'],))
        groups = {}
        matches = challonge.matches.index(t['id'])

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
                    m['id'], row['id'], m['round'], p1, p2, winner, m['scores-csv'], group_id
                ])

        cg = Table('challo_group')
        cg.delete('tournament_id = %s', (row['id'],))
        i = 65
        for group_id, rounds in groups.items():
            if group_id == 0:
                name = 'Main Tournament'
            else:
                name = 'Group {0}'.format(chr(i))
                i += 1
            cg.insert([group_id if group_id is not None else 0, row['id'], rounds[0], rounds[1], name])

        ft.update(row['id'], {('refresh', False), ('challo_id', t['id'])})
        # ft.update(row['id'], {('challo_id', t['id'])})
