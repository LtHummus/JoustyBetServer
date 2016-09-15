from flask import Flask, request
import json

from model.BetState import BettingBoard
from model.JoustConstants import PLAYER_COLORS
from model.player import Player

app = Flask(__name__)

game = BettingBoard()


# I AM LAZY SO ALL THE INCOMING HORSESHIT IS HERE

def handle_game_begin():
    game.close_bets()


def handle_winner(data):
    winner = data['winner']
    game.deal_with_winner(winner)
    game.open_bets()


def decode_event(data):
    decoded = json.loads(data.decode('UTF-8'))
    event_type = decoded['event']

    if event_type == 'gamestart':
        handle_game_begin()
    elif event_type == 'winner':
        handle_winner(decoded)

# END INCOMING HORSESHIT


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/post-game-event', methods=['POST'])
def post_game_event():
    decode_event(request.data)
    return "OK"


@app.route('/player-signup', methods=['POST'])
def player_signup():
    decoded = json.loads(request.data.decode('UTF-8'))
    name = decoded['name']
    p = Player(name)
    game.add_player(p)
    print("Adding player named '{}'".format(name))
    return "OK"


@app.route('/register-bet', methods=['POST'])
def register_bet():
    decoded = json.loads(request.data.decode('UTF-8'))
    name = decoded['name']
    guess = decoded['guess']
    if guess not in PLAYER_COLORS:
        return "Bad player" #TODO: make this return a non-200 error code

    if not game.bets_open:
        return "Can't bet when bets are closed"

    game.players[name].set_bet(guess)
    return "OK"


@app.route('/debug')
def debug():
    print("Players:")
    for k, v in game.players.items():
        print(v.debug_dump())
    return "OK"


if __name__ == '__main__':
    app.run()
