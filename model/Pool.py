import sys
import re
import model.Labels
import model.Countries
from database import service
from typing import Dict, List, Any
from operator import attrgetter
from functools import reduce
from util.glicko2 import Rate, WIN, LOSE, RATE
import collections


class Pool:
    def __init__(self, data: Dict[str, Any]):
        # for link
        self.base_url = data.get('base_url', [])
        self.labels = data.get('labels', [])

        # rows
        self.fg_tournament = data.get('fg_tournament', [])
        self.fg_player = data.get('fg_player', [])

        self.challo_participant = data.get('challo_participant', [])
        self.challo_match = data.get('challo_match', [])
        self.challo_group = data.get('challo_group', [])

        # object array
        self.players = {p['id']: Player(self, p) for p in self.fg_player}
        self.tournaments = {t['id']: Touranament(self, t) for t in self.fg_tournament}
        self.participants = {(p['tournament_id'], p['id']): Participant(self, p) for p in self.challo_participant}
        self.matches = {(m['tournament_id'], m['id']): Match(self, m) for m in self.challo_match}
        self.groups = {(g['tournament_id'], g['id']): Group(self, g) for g in self.challo_group}

        # dic
        self.player_to_participant = {
            (r['tournament_id'], r['player_id']): (r['tournament_id'], r['id']) for r in data['challo_participant']
        } if 'challo_participant' in data else {}
        self.challo_tournament_to_fg = {
            t['challo_id']: t['id'] for t in data['fg_tournament']
        } if 'fg_tournament' in data else {}
        self._vs = None
        self._wl_counted = False
        self._ratings = None
        self._rating_log = None
        self._rating_match_count = 0

    def link_other_tags(self, text: str, tags: list, active: bool) -> str:
        return '<a href="{0}">{1}</a>'.format(
            self.href_with_tags(tags), text
        ) if not active else '<strong>{0}</strong>'.format(text)

    def href_with_tags(self, tags: list) -> str:
        if not tags:
            return '/{0}'.format(self.base_url)
        return '/{0}/labels/{1}'.format(
            self.base_url, '/'.join([t.key for t in tags])
        )

    def a(self, text, url):
        return '<a href="/{0}">{1}</a>'.format(url, text)

    def a_with_current_labels(self, text, url):
        if not self.labels:
            return '<a href="{0}">{1}</a>'.format(self.href_with_current_labels(url), text)
        else:
            return '<a href="{0}">{1}</a>'.format(self.href_with_current_labels(url), text)

    def href_with_current_labels(self, url):
        if not self.labels:
            return '/{0}'.format(url)
        else:
            return '/{0}/labels/{1}'.format(url, '/'.join([t.key for t in self.labels]))

    def labels_included(self, labels: list, index: int) -> bool:
        if len(self.labels) == 0:
            return index == 0

        if len(self.labels) < len(labels):
            return False

        for a, b in zip(labels, self.labels):
            if a != b:
                return False

        return True

    def labels_same(self, labels: list) -> bool:
        if len(self.labels) != len(labels):
            return False

        for a, b in zip(labels, self.labels):
            if a != b:
                return False

        return True

    def labels_text(self) -> str:
        return ', '.join([l.text for l in self.labels])

    @property
    def vs(self):
        if self._vs is None:
            vs = {player['id']: {} for player in self.fg_player}
            for m in self.matches.values():
                fg1, fg2 = m.player1.player.id, m.player2.player.id
                if fg1 != 0 and fg2 != 0 and (m.p1_win or m.p2_win):
                    if m.p1_win:
                        w, l = fg1, fg2
                    if m.p2_win:
                        w, l = fg2, fg1

                    vs[w][l] = (vs[w][l][0] + 1, vs[w][l][1]) if l in vs[w] else (1, 0)
                    vs[l][w] = (vs[l][w][0], vs[l][w][1] + 1) if w in vs[l] else (0, 1)

            self._vs = {}
            for player, opponent_dic in vs.items():
                for opponent, wl in opponent_dic.items():
                    self.vs[(player, opponent)] = Vs(self, player, opponent, wl[0], wl[1])

        return self._vs

    def sum_wl(self):
        if self._wl_counted:
            return
        for m in self.matches.values():
            if m.p1_win:
                m.player1.player.add_win()
                m.player2.player.add_lose()
            if m.p2_win:
                m.player2.player.add_win()
                m.player1.player.add_lose()
        self._wl_counted = True

    @property
    def ratings(self):
        if not self._ratings:
            self.calc_rating()

        return self._ratings

    def rating_log(self, player_url):
        if not self._rating_log:
            self.calc_rating()

        for p in self.players.values():
            if p.url == player_url:
                return RatingLog(p, self._rating_log[p.id])

        return None

    @property
    def rating_match_count(self):
        if self._rating_match_count == 0:
            self.calc_rating()

        return self._rating_match_count

    def calc_rating(self):
        self._ratings = {player['id']: Rate() for player in self.fg_player}
        self._rating_log = {player['id']: [] for player in self.fg_player}
        self._rating_match_count = 0

        for t in sorted(self.tournaments.values(), key=attrgetter('end_at_desc'), reverse=True):
            o = {index: rate.copy() for index, rate in self._ratings.items()}
            m = {index: [] for index in self._ratings.keys()}

            for match in t.matches:
                fg1, fg2 = match.player1.player.id, match.player2.player.id

                if fg1 != 0 and fg2 != 0:
                    self._rating_match_count += 1
                    w1, w2 = match.p1_win_count, match.p2_win_count
                    m[fg1].extend([(o[fg2], WIN) for _ in range(w1)] + [(o[fg2], LOSE) for _ in range(w2)])
                    m[fg2].extend([(o[fg1], WIN) for _ in range(w2)] + [(o[fg1], LOSE) for _ in range(w1)])

            for index, rate in self._ratings.items():
                if m[index]:
                    rate.add_match(m[index])
                    self._rating_log[index].append((t, rate.copy()))

    @classmethod
    def init_for_tournament(cls, challo_url):
        tournament_id, pool = service.select_by_tournament_id(challo_url)
        return tournament_id, cls(pool)

    @classmethod
    def init_for_vs(cls, p1, p2, labels):
        p1_id, p2_id, pool = service.select_for_vs(p1, p2, labels)
        return p1_id, p2_id, cls(pool)

    @classmethod
    def init_for_player(cls, player_url, labels):
        player_id, pool = service.select_by_player_url(player_url, labels)
        return player_id, cls(pool)

    @classmethod
    def init_for_tournaments(cls, labels):
        return cls(service.select_for_tournaments(labels))

    @classmethod
    def init_for_players(cls, labels):
        return cls(service.select_for_players(labels))

    @classmethod
    def init_for_create_rel(cls):
        return cls(service.select_for_create_rel())

    @classmethod
    def init_for_ratings(cls, player_and_labels=None, labels=None):
        player_urls, pool = service.select_for_ratings(player_and_labels=player_and_labels, labels=labels)
        return player_urls, cls(pool)

    @classmethod
    def init_for_standing(cls, standing_url, labels):
        standing, pool = service.select_for_vs_table(standing_url, labels)
        return Standing(Pool({}), standing), cls(pool)


