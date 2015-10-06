#!/usr/bin/env python
import urllib2
import json

from domus.db.influx import DataServer
from domus.utils.logger import master_log

log = master_log.name(__name__)
data_points = []
current_dataset = {
    'temp': 'temp_c',
    'pressure': 'pressure_mb',
    'humidity': 'relative_humidity',
    'feelslike': 'feelslike_c',
    'wind_direction': 'wind_degrees',
    'wind_speed': 'wind_kph'
}

server = DataServer()

current = urllib2.urlopen(
    'http://api.wunderground.com/api/9fe997a4e78bd9cc/conditions/q/zmw:00000.1.87344.json')
json_string = current.read()
parsed_json = json.loads(json_string)

for field, value in current_dataset.iteritems():
    try:
        measurement_value = float(parsed_json['current_observation'][value])
    except ValueError:
        measurement_value = float(parsed_json['current_observation'][value].strip('%'))
    log.debug("{} written".format(field)) if server.add_datapoint(field, measurement_value, 'wunderground') else None

current.close()
forecast = urllib2.urlopen(
    'http://api.wunderground.com/api/9fe997a4e78bd9cc/forecast/q/zmw:00000.1.87344.json')
parsed_forecast = json.loads(forecast.read())
for a_forecast in parsed_forecast['forecast']['simpleforecast']['forecastday']:
    forecast_for =  "{}-{}-{}".format(
            a_forecast['date']['year'],
            a_forecast['date']['month'],
            a_forecast['date']['day'])
    log.debug("Rain forecast written") if server.add_datapoint('rain_forecast', float(a_forecast['pop']), 'wunderground', tags={"forecast_for": forecast_for}) else None
    log.debug("Max forecast written") if server.add_datapoint('max', float(a_forecast['high']['celsius']), 'wunderground', tags={"forecast_for": forecast_for}) else None
    log.debug("Min forecast written") if server.add_datapoint('min', float(a_forecast['low']['celsius']), 'wunderground', tags={"forecast_for": forecast_for}) else None
forecast.close()