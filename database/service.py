from database.common import Table, CustomQueries
from model import Pool


def select_by_tournament_id(challo_url):
    fg_tournament = Table('fg_tournament').select_one('challo_url = %s', (challo_url,))
    tournament_id = fg_tournament['id']
    return fg_tournament, {
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


def select_by_player_url(player_url):
    fg_player = Table('fg_player').select_one('url = %s', (player_url,))
    challo_match = CustomQueries.select_matches_by_player(fg_player['id'])
    challo_participant = Table('challo_participant').select_in(
        'id', [cm['player1_id'] for cm in challo_match] + [cm['player2_id'] for cm in challo_match]
    )
    return fg_player['id'], {
        'fg_player':
            Table('fg_player').select_all(),
        'challo_participant':
            challo_participant,
        'challo_match':
            challo_match,
        'fg_tournament':
            Table('fg_tournament').select_all(),
        'challo_group':
            Table('challo_group').select_all(),
    }


def select_for_players():
    return {
        'fg_player': Table('fg_player').select_all(),
        'challo_participant': Table('challo_participant').select_all()
    }


def select_for_create_rel():
    return {
        'fg_player': Table('fg_player').select_all(),
        'challo_participant': Table('challo_participant').select_all()
    }


def select_for_create_vs():
    return {
        'fg_player': Table('fg_player').select_all(),
        'challo_match': Table('challo_match').select_all(),
        'challo_participant': Table('challo_participant').select_all(),
    }


def select_for_vs_table(standing_url):
    standing = Pool.Standing(None, Table('fg_standing').select_one('url = %s', (standing_url,)))
    return standing, {
        'fg_tournament': Table('fg_tournament').select_all(),
        'fg_player': Table('fg_player').select_in('url', standing.participants),
        'challo_match': CustomQueries.select_matches_by_players(standing.participants),
        'challo_participant': CustomQueries.select_participants_by_players(standing.participants),
        'challo_group': Table('challo_group').select_all(),
    }


def select_for_tournaments():
    return {
        'fg_tournament': Table('fg_tournament').select_all(),
    }


def select_for_vs(p1, p2):
    player_1 = Table('fg_player').select_one('url = %s', (p1,))
    player_2 = Table('fg_player').select_one('url = %s', (p2,))
    challo_participant = Table('challo_participant').select_in('player_id', [player_1['id'], player_2['id']])
    challo_match = (CustomQueries.select_matches_by_player(player_1['id']) +
                    CustomQueries.select_matches_by_player(player_2['id']))

    ps = [(p['tournament_id'], p['id']) for p in challo_participant]
    cut_match = [
        m for m in challo_match if
        (m['tournament_id'], m['player1_id']) in ps and
        (m['tournament_id'], m['player2_id']) in ps
    ]
    return player_1['id'], player_2['id'], {
        'fg_player':
            [player_1, player_2],
        'challo_participant':
            challo_participant,
        'challo_match':
            cut_match,
        'fg_tournament':
            Table('fg_tournament').select_all(),
        'challo_group':
            Table('challo_group').select_all(),
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
