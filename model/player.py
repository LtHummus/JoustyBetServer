import logging
import datetime

INACTIVITY_LIMIT = 30 * 60  # 30 minutes in seconds


class Player:
    def __init__(self, name, session_id):
        logging.info("Adding player with name %s and sid %s", name, session_id)
        self.name = name
        self.score = 0
        self.streak = 0
        self.current_bet = None
        self.last_seen = datetime.datetime.now()
        self.session_id = session_id
        self.number_bets = 0

    def increment_score(self):
        self.score += 1
        self.streak += 1

    def reset_streak(self):
        self.streak = 0

    def set_bet(self, guess):
        self.current_bet = guess
        self.touch()

    def check_winner(self, winner):
        self.number_bets += 1

        if winner == self.current_bet:
            self.score += 1
            self.streak += 1
        else:
            self.streak = 0

    def reset(self):
        self.current_bet = None

    def as_serializable_object(self):
        return {
            'id': self.session_id,
            'name': self.name,
            'score': self.score,
            'streak': self.streak,
            'current_bet': self.current_bet,
            'session_id': self.session_id,
            'number_bets': self.number_bets
        }

    def touch(self):
        self.last_seen = datetime.datetime.now()

    def should_be_cleaned_up(self):
        time_since_last_seen = datetime.datetime.now() - self.last_seen
        return time_since_last_seen.seconds > INACTIVITY_LIMIT

    def as_hexicube_string(self):
        return "player %s %s %s %s %s %s" % (self.session_id, self.score, self.streak, self.current_bet, self.number_bets, self.name)

    def debug_dump(self):
        return """
        Name = {}
        Score = {}
        Streak = {}
        Current Bet = {}
        Session ID = {}

        """.format(self.name, self.score, self.streak, self.current_bet, self.session_id)