import sys
sys.path.append('../lab1/')
import tramdata as td
import graphs
import json

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

        super().__init__(start_list)
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

        return {'lat':[max(lat), min(lat)], 'lon':[max(lon), min(lon)]}

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
        for line in lines_between:
            time_between.append(td.time_between_stops(self._linedict, self._timedict, line, a, b))
        
        return min(time_between)

# in trams.py
def readTramNetwork(file='../lab1/tramnetwork.json'):
    with open(file) as json_file:
        tram_network = json.load(json_file)
        return TramNetwork(tram_network['lines'], tram_network['stops'], tram_network['times'])

def demo():
    G = readTramNetwork()
    
    a, b = input('from,to ').split(',')
    graphs.view_shortest(G, a, b)

if __name__ == '__main__':
    demo()