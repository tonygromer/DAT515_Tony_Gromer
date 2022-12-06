import unittest
from trams import *
from collections import deque 

TRAM_FILE = '../lab1/tramnetwork.json'
ORG_LINES = '../lab1/data/tramlines.txt'


class TestTrams(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']
        
        self.G = TramNetwork(self.linedict, self.stopdict, self.timedict) 
        
        """
         with open(ORG_LINES) as lines:
            self.tram_lines = lines.read()
        """
       
    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}

        for stop in stopset:
            self.assertIn(stop, self.G.vertices(), msg = stop + ' not in TramNetwork')


    def test_lines_exist(self):
        for line in self.linedict:
            self.assertIn(line, self.G.all_lines(), msg = line + ' does not exist in TramNetwork')



    def test_stops_exist_from_original(self):
        for stop in self.stopdict:
            self.assertIn(stop, self.G.vertices())

    def test_connectedness(self):
        connected_stops = BFS(self.G, 'Chalmers')
        for stop in self.stopdict:
            self.assertIn(stop, connected_stops, msg = stop + ' not connected to the rest of the network')

def BFS(G, node, goal=lambda n: False):
    Q = deque()
    explored = [node]
    Q.append(node)
    while Q:
        v = Q.popleft()
        if goal(v):
            return v
        for w in G.neighbors(v):
            if w not in explored:
                explored.append(w)
                Q.append(w)
    return explored


if __name__ == '__main__':
    unittest.main()
