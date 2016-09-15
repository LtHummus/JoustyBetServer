
class BettingBoard:
    def __init__(self):
        self.players = {}
        self.bets_open = True

    def open_bets(self):
        self.bets_open = True

    def close_bets(self):
        self.bets_open = False

    def add_player(self, player):
        self.players[player.name] = player

    def deal_with_winner(self, winner):
        for key, value in self.players.items():
            value.check_winner(winner)
            value.reset()

    def remove_garbage(self):
        # TODO: remove inactive players here for some defintion
        #       of inactive
        pass

