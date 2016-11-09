import config
import json
from util.server import cache, support_datetime_default
from database import service
from bottle import Bottle, run, template, request, response, debug, static_file
from model.Pool import Pool

app = Bottle()
debug(True)


@app.route('/players')
def players():
    return cache(request.path, template('players', pool=Pool.init_for_players()))


@app.route('/tournaments')
def tournaments():
    return cache(request.path, template('tournaments', pool=Pool.init_for_tournaments()))


@app.route('/tournament/<challo_url>')
def tournament(challo_url):
    fg_tournament, pool = Pool.init_for_tournament(challo_url)
    return cache(request.path, template('tournament', pool=pool, fg_tournament=fg_tournament))


@app.route('/vs/<p1>/<p2>')
def vs(p1, p2):
    p1_id, p2_id, pool = Pool.init_for_vs(p1, p2)
    return cache(request.path, template('vs', pool=pool, p1=p1_id, p2=p2_id))


@app.route('/player/<player_url>')
def player(player_url):
    player_id, pool = Pool.init_for_player(player_url)
    return cache(request.path, template('player', pool=pool, player_id=player_id))


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/')
def index():
    return template('index')


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


if __name__ == '__main__':
    run(app, host=config.host, port=config.port)
