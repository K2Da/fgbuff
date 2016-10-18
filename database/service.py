from database.common import Table


def select_by_tournament_id(challo_url):
    fg_tournament = Table('fg_tournament').select_one('challo_url = %s', (challo_url,))
    challo_id = fg_tournament['challo_id']
    return fg_tournament, {
        'fg_tournament':
            [fg_tournament],
        'fg_player':  # TODO 削る
            Table('fg_player').select_all(),
        'challo_tournament':
            Table('challo_tournament').select('id = %s', (challo_id,)),
        'challo_participant':
            Table('challo_participant').select('tournament_id = %s', (challo_id,)),
        'challo_match':
            Table('challo_match').select('tournament_id = %s', (challo_id,)),
        'challo_group':
            Table('challo_group').select('tournament_id = %s', (challo_id,)),
        'rel_player':
            Table('rel_player').select('tournament_id = %s', (challo_id,))
    }


def select_by_player_url(player_url):
    fg_player = Table('fg_player').select_one('url = %s', (player_url,))
    rel_player = Table('rel_player').select('fg_id = %s', (fg_player['id'],))
    challo_participant = Table('challo_participant').select_in('id', [rp['challo_id'] for rp in rel_player])
    cm = Table('challo_match')
    cp_ids = [cp['id'] for cp in challo_participant]
    challo_match = cm.select_in('player1_id', cp_ids) + cm.select_in('player2_id', cp_ids)
    challo_participant = Table('challo_participant').select_in(
        'id', [cm['player1_id'] for cm in challo_match] + [cm['player2_id'] for cm in challo_match]
    )
    rel_player = Table('rel_player').select_in('challo_id', [cp['id'] for cp in challo_participant])
    return fg_player['id'], {
        'fg_player':
            Table('fg_player').select_all(),
        'rel_player':
            rel_player,
        'rel_vs':
            Table('rel_vs').select('player_id = %s', (fg_player['id'],)),
        'challo_participant':
            challo_participant,
        'challo_match':
            challo_match,
        'fg_tournament':
            Table('fg_tournament').select_all(),
        'challo_group':
            Table('challo_group').select_all(),
        'challo_tournament':
            Table('challo_tournament').select_all()
    }


def select_for_players():
    return {
        'fg_player': Table('fg_player').select_all(),
        'rel_player': Table('rel_player').select_all()
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
        'rel_player': Table('rel_player').select_all()
    }


def select_for_tournaments():
    return {
        'fg_tournament': Table('fg_tournament').select_all(),
        'challo_tournament': Table('challo_tournament').select_all()
    }


def select_for_vs(p1, p2):
    player_1 = Table('fg_player').select_one('url = %s', (p1,))
    player_2 = Table('fg_player').select_one('url = %s', (p2,))
    rel_player = Table('rel_player').select_in('fg_id', [player_1['id'], player_2['id']])
    challo_participant = Table('challo_participant').select_in('id', [rp['challo_id'] for rp in rel_player])
    cm = Table('challo_match')
    cp_ids = [cp['id'] for cp in challo_participant]
    challo_match = cm.select_in('player1_id', cp_ids) + cm.select_in('player2_id', cp_ids)

    ps = [p['id'] for p in challo_participant]
    cut_match = [
        m for m in challo_match if m['player1_id'] in ps and m['player2_id'] in ps
    ]
    return player_1['id'], player_2['id'], {
        'fg_player':
            [player_1, player_2],
        'rel_player':
            rel_player,
        'challo_participant':
            challo_participant,
        'challo_match':
            cut_match,
        'fg_tournament':
            Table('fg_tournament').select_all(),
        'challo_group':
            Table('challo_group').select_all(),
        'challo_tournament':
            Table('challo_tournament').select_all()
    }
