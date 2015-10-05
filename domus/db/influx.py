from copy import deepcopy

from influxdb import InfluxDBClient
from domus.utils.config import INFLUX_DB_PASSWORD,INFLUX_DB_PORT,INFLUX_DB_SERVER,INFLUX_DB_TABLE,INFLUX_DB_USER
from utils.logger import master_log

"""
An standard datapoint object
"""
DATAPOINT = {
    'measurement': 'label',
    'tags': {'board': ''},
    'fields': {
        'value': 0.0}}



class DataServer(object):
    """
    An influx db abstraction
    """
    def __init__(self,server = INFLUX_DB_SERVER,
                 port = INFLUX_DB_PORT,
                 table = INFLUX_DB_TABLE,
                 user = INFLUX_DB_USER,
                 passwd = INFLUX_DB_PASSWORD):
        """
        Standard construction. The parameters should be in the environment.
        See utils.config.py
        :param server: Host
        :param port: Port, default to 8086
        :param table: table to be used
        :param user: username
        :param passwd: password
        :return:
        """
        self.log = master_log.name(__name__)

        try:
            self.log.debug("Connecting to" + server)
            self.server = InfluxDBClient(server, port, user, passwd, table)
            self.log.debug("Connected to" + server)
        except Exception as e:
            reason = str(e)
            raise Exception("Unable to connect to {}:{} with {}.{}".format(server, port, user, reason))

    def add_datapoint(self, measurement,value,  board, tags=None):
        datapoint = deepcopy(DATAPOINT)
        datapoint['measurement'] = measurement
        datapoint['fields']['value'] = value
        datapoint['tags']['board'] = board
        if tags and isinstance(tags,dict):
            for tag, value in tags.iteritems():
                datapoint['tags'][tag] = value
        try:
            self.log.debug("Writting to InfluxDB: {}-{}".format(measurement,value))
            result = self.server.write_points([datapoint])
        except Exception as e:
            reason = str(e)
            raise Exception("Unable to write {} due to {}".format(datapoint, reason))
        return result

    def query(self,query):
        return self.server.query(query)
