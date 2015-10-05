from twython import Twython
from settings import app_key, app_secret, oauth_token, oauth_token_secret


class Tweety(object):

    def __init__(self, app_key=app_key, app_secret=app_secret,
                 oauth_token=oauth_token, oauth_token_secret=oauth_token_secret):
        self.twitter = Twython(
            app_key,
            app_secret,
            oauth_token,
            oauth_token_secret)

    def tweet(self, message):
        self.twitter.update_status(
            status=message[:140] + (message[138:] and '..'))