class Row:
    def __init__(self, pool: Pool, challo_row: Dict[str, Any]):
        self._pool = pool
        self._row = challo_row
        self.id = self._row['id'] if self._row is not None and 'id' in self._row else 0

    def get(self, column, default):
        if self._row is not None and column in self._row and self._row[column] is not None:
            return self._row[column]
        else:
            return default


class CountryMixin:
    @property
    def country(self):
        return self.get('country', '')

    @property
    def flag_span(self):
        if self.country == '':
            return ''
        if self.country == '@O':
            return "<span data-toggle='tooltip' title='{0}'>🌐</span>".format(self.country_name)

        span = "<span class='flag-icon flag-icon-{0}'  data-toggle='tooltip' title='{1}'></span>"
        return span.format(self.country, self.country_name)

    @property
    def country_name(self):
        return model.Countries.code_to_name(self.country)


class Touranament(Row, CountryMixin):
    link_names = {
        'challo': 'challonge',
        'smash': 'smash.gg'
    }

    def player_at_rank(self, rank: int) -> list:
        rankers = [
            p for p in self._pool.participants.values()
            if p.tournament_id == self.id and p.final_rank == rank
        ]
        if rankers:
            return [p.player for p in rankers]
        else:
            return []

    @property
    def name(self):
        return self.get('name', '-')

    @property
    def a(self):
        if self.challo_url is None:
            return self.name
        return self._pool.a(self.name, 'tournament/{0}'.format(self.challo_url))

    @property
    def challo_url(self):
        return self.get('challo_url', None)

    @property
    def tournament_link(self):
        if self._row['full_url'] is None or len(self._row['full_url']) == 0:
            return ""
        link = self.link_names[self._row['source']] if self._row['source'] in self.link_names else self._row['source']
        return '<a href="{0}">{1}</a>'.format(self.get('full_url', ''), link)

    @property
    def end_at(self):
        return self.get('end_at', '-')

    @property
    def date_string(self):
        end_at = self.end_at
        if end_at == '-':
            return '-'

        return end_at.strftime('%b %d, %Y')

    @property
    def type(self):
        return self.get('type', '-')

    @property
    def end_at_desc(self):
        return -(self.end_at.year * 12 * 32 + self.end_at.month * 32 + self.end_at.day)

    @property
    def labels_short(self):
        labels = model.Labels.labels_from_string(self.get('labels', ''))
        return reduce(lambda a, b: a + ', ' + b, map(lambda l: l.short, labels))

    @property
    def labels_text(self):
        labels = model.Labels.labels_from_string(self.get('labels', ''))
        return reduce(lambda a, b: a + ', ' + b, map(lambda l: l.text, labels))

    @property
    def matches(self):
        return [m for tm, m in self._pool.matches.items() if tm[0] == self.id]

    def participant_by_player(self, player_id):
        for tp, participant in self._pool.participants.items():
            if tp[0] == self.id and participant.player_id == player_id:
                return participant

        return None


