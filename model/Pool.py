import sys
from Lib import re
from database import service
from typing import Dict, List, Any


class Pool:
    def __init__(self, data: Dict[str, List[Dict]]):
        # rows
        self.fg_tournament = data['fg_tournament'] if 'fg_tournament' in data else []
        self.fg_player = data['fg_player'] if 'fg_player' in data else []

        self.challo_participant = data['challo_participant'] if 'challo_participant' in data else []
        self.challo_match = data['challo_match'] if 'challo_match' in data else []
        self.challo_group = data['challo_group'] if 'challo_group' in data else []

        self.rel_vs = data['rel_vs'] if 'rel_vs' in data else []

        # object array
        self.players = {p['id']: Player(self, p) for p in self.fg_player}
        self.tournaments = {t['id']: Touranament(self, t) for t in self.fg_tournament}
        self.participants = {p['id']: Participant(self, p) for p in self.challo_participant}
        self.matches = {m['id']: Match(self, m) for m in self.challo_match}
        self.groups = {(g['tournament_id'], g['id']): Group(self, g) for g in self.challo_group}
        self.vs = {(v['player_id'], v['opponent_id']): Vs(self, v) for v in self.rel_vs}

        # dic
        self.participant_to_player = {
            r['challo_id']: r['fg_id'] for r in data['rel_player']
        } if 'rel_player' in data else {}
        self.player_to_participant = {
            (r['tournament_id'], r['fg_id']): r['challo_id'] for r in data['rel_player']
        } if 'rel_player' in data else {}
        self.challo_tournament_to_fg = {
            t['challo_id']: t['id'] for t in data['fg_tournament']
        } if 'fg_tournament' in data else {}

    @classmethod
    def init_for_tournament(cls, challo_url):
        fg_tournament, pool = service.select_by_tournament_id(challo_url)
        return fg_tournament, cls(pool)

    @classmethod
    def init_for_vs(cls, p1, p2):
        p1_id, p2_id, pool = service.select_for_vs(p1, p2)
        return p1_id, p2_id, cls(pool)

    @classmethod
    def init_for_player(cls, player_url):
        player_id, pool = service.select_by_player_url(player_url)
        return player_id, cls(pool)

    @classmethod
    def init_for_tournaments(cls):
        return cls(service.select_for_tournaments())

    @classmethod
    def init_for_players(cls):
        return cls(service.select_for_players())

    @classmethod
    def init_for_create_rel(cls):
        return cls(service.select_for_create_rel())

    @classmethod
    def init_for_create_vs(cls):
        return cls(service.select_for_create_vs())


class Row:
    def __init__(self, pool: Pool, challo_row: Dict[str, Any]):
        self._pool = pool
        self._challo_row = challo_row

    @property
    def id(self):
        return self.get_with_default('id', 0)

    def get_with_default(self, column, default):
        if self._challo_row is not None and column in self._challo_row and self._challo_row[column] is not None:
            return self._challo_row[column]
        else:
            return default


class Touranament(Row):
    @property
    def name(self):
        return self.get_with_default('name', '-')

    @property
    def link_or_name(self):
        if self.challo_url is None:
            return self.name
        return '<a href="/tournament/{0}">{1}</a>'.format(self.challo_url, self.name)

    @property
    def challo_url(self):
        return self.get_with_default('challo_url', None)

    @property
    def tournament_link(self):
        if self._challo_row['full_url'] is None or len(self._challo_row['full_url']) == 0:
            return ""
        return '<a href="{0}">challonge</a>'.format(self.get_with_default('full_url', ''))

    @property
    def end_at(self):
        return self.get_with_default('end_at', '-')

    @property
    def type(self):
        return self.get_with_default('type', '-')

    @property
    def end_at_desc(self):
        return -(self.end_at.year * 1000 + self.end_at.month * 100 + self.end_at.day)


class Participant(Row):
    @property
    def name(self):
        return self.get_with_default('name', '-')

    @property
    def tournament_id(self):
        return self.get_with_default('tournament_id', 0)

    @property
    def final_rank(self):
        return self.get_with_default('final_rank', 0)

    @property
    def rank_for_sort(self):
        return self.get_with_default('final_rank', sys.maxsize)

    @property
    def rank_text(self):
        return self.get_with_default('final_rank', '-')

    @property
    def player(self):
        if self.id in self._pool.participant_to_player:
            return self._pool.players[self._pool.participant_to_player[self.id]]
        else:
            return Player(self._pool, {})

    @property
    def link_or_text(self):
        if self.id in self._pool.participant_to_player:
            return self._pool.players[self._pool.participant_to_player[self.id]].link
        else:
            return self.name


class Group(Row):
    @property
    def min_round(self):
        return self.get_with_default('min_round', '-1')

    @property
    def max_round(self):
        return self.get_with_default('max_round', '1')

    @property
    def name(self):
        return self.get_with_default('name', '')


