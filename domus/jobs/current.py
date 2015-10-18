# -*- coding: utf-8 -*-
import datetime
from emoji import emojize
from domus.utils.wind_processor import direction,angle_difference
from domus.utils.logger import master_log
log = master_log.name(__name__)


class CurrentConditions(object):
    """
    A current condition processor and alert emitter.
    Initially, its designed to react to wind and temperature changes.
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
        self.log = master_log.name(__name__)
        self.log.debug("CurrentCondition class created")

    def _assess_wind(self):
        query = "select value from wind_direction where time >= now() - 1h;"
        message = False
        try:
            rs = self.server.query(query)
            forecast = list(rs.get_points(measurement=measurement))[0]['last']
            for key, value in threshold.iteritems():
                if value[0] <= forecast <= value[1]:
                    message = key + u" ({}%)".format(forecast)
                    break
        except ValueError:
            raise Exception("Unable to connect to the dataserver")
        return message
