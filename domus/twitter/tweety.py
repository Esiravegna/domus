import json
from twython import Twython
from twython import TwythonError,TwythonAuthError,TwythonRateLimitError
from domus.utils.config import TWITTER_APP_KEY,TWITTER_APP_SECRET,TWITTER_OAUTH_TOKEN,\
    TWITTER_OAUTH_SECRET,REDIS_DATABASE,REDIS_SERVER,REDIS_PORT
from domus.utils.cache import RedisCache

class Tweety(object):
    """
    Twitter client using Twython
    """

    def __init__(self, app_key=TWITTER_APP_KEY, app_secret=TWITTER_APP_SECRET,
                 oauth_token=TWITTER_OAUTH_TOKEN, oauth_token_secret=TWITTER_OAUTH_SECRET):
        try:
            self.twitter = Twython(
            app_key,
            app_secret,
            oauth_token,
            oauth_token_secret)
            self.cache = RedisCache({
            'server': REDIS_SERVER,
            'port': REDIS_PORT,
            'database': REDIS_DATABASE,
            'key_prefix': 'domus-twitter'
            })
        except TwythonAuthError:
            raise Exception("Unable to connect to twitter")

    def __get_friends(self):
        """
        Using twitter get_friends and redis, gets a list of screen names
        :return:a list of twitter users
        """
        results = self.cache.get('twitter_friends')
        if not results:
            try:
                results = [a['screen_name'] for a in self.twitter.get_friends_list()['users']]
                self.cache.store('twitter_friends',json.dumps(results), expires=120)
            except (TwythonError, TwythonRateLimitError):
                raise Exception('Unable to get followers list')
        else:
            results = json.loads(results)
        return results

    def tweet(self, message,to_friends=False):
        """
        Writtes a twit
        :param message: what to tweet
        :param to_friends: send to all friends?
        :return:
        """
        try:
            if to_friends:
                for a_friend in self.__get_friends():
                    mention = "@{} ".format(a_friend)
                    available_chars = 140 - len(mention)
                    self.twitter.update_status(
                        status=(mention+message)[:available_chars] + ((mention+message)[(available_chars-2):] and '..'))
            else:
                self.twitter.update_status(
                        status=message[:140] + (message[138:] and '..'))
        except (TwythonError, TwythonRateLimitError):
            raise Exception("Unable to post update")

    def dm(self, user, message):
        try:
            self.twitter.send_direct_message(screen_name=user, text=message)
        except TwythonError:
            raise Exception("Unable to send dm to {}".format(user))

    def get_dms(self):
        """
        Gets a list of dms. Stores the last id seen so the next request is for the new messages only.
        :return: a dict of the form {tweet_id:{sender:screen_name,text:the_message}}
        """
        results = {}
        dms = []
        last_id = self.cache.get('twitter_last_dm')
        if last_id:
            dms = self.twitter.get_direct_messages(count=100,since_id = last_id)
        else:
            dms = self.twitter.get_direct_messages(count=100)
        if dms:
            last_id = 0
            for a_dm in dms:
                results[a_dm['id']] = {'from':a_dm['sender_screen_name'],'text': a_dm['text']}
                last_id = a_dm['id'] if a_dm['id'] > last_id else last_id
            self.cache.store('twitter_last_dm', last_id)
        return results

    def get_mentions(self):
        """
        Gets a list of mentions.  Stores the last id seen so the next request is for the new messages only.
        :return: a dict of the form {tweet_id:{sender:screen_name,text:the_message}}
        """
        results = {}
        mentions = []
        last_id = self.cache.get('twitter_last_mention')
        if last_id:
            mentions = self.twitter.get_mentions_timeline(count=100,since_id = last_id)
        else:
            mentions = self.twitter.get_mentions_timeline(count=100)
        if mentions:
            last_id = 0
            for a_mention in mentions:
                results[a_mention['id']] = {'from':a_mention['user']['screen_name'],'text': a_mention['text']}
                last_id = a_mention['id'] if a_mention['id'] > last_id else last_id
            self.cache.store('twitter_last_mention', last_id)
        return results