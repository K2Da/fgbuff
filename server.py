from bottle import Bottle, run, template
from model.Pool import Pool

app = Bottle()


@app.route('/players')
def players():
    return template('players', pool=Pool.init_for_players())


@app.route('/tournaments')
def tournaments():
    return template('tournaments', pool=Pool.init_for_tournaments())


@app.route('/tournament/<challo_url>')
def tournament(challo_url):
    fg_tournament, pool = Pool.init_for_tournament(challo_url)
    return template('tournament', pool=pool, fg_tournament=fg_tournament)


@app.route('/vs/<p1>/<p2>')
def vs(p1, p2):
    p1_id, p2_id, pool = Pool.init_for_vs(p1, p2)
    return template('vs', pool=pool, p1=p1_id, p2=p2_id)


@app.route('/player/<player_url>')
def player(player_url):
    player_id, pool = Pool.init_for_player(player_url)
    return template('player', pool=pool, player_id=player_id)


@app.route('/')
def index():
    return template('index')

run(app, host='localhost', port=8080)
