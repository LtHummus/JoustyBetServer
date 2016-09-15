import logging

class Player:
    def __init__(self, name, session_id):
        logging.info("Adding player with name %s and sid %s", name, session_id)
        self.name = name
        self.score = 0
        self.streak = 0
        self.current_bet = None
        self.last_seen = None # TODO: deal with this bullshit later
        self.session_id = session_id

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

    def as_serializable_object(self):
        return {
            'name': self.name,
            'score': self.score,
            'streak': self.streak,
            'current_bet': self.current_bet,
            'session_id': self.session_id
        }

    def debug_dump(self):
        return """
        Name = {}
        Score = {}
        Streak = {}
        Current Bet = {}
        Session ID = {}

        """.format(self.name, self.score, self.streak, self.current_bet, self.session_id)