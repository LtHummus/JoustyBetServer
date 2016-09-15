import logging

class BettingBoard:
    def __init__(self):
        self.players = {}
        self.bets_open = True
        self.last_winner = None

    def open_bets(self):
        self.bets_open = True

    def close_bets(self):
        self.bets_open = False

    def player_exists(self, name):
        return name in self.players

    def add_player(self, player):
        self.players[player.session_id] = player

    def set_bet_on_player(self, player, guess):
        if not self.bets_open:
            return False
        try:
            self.players[player].set_bet(guess)
            return True
        except:
            return False


    def update_player_session(self, old_id, new_id):
        player = self.players[old_id]
        del self.players[old_id]
        self.players[new_id] = player
        player.session_id = new_id
        logging.info('updated %s to new session %s', old_id, new_id)


    def deal_with_winner(self, winner):
        self.last_winner = winner
        for key, value in self.players.items():
            value.check_winner(winner)
            value.reset()

    def remove_garbage(self):
        # TODO: remove inactive players here for some defintion
        #       of inactive
        pass

