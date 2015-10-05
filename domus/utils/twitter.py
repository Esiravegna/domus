from twython import Twython
from config import TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET

class Tweety(object):

    def __init__(self,
                app_key=TWITTER_APP_KEY,
                 app_secret=TWITTER_APP_SECRET,
                 oauth_token=TWITTER_OAUTH_TOKEN,
                 oauth_token_secret=TWITTER_OAUTH_SECRET):

        self.twitter = Twython(app_key,
                               app_secret,
                               oauth_token,
                               oauth_token_secret)

    def tweet(self, message):
        self.twitter.update_status(status=message[:140] + (message[138:] and '..'))