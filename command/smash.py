import json
import urllib.request
from database.common import Table


class SmashLoader:
    api_url = 'https://api.smash.gg/phase_group/{0}?expand%5B%5D=sets&expand%5B%5D=standings&expand%5B%5D=entrants'

    def __init__(self, tournament):
        self.ft = Table('fg_tournament')
        self.cm = Table('challo_match')
        self.cp = Table('challo_participant')
        self.cg = Table('challo_group')
        self.tournament = tournament
        self.json_text = self._get_json()

    def _get_json(self):
        url = self.api_url.format(self.tournament['source_key'])
        with urllib.request.urlopen(url) as res:
            return res.read().decode('utf-8')

    def import_data(self):
        obj = json.loads(self.json_text)
        self.cm.delete('tournament_id = %s', (self.tournament['id'],))
        self.cp.delete('tournament_id = %s', (self.tournament['id'],))
        self.cg.delete('tournament_id = %s', (self.tournament['id'],))

        groups = {}
        group_id = 0
        for s in obj['entities']['sets']:
            r = s['round']
            if group_id not in groups:
                groups[group_id] = (r, r)

            if r < groups[group_id][0]:
                groups[group_id] = (r, groups[group_id][1])

            if r > groups[group_id][1]:
                groups[group_id] = (groups[group_id][0], r)

            if s['entrant1Id'] and s['entrant2Id']:
                self.cm.insert([
                    s['id'], self.tournament['id'], s['round'], s['entrant1Id'], s['entrant2Id'],
                    s['winnerId'], self.create_score(s), 0]
                )

        for p in obj['entities']['entrants']:
            self.cp.insert([
                p['id'], self.tournament['id'], p['name'], p['finalPlacement']
            ])

        i = 65
        for group_id, rounds in groups.items():
            if group_id == 0:
                name = 'Main Tournament'
            else:
                name = 'Group {0}'.format(chr(i))
                i += 1
            self.cg.insert([group_id if group_id is not None else 0, self.tournament['id'], rounds[0], rounds[1], name])

        self.ft.update(self.tournament['id'], {('refresh', False)})

    @staticmethod
    def create_score(s):
        if s['entrant1Score'] is None or s['entrant2Score'] is None:
            return '-'

        if s['entrant1Score'] < 0 or s['entrant2Score'] < 0:
            return '-'

        return str(s['entrant1Score']) + '-' + str(s['entrant2Score'])

