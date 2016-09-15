
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.streak = 0
        self.current_bet = None
        self.last_seen = None # TODO: deal with this bullshit later

    def increment_score(self):
        self.score += 1
        self.streak += 1

    def reset_streak(self):
        self.streak = 0

    def set_bet(self, guess):
        self.current_bet = guess
        self.last_seen = None # TODO: still dealing with it

    def check_winner(self, winner):
        if winner == self.current_bet:
            self.score += 1
            self.streak += 1
        else:
            self.streak = 0

    def reset(self):
        self.current_bet = None

    def debug_dump(self):
        return """
        Name = {}
        Score = {}
        Streak = {}
        Current Bet = {}

        """.format(self.name, self.score, self.streak, self.current_bet)