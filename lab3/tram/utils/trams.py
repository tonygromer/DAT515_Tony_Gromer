import json

# imports added in Lab3 version
import math
import os
from .graphs import WeightedGraph
import tramdata as td
from django.conf import settings


# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here
TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')


class TramNetwork(WeightedGraph):
    def __init__(self, lines, stops, times):
        edgelist = []
        for line in lines:
            l = lines[line]
            for i in range(len(l)-1):
                edgelist.append((l[i+1], l[i]))

        weightlist = {}
        for stop1 in times:
            for stop2 in times[stop1]:
                w = times[stop1][stop2]
                stop1_temp, stop2_temp = stop1, stop2
                if stop1 > stop2:
                    stop1_temp, stop2_temp = stop2, stop1
                
                weightlist[(stop1_temp, stop2_temp)] = w

        
        start_list = {'edgelist': edgelist, 'weight': weightlist}

        super().__init__(start_list) # type: ignore
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times

    def all_lines(self):
        return self._linedict

    def all_stops(self):
        return self._stopdict

    def extreme_positions(self):
        lat = []
        lon = []
        
        for stop in self._stopdict:
            lat.append(self._stopdict[stop]['lat'])
            lon.append(self._stopdict[stop]['lon'])

        return min(lon), min(lat), max(lon), max(lat)

    def geo_distance(self, a,b):
        return td.distance_between_stops(self._stopdict,a,b)

    def line_stops(self, line):
        return self._linedict[line]

    def stop_lines(self, a):
        return td.lines_via_stop(self._linedict, a)

    def stop_position(self, a):
        return self._stopdict[a]

    def transition_time(self, a, b):
        lines_between = td.lines_between_stops(self._linedict, a, b)
        time_between = []
        for line in lines_between: #type: ignore
            time_between.append(td.time_between_stops(self._linedict, self._timedict, line, a, b))
        
        return min(time_between)


def readTramNetwork(file = TRAM_FILE):
    with open(file) as json_file:
        tram_network = json.load(json_file)
        return TramNetwork(tram_network['lines'], tram_network['stops'], tram_network['times'])


# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance


