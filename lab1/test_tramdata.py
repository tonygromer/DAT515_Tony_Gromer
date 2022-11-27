import unittest
from tramdata import *

TRAM_FILE = './tramnetwork.json'
ORG_LINES = './data/tramlines.txt'
ORG_STOPS = './data/tramstops.json'


class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
        
        with open(ORG_LINES) as lines:
            self.tram_lines = lines.read()
        
        with open(ORG_STOPS) as stops:
            self.tram_stops = json.loads(stops.read())

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    # add your own tests here
    # ^ above test_stops_exists() test functions 1,2,3.
    def test_lines_exist_from_original(self):
        org_lines = {line for line in self.tram_lines if line[0].isdigit()}
        for line in org_lines:
            self.assertIn(line, self.tram_lines, msg = line + ' does not exist in original file')


    def test_stops_extist_from_original(self):
        org_stops = {}
        return

    def test_feasible_distance(self):
        return


if __name__ == '__main__':
    unittest.main()

