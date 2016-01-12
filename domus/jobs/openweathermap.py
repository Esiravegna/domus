#!/usr/bin/env python
import urllib2
import json
from domus.utils.logger import master_log


class Openweathermap(object):

    def __init__(self, data_server):
        self.log = master_log.name(__name__)
        self.server = data_server
        self.data_points = []
        self.log.debug("Openweathermap class created")

    def run(self):
        field = 'cloud_coverage'
        current = urllib2.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?id=3860259&appid=2de143494c0b295cca9337e1e96b00e0')
        json_string = current.read()
        parsed_json = json.loads(json_string)
        try:
            measurement_value = float(parsed_json['clouds']['all'])/100
        except ValueError:
            measurement_value = float(parsed_json['clouds']['all'].strip('%'))/100
        self.log.debug("{} written".format(field)) if self.server.add_datapoint(field, measurement_value, 'openweathermap') else None
        current.close()