class Participant(Row):
    @property
    def name(self):
        return self.get('name', '-')

    @property
    def tournament_id(self):
        return self.get('tournament_id', 0)

    @property
    def tournament(self) -> Touranament:
        return self._pool.tournaments[self.tournament_id]

    @property
    def final_rank(self):
        return self.get('final_rank', 100000)

    @property
    def rank_for_sort(self):
        return self.get('final_rank', sys.maxsize)

    @property
    def rank_text(self):
        return self.get('final_rank', '-')

    @property
    def rank_emoji(self):
        if self.final_rank == 1:
            return '🥇'
        if self.final_rank == 2:
            return '🥈'
        if self.final_rank == 3:
            return '🥉'
        return '🏁'

    @property
    def player_id(self):
        return self.get('player_id', 0)

    @property
    def player(self):
        if self.player_id:
            return self._pool.players[self.player_id]
        else:
            return Player(self._pool, {})

    @property
    def link_or_text(self):
        if self.player_id:
            return self._pool.players[self.player_id].link
        else:
            return self.name

    @property
    def wl(self):
        matches = self._pool.matches.values()
        (w, l) = (0, 0)

        ret = ""
        for m in sorted(matches, key=attrgetter('tournament_id', 'group_id', 'sort_key', 'id_desc')):
            if m.player1 == self and m.p1_win or m.player2 == self and m.p2_win:
                ret = '<span style="color: green">{0}</span>'.format('✔') + ret
                w += 1
            if m.player1 == self and m.p2_win or m.player2 == self and m.p1_win:
                ret = '<span style="color: red">{0}</span>'.format('✖') + ret
                l += 1
        return '({0} / {1}) '.format(w, l) + ret

    @property
    def end_at_desc(self):
        return self.tournament.end_at_desc


class Group(Row):
    @property
    def min_round(self):
        return self.get('min_round', '-1')

    @property
    def max_round(self):
        return self.get('max_round', '1')

    @property
    def name(self):
        return self.get('name', '')

    @property
    def ttype(self):
        return self.get('ttype', '')

    @property
    def tournament_type(self):
        if self.ttype == 'DE':
            return 'Double Elimination'
        if self.ttype == 'SE':
            return 'Single Elimination'
        return ''


