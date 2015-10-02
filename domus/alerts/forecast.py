THRESHOLDS =

class Forecast(object):
    """
    A simple forecast that tweets the day that will do today, tomorrow and the rest of the day
    based on the wunderground board
    """
    def __init__(self, interval):
        """
        :param interval:
        :return:
        """
        self.interval = interval
        pass
    def __call__(self, data_server,twitter_client):

        pass

