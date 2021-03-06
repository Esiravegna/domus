import urllib2
import json
from domus.utils.logger import master_log


class Wunderground(object):

    def __init__(self, data_server):
        self.log = master_log.name(__name__)
        self.server = data_server
        self.data_points = []
        self.current_dataset = {
            'temp': 'temp_c',
            'pressure': 'pressure_mb',
            'humidity': 'relative_humidity',
            'feelslike': 'feelslike_c',
            'wind_direction': 'wind_degrees',
            'wind_speed': 'wind_kph'
        }
        self.log.debug("Wunderground worker created")

    def run(self):
        current = urllib2.urlopen(
            'http://api.wunderground.com/api/9fe997a4e78bd9cc/conditions/q/zmw:00000.1.87344.json')
        json_string = current.read()
        parsed_json = json.loads(json_string)

        for field, value in self.current_dataset.iteritems():
            try:
                measurement_value = float(parsed_json['current_observation'][value])
            except ValueError:
                measurement_value = float(parsed_json['current_observation'][value].strip('%'))
        current.close()
        forecast = urllib2.urlopen('http://api.wunderground.com/api/9fe997a4e78bd9cc/forecast/q/zmw:00000.1.87344.json')
        parsed_forecast = json.loads(forecast.read())
        for a_forecast in parsed_forecast['forecast']['simpleforecast']['forecastday']:
            forecast_for = "{}-{}-{}".format(
                    a_forecast['date']['year'],
                    a_forecast['date']['month'],
                    a_forecast['date']['day'])
            self.log.debug("Rain forecast written") if self.server.add_datapoint('rain_forecast', float(a_forecast['pop']), 'wunderground', tags={"forecast_for": forecast_for}) else None
            self.log.debug("Max forecast written") if self.server.add_datapoint('max', float(a_forecast['high']['celsius']), 'wunderground', tags={"forecast_for": forecast_for}) else None
            self.log.debug("Min forecast written") if self.server.add_datapoint('min', float(a_forecast['low']['celsius']), 'wunderground', tags={"forecast_for": forecast_for}) else None
            self.log.debug("Condition written") if self.server.add_datapoint('cond', (a_forecast['icon']), 'wunderground', tags={"forecast_for": forecast_for}) else None
        forecast.close()