class Vs:
    def __init__(self, pool, player_id, opponent_id, win, lose):
        self._pool = pool
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.win = win
        self.lose = lose

    @property
    def player(self):
        if self.player_id in self._pool.players:
            return self._pool.players[self.player_id]
        else:
            return Player(self._pool, {})

    @property
    def opponent(self):
        if self.opponent_id in self._pool.players:
            return self._pool.players[self.opponent_id]
        else:
            return Player(self._pool, {})

    @property
    def sort_key(self):
        return -((self.win + self.lose) * 10000 + self.win)

    @property
    def wl(self):
        matches = self._pool.matches.values()
        ret = ""
        for m in sorted(matches, key=attrgetter('end_at_desc', 'group_id', 'sort_key', 'id_desc')):
            if (
                  m.player1.player == self.player and m.player2.player == self.opponent and m.p1_win or
                  m.player2.player == self.player and m.player1.player == self.opponent and m.p2_win
               ):
                ret = '<span style="color: green">{0}</span>'.format('✔') + ret
            if (
                  m.player1.player == self.player and m.player2.player == self.opponent and m.p2_win or
                  m.player2.player == self.player and m.player1.player == self.opponent and m.p1_win
               ):
                ret = '<span style="color: red">{0}</span>'.format('✖') + ret
        return ret


class Match(Row):
    @property
    def scores_csv(self):
        return self.get('scores_csv', '')

    @property
    def reverse_scores(self):
        return self.scores_csv[::-1] if len(self.scores_csv) > 0 else ''

    @property
    def player1(self):
        if (self.tournament_id, self._row['player1_id']) in self._pool.participants:
            return self._pool.participants[(self.tournament_id, self._row['player1_id'])]
        else:
            return Participant(self._pool, {})

    @property
    def player2(self):
        if (self.tournament_id, self._row['player2_id']) in self._pool.participants:
            return self._pool.participants[(self.tournament_id, self._row['player2_id'])]
        else:
            return Participant(self._pool, {})

    @property
    def round(self):
        return self._row['round']

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
        if self.group.ttype == 'DE':
            return self.round_name_de
        if self.group.ttype == 'SE':
            return self.round_name_se

    @property
    def round_name_de(self):
        max_r = self.group.max_round
        min_r = self.group.min_round
        r = self.round
        if r == min_r:
            return "Losers Final".format(abs(r))
        elif r == min_r + 1:
            return "Losers Semi Final".format(abs(r))
        elif r < 0:
            return "Losers {0}".format(abs(r))
        elif r == max_r:
            return "Grand Final"
        elif r == max_r - 2:
            return "Winners Semi Final"
        elif r == max_r - 1:
            return "Winners Final"
        else:
            return "Winners {0}".format(abs(r))

    @property
    def round_name_se(self):
        max_r = self.group.max_round
        r = self.round
        if r == max_r:
            return "Final"
        elif r == max_r - 1:
            return "Semi Final"
        else:
            return "Winners {0}".format(r)

    @property
    def tournament_id(self):
        return self.get('tournament_id', 0)

    @property
    def end_at_desc(self):
        return self.tournament.end_at_desc

    @property
    def group_id(self):
        return self.get('group_id', 0)

    @property
    def p1_win(self):
        return self.get('winner_id', -1) == self.player1.id

    @property
    def p2_win(self):
        return self.get('winner_id', -1) == self.player2.id

    @property
    def p1_win_count(self):
        if not self.scores_csv.split('-')[0].isdigit():
            raise Exception(self.tournament.name)

        i = int(self.scores_csv.split('-')[0])
        if i > 10:
            raise Exception(self.scores_csv)
        return i

    @property
    def p2_win_count(self):
        if not self.scores_csv.split('-')[1].isdigit():
            raise Exception(self.tournament.name)

        i = int(self.scores_csv.split('-')[1])
        if i > 10:
            raise Exception(self.scores_csv)
        return i


