# -*- coding: utf-8 -*-
import datetime
from emoji import emojize
RAIN_THRESHOLD = {
    u'es improbable que llueva': (0, 40),
    emojize(u'va a llover :umbrella:'): (75, 100),
    u'puede llover': (40, 74)
    }


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
                " ORDER BY time desc LIMIT 1".format(dt=datetime.datetime.now() + datetime.timedelta(days=when))
        message = False
        try:
            rs = self.server.query(query)
            forecast = list(rs.get_points(measurement=measurement))[0]['value']
            for key, value in threshold.iteritems():
                if value[0] <= forecast <= value[1]:
                    message = key
                    break
        except ValueError:
            raise Exception("Unable to connect to the dataserver")
        return message

    def __call__(self):
        result = False
        current_time = datetime.datetime.now().hour
        today = self.__forecast_to_message(RAIN_THRESHOLD)
        tomorrow = self.__forecast_to_message(RAIN_THRESHOLD, when=1)
        if today and tomorrow:
            tweet_response = u"Hoy " if current_time <= 12 else u"Esta tarde "
            tomorrow = "lo mismo" if today == tomorrow else tomorrow
            tweet_response = tweet_response + u"{}. Mañana, {}".format(today,tomorrow)
            result = self.twitter.tweet(tweet_response)
        return result
