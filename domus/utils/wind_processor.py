"""
Just a wind processor. Given the wind direction in degrees returns a cardinal number. Also
"""
DIRECTIONS = {u'N':(0,11.25),
            u'NNE':(11.25,33.75),
            u'NE':(33.75,56.25),
            u'ENE':(56.25,78.75),
            u'E':(78.75,101.25),
            u'ESE':(101.25,123.75),
            u'SE':(123.75,146.25),
            u'SSE':(146.25,168.75),
            u'S':(168.75,191.25),
            u'SSW':(191.25,213.75),
            u'SW':(213.75,236.25),
            u'WSW':(236.25,258.75),
            u'W':(258.75,281.25),
            u'WNW':(281.25,303.75),
            u'NW':(303.75,326.25),
            u'NNW':(326.25,348.75),
            u'N':(348.75,360)
            }

def direction(direction):
    """
    Cardinal slabels from address in degrees
    :param direction: 0 to 360
    :return: N, S, and so on
    """
    for key, value in DIRECTIONS.iteritems():
        if value[0] >= direction <= value[1]:
            return key


def angle_difference(angle, reference=180):
    """
    Angular distance
    :param angle: the angle to be tested
    :param reference: 180 by default
    :return: the difference
    """
    return 180 - abs(abs(reference - angle) - 180)
