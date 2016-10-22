import json

# https://api.smash.gg/phase_group/229749?expand%5B%5D=sets&expand%5B%5D=entrants


class SmashLoader:
    def __init__(self, json_text):
        self.json_text = json_text

    def import_data(self):
        obj = json.loads(self.json_text)
        return obj


lines = open('c:\\Workspace\\data\\a.json').read()
l = SmashLoader(lines)
o = l.import_data()
print(o)

# challo_tournament
# id, name, started_at, tournament_type, full_challonge_url
