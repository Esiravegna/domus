# -*- coding: utf-8 -*-
import pandas as pd
from numpy.linalg.linalg import LinAlgError
from statsmodels.tsa.arima_model import ARMA
from domus.utils.wind_processor import direction
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

    def _current_wind(self):
        """
        Gets the current wind direction from Influx
        :return: a string as an address. See direction in wind_processor.
        """
        query = "SELECT LAST(value) FROM wind_direction WHERE board='wunderground'"
        message = False
        try:
            rs = self.server.query(query)
            message = direction(list(rs.get_points(measurement='wind_direction'))[0]['last'])
        except ValueError:
            raise Exception("Unable to connect to the dataserver")
        return message

    def _pressure_trend(self,base_pressure = 1000):
        """
        Uses ARMA models to detect a trend of descending pressure
        :param base_pressure: the base pressure in order to improve change detection, 1000 millibars
        :return: a trend vaue between -1 and 1, 0 if undetermined, False on error.
        """
        query = "SELECT value as pressure FROM pressure WHERE board='wunderground' AND time >= now() - 4h"
        message = False
        try:
            rs = self.server.query(query)
            pres = pd.DataFrame([a_point['pressure']*1.0 for a_point in list(rs.get_points())],
                                    columns=['pressure'],
                                    index = [pd.to_datetime(a_point['time']) for a_point in list(rs.get_points())])
            try:
                forecast,_,confidence_interval = (ARMA(pres.apply(lambda row: row['pressure']-base_pressure,axis=1).pct_change().dropna(), (3, 0)).fit()).forecast(1)
                message = forecast[0]
            except (LinAlgError,ValueError):
                message = 0
        except ValueError:
            raise Exception("Unable to connect to the dataserver")
        return message

    def _wind_rotation(self, check_direction=180):
        """
        Uses ARMA models to forecast if the wind is rotating towards the check_direction parameter
        :param check_direction: the direction to detect rotation. Base is 180, south.
        :return: True if the check_direction is between the confidence interval returned.
        """
        self.log.debug("Calculating wind rotation")
        query = "SELECT value FROM wind_direction WHERE board='wunderground' AND time >= now() - 3h"
        message = False
        try:
            rs = self.server.query(query)
            directions = pd.DataFrame([a_direction['value']*1.0 for a_direction in list(rs.get_points())],
                                      columns=['direction'],
                                      index = [pd.to_datetime(a_direction['time']) for a_direction in list(rs.get_points())])
            forecast,_,confidence_interval = (ARMA(directions, (3, 0)).fit()).forecast(1)
            if check_direction*0.80 <= confidence_interval[0][0] <= check_direction * 1.2 or check_direction * 0.80 <= confidence_interval[0][1] <= check_direction * 1.2:
                message = True
        except ValueError:
            raise Exception("Unable to connect to the dataserver")
        return message

    def run(self):
        result = False
        self.log.debug("Getting current conditions")
        response = u""
        if self._current_wind() not in [u'SSE',u'S',u'SSW']:
            if self._wind_rotation():
                response += u"\nViento rotando al sur."
        if self._pressure_trend() < 0:
            response += u"\nPresión en baja."
        if response:
            log.debug("Tweeting condition : {}".format(response))
            result = self.twitter.tweet(response, to_friends=True)
        return result