import sys
sys.path.append('../lab1/')
import tramdata as td
import graphs

class TramStop:
    def __init__(self, name, lines = None, lat = None, lon = None):
        if lines:
            self._lines = lines
        else:
            self._lines = []
        self._name = name
        if lat and lon:
            self._position = (lat, lon)
        else:
            self._position = ()

    def add_line(self, line):
        self._lines.append(line)

    def get_lines(self):
        return self._lines
    
    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position = (lat, lon)


class TramLine:
    def __init__(self, num, stops):
        self._number = num
        self._stops = stops

    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops

class TramNetwork(graphs.WeightedGraph):
    def __init__(self, lines, stops, times):
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times

    def all_lines(self):
        return self._linedict

    def all_stops(self):
        return self._stopdict

    def extreme_positions(self):
        return 'a'

    def geo_distance(self, a,b):
        return 'a'

    def line_stops(self, line):
        return 'a'

    def stop_lines(self, a):
        return 'a'

    def stop_position(self, a):
        return 'a'

    def transition_time(self, a, b):
        return 'a'

# in trams.py
def readTramNetwork(file='tramnetwork.json'):
    print('a')