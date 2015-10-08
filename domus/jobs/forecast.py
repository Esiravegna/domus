# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import datetime
from emoji import emojize
from domus.utils.logger import master_log
log = master_log.name(__name__)

RAIN_THRESHOLD = {
    u'no llueve': (0, 40),
    emojize(u'llueve :umbrella:'): (75, 100),
    u'puede llover': (40, 74)
    }
#See
#http://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary&MR=1
CONDITION_TO_EMOJI ={
    u'chanceflurries': u':snowflake:',
    u'chancerain': u':umbrella:',
    u'chancesleet': u':snowflake:',
    u'chancesnow':u':snowflake:',
    u'chancetstorms':u':zap:',
    u'clear':u':sunny:',
    u'cloudy':u':cloudy:',
    u'flurries':u':snowflake:',
    u'fog':u':foggy:',
    u'hazy':u':foggy:',
    u'mostlycloudy':u':cloud:',
    u'mostlysunny':u':sunny:',
    u'partlycloudy':u':cloud:',
    u'partlysunny':u':sunny:',
    u'sleet':u':sonwflake:',
    u'rain':u':umbrella:',
    u'snow':u':snowflake:',
    u'sunny':u':sunny:',
    u'tstorms':u':zap:',
    u'unknown':u':interrobang:',
    u'cloudy':u':cloud:'}


class Forecast(object):
    """
    A simple forecast that tweets the day that will do today, tomorrow and the rest of the day
    based on the wunderground board
    """
    def __init__(self, data_server, twitter_client):
        """
        :param data_server: Current influxdb server
        :param twitter_client: Twitter interface to do da magic
        :return:
        """
        self.server = data_server
        self.twitter = twitter_client
        log.debug("Forecast class created")

    def __forecast_to_message(self, threshold, when=0, measurement='rain_forecast'):
        """
        translates the rain forecast to actual sentences based on the RAIN_THRESHOLD constant below
        :param threshold a dict of {'message':(upper,lower)} used to generate the message
        :param when: 0 for today 1, for tomorrow and so on
        :param measurement The measurement to be queried, rain_forecast as the default.
        :return: a proper twitteable string.
        """
        query = "SELECT value FROM {}".format(measurement) +\
                " WHERE board='wunderground' AND forecast_for = '{dt.year}-{dt.month}-{dt.day}' " \
                " ORDER BY time desc LIMIT 1".format( dt=datetime.datetime.now() + datetime.timedelta(days=when))
        message = False
        try:
            rs = self.server.query(query)
            forecast = list(rs.get_points(measurement=measurement))[0]['value']
            for key, value in threshold.iteritems():
                if value[0] <= forecast <= value[1]:
                    message = key + u" ({}%)".format(forecast)
                    break
        except ValueError:
            raise Exception("Unable to connect to the dataserver")
        return message

    def __min_max_message(self, when=0):
        """
        translates the min/max temperature to a readble tweet
        :param when: 0 for today, 1 for tomorrow and so on
        :return: a proper twittable string
        """
        measurements =[]
        for measurement in ['max', 'min']:
            query = "SELECT value FROM {}".format(measurement) +\
                    " WHERE board='wunderground' AND forecast_for = '{dt.year}-{dt.month}-{dt.day}' " \
                    " ORDER BY time desc LIMIT 1".format(dt=datetime.datetime.now() + datetime.timedelta(days=when))
            try:
                rs = self.server.query(query)
                measurements.append(list(rs.get_points(measurement=measurement))[0]['value'])
            except ValueError:
                raise Exception("Unable to connect to the dataserver")
        message = emojize(":arrow_up:{}°/:arrow_down:{}°".format(measurements[0],measurements[1]),use_aliases=True)
        return message

    def __condition(self,when=0):
        """
        Converts the condition parameter in wunderground to an emoji
        when: 0 for today, 1 for tomorrow and so on
        :return: a proper twittable string
        """
        query = "SELECT value FROM cond" +\
                " WHERE board='wunderground' AND forecast_for = '{dt.year}-{dt.month}-{dt.day}' " \
                " ORDER BY time desc LIMIT 1".format(dt=datetime.datetime.now() + datetime.timedelta(days=when))
        cond = False
        try:
            rs = self.server.query(query)
            cond =  emojize(CONDITION_TO_EMOJI[list(rs.get_points(measurement='cond'))[0]['value']])
        except ValueError:
            raise Exception("Unable to connect to the dataserver")
        return cond

    def run(self):
        result = False
        current_time = datetime.datetime.now().hour
        log.debug("Getting forecast")
        rain = [self.__forecast_to_message(RAIN_THRESHOLD), self.__forecast_to_message(RAIN_THRESHOLD, when=1)]
        condition = [self.__condition(),self.__condition(when=1)]
        temp = [self.__min_max_message(),self.__min_max_message(when=1)]
        tweet_response = u"Hoy "
        log.debug("Tweeting forecast")
        tweet_response = tweet_response + u"{0}.Se esperan {1} y {2}.".format(rain[0], temp[0], condition[0])
        tweet_response = tweet_response + u"\nMañana {0}.Se esperan {1} y {2}.".format(rain[0], temp[0], condition[0])
        result = self.twitter.tweet(tweet_response, to_friends=True)
        return result