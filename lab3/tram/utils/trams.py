import json

# imports added in Lab3 version
import math
import os
from .graphs import WeightedGraph
from .tramdata import lines_between_stops, time_between_stops, distance_between_stops, lines_via_stop
from django.conf import settings #type: ignore
from itertools import combinations


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

    def geo_distance(self, u,v):
        return distance_between_stops(self._stopdict,u,v)

    def line_stops(self, line):
        return self._linedict[line]

    def stop_lines(self, a):
        return lines_via_stop(self._linedict, a)

    def stop_position(self, a):
        return self._stopdict[a]

    def transition_time(self, u, v):
        lines_between = lines_between_stops(self._linedict, u, v)
        time_between = []
        for line in lines_between: #type: ignore
            time_between.append(time_between_stops(self._linedict, self._timedict, line, u, v))
        
        return min(time_between)


# Bonus task 1: take changes into account and show used tram lines

    def specialize_stops_to_lines(self):
        # TODO: write this function as specified
        verts = set()
        edgelist = []
        for line in self._linedict:
            l = self._linedict[line]
            for i in range(len(l)-1):
                p1 = l[i]
                p2 = l[i+1]
                edgelist.append(((p1, line), (p2,line)))
                verts.add((p1, line))
                verts.add((p2,line))
        for v1 in verts:
            for v2 in verts:
                if v1[0] == v2[0] and v1[1] != v2[1]:
                    edgelist.append((v1,v2))

        
        weightlist = {}
        """
        for stop1 in self._timedict:
            for stop2 in self._timedict[stop1]:
                w = self._timedict[stop1][stop2]
                stop1_temp, stop2_temp = stop1, stop2
                if stop1 > stop2:
                    stop1_temp, stop2_temp = stop2, stop1
                    
                weightlist[(stop1_temp, stop2_temp)] = w
        """
        """
        for edge in edgelist:
            vert1 = edge[0]
            vert2 = edge[1]
            
            weightlist[edge] = self.specialized_transition_time(vert1,vert2)
        """

        start_list = {'edgelist': edgelist, 'weight': weightlist}
        super().__init__(start_list)

        return self


    def specialized_transition_time(self, u, v, changetime=10):
        # TODO: write this function as specified
    
        if u[0] == v[0] and u[1] != v[1]:
            return changetime
        
        try:
            return self._timedict[u[0]][v[0]]
        except:
            return self._timedict[v[0]][u[0]]


    def specialized_geo_distance(self, u, v, changedistance=0.02):
        # TODO: write this function as specified
        if u[0] == v[0] and u[1] != v[1]:
            return changedistance

        return distance_between_stops(self._stopdict,u[0],v[0])



def readTramNetwork(file = TRAM_FILE):
    with open(file) as json_file:
        tram_network = json.load(json_file)
        return TramNetwork(tram_network['lines'], tram_network['stops'], tram_network['times'])