class Player(Row, CountryMixin):
    def __init__(self, pool, challo_row):
        self.re = None
        self._win = None
        self._lose = None
        self._rank_dic = None
        self.name_matcher = None
        super(Player, self).__init__(pool, challo_row)

    def add_win(self):
        if self._win is None:
            self._win = 0
        self._win += 1

    def add_lose(self):
        if self._lose is None:
            self._lose = 0
        self._lose += 1

    @property
    def url(self):
        return self.get('url', '')

    @property
    def a(self):
        return self._pool.a(self.name, 'player/{0}'.format(self.url))

    @property
    def a_to_rate(self):
        return self._pool.a_with_current_labels(self.name, 'rate/{0}'.format(self.url))

    @property
    def name(self):
        return self.get('name', '')

    @property
    def patterns(self):
        return self.get('patterns', '')

    @property
    def unique_str(self):
        return self.get('unique_str', '')

    @property
    def link(self):
        return '<a href="/player/{0}">{1}</a>'.format(self.url, self.name)

    @property
    def win(self):
        if self._win is None:
            self._pool.sum_wl()

        return self._win or 0

    @property
    def lose(self):
        if self._win is None:
            self._pool.sum_wl()

        return self._lose or 0

    @property
    def sort_key(self):
        return -(self.win + self.lose)

    @property
    def participant_ids(self):
        return [pid for tf, pid in self._pool.player_to_participant.items() if tf[1] == self.id]

    @property
    def participants(self):
        return [
            self._pool.participants[t_participant]
            for t_player, t_participant
            in self._pool.player_to_participant.items() if t_player[1] == self.id
        ]

    @property
    def rank_dic(self):
        if not self._rank_dic:
            self._rank_dic = collections.Counter([p.final_rank for p in self.participants])

        return self._rank_dic

    @property
    def rank_sort(self):
        dic = self.rank_dic
        one = 1000000 * dic[1] if dic[1] else 0
        two = 10000 * dic[2] if dic[2] else 0
        three = 100 * dic[3] if dic[3] else 0
        return -(one + two + three) + self.sort_key

    def maybe(self, name: str):
        if self.name_matcher is None:
            self.name_matcher = NameMatcher(self)

        return self.name_matcher.maybe(name)

    @property
    def name_for_2bytes(self):
        uppers = [u for u in self.name if u.isupper()]
        if len(uppers) >= 2:
            return ''.join(uppers[:2])
        else:
            return self.name[:2]


class NameMatcher:
    def __init__(self, player: Player):
        self.player = player
        additional = self.player.patterns.split('\\') if len(self.player.patterns) != 0 else []
        self.pattern_re = re.compile(self.join_reg([self.player.url] + additional))
        self.unique_re = re.compile('([^a-z]|^){0}([^a-z]|$)'.format(self.player.unique_str.lower()))

    def normalize(self, txt):
        return re.sub('[/*_ .\'　|丨│︱]', '', txt.lower())

    def trim(self, txt):
        return '(^|\]){0}(\(|$|／|\[)'.format(txt)

    def separate_team_name(self, txt):
        spl = self.normalize(txt).split('|')
        if len(spl) != 2:
            reg_name = self.trim(re.escape(self.normalize(txt).lower()))
        else:
            s1 = re.escape(spl[0])
            s2 = re.escape(spl[1])
            tn = self.trim('{0}[ \(\)\|\.]*{1}'.format(s1, s2))
            nt = self.trim('{0}[ \(\)\|\.]*{1}'.format(s2, s1))
            reg_name = '{0}|{1}'.format(tn, nt)
        return reg_name

    def join_reg(self, patterns):
        return '|'.join([self.separate_team_name(p) for p in patterns])

    def maybe(self, name: str):
        if self.pattern_re.search(self.normalize(name)) is not None:
            return True

        if len(self.player.unique_str) == 0:
            return False

        # uniqueチェック
        # 削ったりせず、素で比べて連続した文字列じゃない状態で含まれてればOK
        ret = self.unique_re.search(name.lower())
        return ret is not None


class Standing(Row):
    @property
    def url(self):
        return self.get('url', '')

    @property
    def name(self):
        return self.get('name', '')

    @property
    def participants(self):
        return [s.strip() for s in self.get('participants', '').split(',')]


class RatingLog:
    def __init__(self, player, log):
        self.player = player
        self.log = log

    @property
    def tournaments(self):
        return [l[0] for l in self.log]

    def rate_at(self, start_dt, date):
        last_rate, last_date = RATE, start_dt
        for d in self.log:
            if d[0].end_at >= date:
                if d[0].end_at == date:
                    return d[1].rating
                else:
                    return int(
                        last_rate +
                        ((d[1].rating - last_rate) / ((d[0].end_at - last_date).days + 1)) *
                        (date - last_date).days
                    )
            else:
                last_rate, last_date = d[1].rating, d[0].end_at

        return last_rate

    def tournament_at(self, date):
        for d in self.log:
            if d[0].end_at == date:
                return d[0]
        return None

    def tournament_name_at(self, date):
        t = self.tournament_at(date)
        return t.name if t else ''

    def rank_at(self, date):
        t = self.tournament_at(date)
        if t is None:
            return ''

        p = t.participant_by_player(self.player.id)
        return '' if p is None else self.player.name + ' rank:' + str(p.final_rank)

