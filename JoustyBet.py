from flask import Flask, request, render_template, make_response
from flask_socketio import SocketIO, emit

import json
import logging
from profanity import profanity

from model.BetState import BettingBoard
from model.JoustConstants import PLAYER_COLORS
from model.player import Player

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet

        async_mode = 'eventlet'
    except ImportError(eventlet):
        pass

    if async_mode is None:
        try:
            from gevent import monkey

            async_mode = 'gevent'
        except ImportError(monkey):
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)


# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet

    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey

    monkey.patch_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' # don't tell anyone (or you'll be just another regret)
socketio = SocketIO(app, async_mode=async_mode, logger=True, cookie='session-resume')
thread = None

game = BettingBoard()

def handle_game_begin():
    logging.info("Closing bets!")
    game.close_bets()
    socketio.emit('close_bet', {}, namespace='/jousty', broadcast=True)


def handle_winner(data):
    winner = data['winner']
    logging.info("Got winner: %s", winner)
    game.deal_with_winner(winner)
    game.open_bets()
    socketio.emit('open_bet', {'previous_winner': winner}, namespace='/jousty', broadcast=True)


def decode_event(data):
    logging.info("Received event.  Raw JSON: %s", data)
    decoded = json.loads(data.decode('UTF-8'))
    event_type = decoded['type']

    if event_type == 'beginning':
        handle_game_begin()
    elif event_type == 'winner':
        handle_winner(decoded)

# END INCOMING HORSESHIT

# SOCKET IO ENDPOINTS


@socketio.on('connect', namespace='/jousty')
def socket_connect():
    print('client connect')
    emit('connection', {'session_id': request.sid})


@socketio.on('attempt_session_resume', namespace='/jousty')
def attempt_session_resume(payload):
    old_session_id = payload['session_id']
    logging.info("Attempting to resume session for old id %s", old_session_id)
    if game.player_exists(old_session_id):
        game.update_player_session(old_session_id, request.sid)
        player = game.players[request.sid]
        emit('resume_success', {'player': player.as_serializable_object(),
                                'bets_open': game.bets_open})
    else:
        emit('resume_failed', {'status': 'could not resume'})




@socketio.on('client_init', namespace='/jousty')
def client_init():
    pass


@socketio.on('signup', namespace='/jousty')
def signup(payload):
    username = payload['username']
    if profanity.contains_profanity(username):
        emit('join_fail', {'error': 'Your username has bad words in it'})
    elif len(username) > 32:
        emit('join_fail', {'error': 'Your username is too long'})
    elif game.player_exists(username):
        emit('join_fail', {'error': 'Username %s already exists' % username})
    else:
        p = Player(username, request.sid)
        game.add_player(p)
        emit('join_ok', {'status': 'ok', 'state': game.bets_open})


@socketio.on('vote', namespace='/jousty')
def vote(payload):
    logging.info('got vote for %s from %s', payload['guess'], request.sid)
    success = game.set_bet_on_player(request.sid, payload['guess'])
    if success:
        emit('bet_ok', {'guess': payload['guess']})
    else:
        emit('bet_fail', {'error': 'Something went wrong'})

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/kill-player', methods=['POST'])
def kill_player():
    decoded = json.loads(request.data.decode('UTF-8'))
    name = decoded['name']
    del game.players[name]
    return "killed"


@app.route('/post-game-event', methods=['POST'])
def post_game_event():
    decode_event(request.data)
    return "OK"


@app.route('/scoreboard')
def scoreboard():
    players = [v.as_serializable_object() for k, v in game.players.items()]
    if game.bets_open:
        game_state = "Accepting bets"
    else:
        game_state = "Not accepting bets"
    response = make_response(render_template('status.html', players=players, game_state=game_state, last_winner=game.last_winner))
    response.headers['Connection'] = 'close'
    return response


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    socketio.run(app, host='0.0.0.0')
