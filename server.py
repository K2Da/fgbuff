import config
import json
from util.server import cache, support_datetime_default
from database import service
from bottle import Bottle, run, template, request, response, debug, static_file
from model.Pool import Pool

app = Bottle()
debug(config.debug)


@app.route('/players')
@app.route('/players/labels/<labels:path>')
@cache
def players(labels=None):
    return template('players', pool=Pool.init_for_players(labels))


@app.route('/tournaments')
@app.route('/tournaments/labels/<labels:path>')
@cache
def tournaments(labels=None):
    return template('tournaments', pool=Pool.init_for_tournaments(labels))


@app.route('/tournament/<challo_url>')
@cache
def tournament(challo_url):
    tournament_id, pool = Pool.init_for_tournament(challo_url)
    return template('tournament', pool=pool, tournament_id=tournament_id)


@app.route('/vs/<p1>/<p2>')
@app.route('/vs/<p1>/<p2>/labels/<labels:path>')
@cache
def vs(p1, p2, labels=None):
    p1_id, p2_id, pool = Pool.init_for_vs(p1, p2, labels)
    return template('vs', pool=pool, p1=p1_id, p2=p2_id)


@app.route('/player/<player_url>')
@app.route('/player/<player_url>/labels/<labels:path>')
@cache
def player(player_url, labels=None):
    player_id, pool = Pool.init_for_player(player_url, labels)
    return template('player', pool=pool, player_id=player_id)


@app.route('/standing/<standing_url>')
@app.route('/standing/<standing_url>/labels/<labels:path>')
@cache
def standing(standing_url, labels=None):
    s, pool = Pool.init_for_standing(standing_url, labels)
    return template('standing', pool=pool, standing=s)


@app.route('/ratings')
@app.route('/ratings/labels/<labels:path>')
@cache
def ratings(labels=None):
    _, pool = Pool.init_for_ratings(labels=labels)
    return template('ratings', pool=pool)


@app.route('/rate/<player_and_labels:path>')
@cache
def rate(player_and_labels=None):
    player_urls, pool = Pool.init_for_ratings(player_and_labels=player_and_labels)
    return template('rate', pool=pool, player_urls=player_urls)


@app.route('/vstable')
@cache
def vstable():
    s, pool = Pool.init_for_standing('cpt-finals-2016', None)
    return template('standing', pool=pool, standing=s)


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/')
@cache
def index():
    return template('index', count=service.select_match_count())


@app.route('/edit/<url>')
def tournament_edit(url):
    return template('edit', title='edit', url=url)


@app.route('/api/tournament/<url>')
def tournament_api(url):
    response.set_header('Content-Type', 'application/json')
    _, pool = service.select_by_tournament_id(url)
    return json.dumps(pool, default=support_datetime_default)


@app.post('/api/update')
def tournament_update():
    try:
        data = request.json
        service.update_tournament(data)
    except Exception as ex:
        print(ex)
        return u'NG'

    return u'OK'


@app.post('/api/comment/read')
def comment_read():
    response.set_header('Content-Type', 'application/json')
    return json.dumps(service.select_comments(request.json), default=support_datetime_default)


@app.post('/api/comment/write')
def comment_write():
    service.insert_comment(request.json)
    return 'OK'


if __name__ == '__main__':
    run(app, host=config.host, port=config.port)