class Vs(Row):
    @property
    def player(self):
        if self._challo_row['player_id'] in self._pool.players:
            return self._pool.players[self._challo_row['player_id']]
        else:
            return Player(self._pool, {})

    @property
    def opponent(self):
        if self._challo_row['opponent_id'] in self._pool.players:
            return self._pool.players[self._challo_row['opponent_id']]
        else:
            return Player(self._pool, {})

    @property
    def win(self):
        return self.get_with_default('win', 0)

    @property
    def lose(self):
        return self.get_with_default('lose', 0)

    @property
    def sort_key(self):
        return -(self.win + self.lose)


class Match(Row):
    @property
    def scores_csv(self):
        return self._challo_row['scores_csv']

    @property
    def player1(self):
        if self._challo_row['player1_id'] in self._pool.participants:
            return self._pool.participants[self._challo_row['player1_id']]
        else:
            return Participant(self._pool, {})

    @property
    def player2(self):
        if self._challo_row['player2_id'] in self._pool.participants:
            return self._pool.participants[self._challo_row['player2_id']]
        else:
            return Participant(self._pool, {})

    @property
    def round(self):
        return self._challo_row['round']

    @property
    def sort_key(self):
        r = float(self.round)
        if r > 0:
            key = self.group.max_round - r
        else:
            key = (abs(self.group.min_round) - abs(r)) * 0.5 + 0.25

        return key

    @property
    def id_desc(self):
        return -self.id

    @property
    def tournament(self) -> Touranament:
        return self._pool.tournaments[self.tournament_id]

    @property
    def group(self) -> Group:
        return self._pool.groups[self.tournament_id, self.group_id]

    @property
    def round_name(self):
        max_r = self.group.max_round
        r = self.round
        if r < 0:
            return "Losers {0}".format(abs(r))
        elif r == max_r:
            return "Grand Final"
        elif r == max_r - 1:
            return "Winners Final"
        else:
            return "Winners {0}".format(abs(r))

    @property
    def tournament_id(self):
        return self.get_with_default('tournament_id', 0)

    @property
    def end_at_desc(self):
        return self.tournament.end_at_desc

    @property
    def group_id(self):
        return self.get_with_default('group_id', 0)

    @property
    def p1_win(self):
        return self.get_with_default('winner_id', -1) == self.player1.id

    @property
    def p2_win(self):
        return self.get_with_default('winner_id', -1) == self.player2.id


class Player(Row):
    def __init__(self, pool, challo_row):
        self.re = None
        super(Player, self).__init__(pool, challo_row)

    @property
    def url(self):
        return self.get_with_default('url', '')

    @property
    def name(self):
        return self.get_with_default('name', '')

    @property
    def patterns(self):
        return self.get_with_default('patterns', '')

    @property
    def unique(self):
        return self.get_with_default('unique', '')

    @property
    def link(self):
        return '<a href="/player/{0}">{1}</a>'.format(self.url, self.name)

    @property
    def win(self):
        return self.get_with_default('win', 0)

    @property
    def lose(self):
        return self.get_with_default('lose', 0)

    @property
    def sort_key(self):
        return -(self.win + self.lose)

    @property
    def participant_ids(self):
        return [pid for tf, pid in self._pool.player_to_participant.items() if tf[1] == self.id]

    def maybe(self, name: str):
        def normalize(txt):
            return re.sub('[/\-*_ .\'　|丨│︱]', '', txt.lower())

        def trim(txt):
            return '(^|\]){0}(\(|$|／|\[|-)'.format(txt)

        def separate_team_name(txt):
            spl = normalize(txt).split('|')
            if len(spl) != 2:
                reg_name = trim(re.escape(normalize(txt).lower()))
            else:
                s1 = re.escape(spl[0])
                s2 = re.escape(spl[1])
                tn = trim('{0}[ \(\)\|\.]*{1}'.format(s1, s2))
                nt = trim('{0}[ \(\)\|\.]*{1}'.format(s2, s1))
                reg_name = '{0}|{1}'.format(tn, nt)
            return reg_name

        def join_reg(patterns):
            return '|'.join([separate_team_name(p) for p in patterns])

        if self.re is None:
            additional = self.patterns.split('^') if len(self.patterns) != 0 else []
            self.re = re.compile(join_reg([self.name, self.url] + additional))

        if self.re.search(normalize(name)) is not None:
            return True

        if len(self.unique) == 0:
            return False

        # uniqueチェック
        # 削ったりせず、素で比べて連続した文字列じゃない状態で含まれてればOK
        ret = re.search('([^a-z]|^){0}([^a-z]|$)'.format(self.unique.lower()), name.lower())
        return ret is not None

