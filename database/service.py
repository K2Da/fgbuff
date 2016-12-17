from database.common import Table, CustomQueries, TranQueries


def select_by_tournament_id(challo_url):
    fg_tournament = Table('fg_tournament').select_one('challo_url = %s', (challo_url,))
    tournament_id = fg_tournament['id']
    return tournament_id, {
        'base_url': 'tournament/{0}'.format(challo_url),
        'fg_tournament':
            [fg_tournament],
        'fg_player':
            Table('fg_player').select_all(),
        'challo_participant':
            Table('challo_participant').select('tournament_id = %s', (tournament_id,)),
        'challo_match':
            Table('challo_match').select('tournament_id = %s', (tournament_id,)),
        'challo_group':
            Table('challo_group').select('tournament_id = %s', (tournament_id,))
    }


def select_by_player_url(player_url, labels):
    fg_player = Table('fg_player').select_one('url = %s', (player_url,))
    label_list, tournaments = CustomQueries.select_tournamets_with_labels(labels)
    challo_match = CustomQueries.select_matches_by_player(fg_player['id'], tournaments)
    challo_participant = Table('challo_participant').select_in(
        'tournament_id', [t['id'] for t in tournaments]
    )
    return fg_player['id'], {
        'base_url': 'player/{0}'.format(player_url),
        'fg_player':
            Table('fg_player').select_all(),
        'challo_participant':
            challo_participant,
        'challo_match':
            challo_match,
        'fg_tournament':
            tournaments,
        'challo_group':
            Table('challo_group').select_all(),
        'labels':
            label_list,
    }


def select_for_players(labels):
    label_list, tournaments = CustomQueries.select_tournamets_with_labels(labels)
    return {
        'base_url': 'players',
        'challo_participant': Table('challo_participant').select_in('tournament_id', [t['id'] for t in tournaments]),
        'fg_player': Table('fg_player').select_all(),
        'challo_match': Table('challo_match').select_in('tournament_id', [t['id'] for t in tournaments]),
        'labels': label_list,
    }


def select_for_create_rel():
    return {
        'fg_player': Table('fg_player').select_all(),
        'fg_tournament': Table('fg_tournament').select_all(),
        'challo_participant': Table('challo_participant').select_all()
    }


def select_for_ratings(player_and_labels=None, labels=None):
    if player_and_labels:
        split = player_and_labels.split('/labels/') if player_and_labels is not None else ['']
        players, labels = split[0], (split[1] if len(split) > 1 else None)
        base_url = 'rate/' + players
    else:
        players = ''
        base_url = 'ratings'

    label_list, tournaments = CustomQueries.select_tournamets_with_labels(labels)
    return players.split('/'), {
        'base_url': base_url,
        'fg_tournament': tournaments,
        'fg_player': Table('fg_player').select_all(),
        'challo_match': Table('challo_match').select_in('tournament_id', [t['id'] for t in tournaments]),
        'challo_participant': Table('challo_participant').select_in('tournament_id', [t['id'] for t in tournaments]),
        'labels': label_list,
    }


def select_for_vs_table(standing_url, labels):
    label_list, tournaments = CustomQueries.select_tournamets_with_labels(labels)
    standing = Table('fg_standing').select_one('url = %s', (standing_url,))
    urls = [s.strip() for s in standing['participants'].split(',')]
    return standing, {
        'base_url': 'standing/{0}'.format(standing_url),
        'fg_tournament': tournaments,
        'fg_player': Table('fg_player').select_in('url', urls),
        'challo_match': CustomQueries.select_matches_by_players(urls, tournaments),
        'challo_participant': CustomQueries.select_participants_by_players(urls),
        'challo_group': Table('challo_group').select_all(),
        'labels': label_list,
    }


def select_for_tournaments(labels):
    label_list, tournaments = CustomQueries.select_tournamets_with_labels(labels)
    participants = Table('challo_participant').select('final_rank = %s', (1,))
    players = Table('fg_player').select_in('id', [p['player_id'] for p in participants])
    return {
        'base_url': 'tournaments',
        'fg_tournament': tournaments,
        'challo_participant': participants,
        'fg_player': players,
        'labels': label_list,
    }


def select_for_vs(p1, p2, labels):
    player_1 = Table('fg_player').select_one('url = %s', (p1,))
    player_2 = Table('fg_player').select_one('url = %s', (p2,))
    label_list, tournaments = CustomQueries.select_tournamets_with_labels(labels)
    challo_participant = Table('challo_participant').select_in('player_id', [player_1['id'], player_2['id']])
    challo_match = (CustomQueries.select_matches_by_player(player_1['id'], tournaments) +
                    CustomQueries.select_matches_by_player(player_2['id'], tournaments))

    ps = [(p['tournament_id'], p['id']) for p in challo_participant]
    cut_match = [
        m for m in challo_match if
        (m['tournament_id'], m['player1_id']) in ps and
        (m['tournament_id'], m['player2_id']) in ps
    ]
    return player_1['id'], player_2['id'], {
        'base_url': 'vs/{0}/{1}'.format(p1, p2),
        'fg_player':
            [player_1, player_2],
        'challo_participant':
            challo_participant,
        'challo_match':
            cut_match,
        'fg_tournament':
            tournaments,
        'challo_group':
            Table('challo_group').select_all(),
        'labels':
            label_list,
    }


def update_tournament(data):
    tournament = data['fg_tournament'][0]
    p = Table('challo_participant')
    m = Table('challo_match')
    g = Table('challo_group')
    p.delete('tournament_id = %s', (tournament['id'],))
    m.delete('tournament_id = %s', (tournament['id'],))
    g.delete('tournament_id = %s', (tournament['id'],))
    for r in data['challo_participant']:
        p.insert_with_dictionary(r)

    for r in data['challo_match']:
        m.insert_with_dictionary(r)

    for r in data['challo_group']:
        g.insert_with_dictionary(r)


def insert_comment(data):
    TranQueries.insert_comment(data['page_url'], data['text'])


def select_comments(data):
    return TranQueries.select_comments(data['page_url'])


def select_match_count():
    return CustomQueries.select_match_count()[0]['cnt']

