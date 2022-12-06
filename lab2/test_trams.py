import unittest
from hypothesis import given, strategies as st
from trams import *

TRAM_FILE = '../lab1/tramnetwork.json'
ORG_LINES = '../lab1/data/tramlines.txt'


class TestTrams(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']
        
        
        """
         with open(ORG_LINES) as lines:
            self.tram_lines = lines.read()
        """
       
    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    # add your own tests here
    """
    def test_lines_exist_from_original(self):
        org_lines = {line for line in self.tram_lines if line[0].isdigit()}
        for line in org_lines:
            self.assertIn(line, self.tram_lines, msg = line + ' does not exist in original file')
    """
    
    """
    def test_stops_exist_from_original(self):
        line_dictionary = {}
        current_line = ''       # Keep track of which stop you are at

        text = [t for t in self.tram_lines.splitlines() if t !=''] # Remove empty '' from lines
    
        for line in text:
            if line[0].isdigit():
            # If first character is a number create a new key with an empty list as value
                current_line = line.strip(':')
                line_dictionary[current_line] = []
            elif line[0].isalpha():
            # If the first character is something else, remove time and add it to current stop´s list
                s = remove_non_alpha(line)
                line_dictionary[current_line].append(s)
        self.assertDictEqual(line_dictionary, self.linedict)
    """

    """
    def test_feasible_distance(self):
        max_dist = 0

        for i,stop in enumerate(self.stopdict):
            for j,stops in enumerate(self.stopdict, i):
                dist = distance_between_stops(self.stopdict, stop, stops)
                max_dist = max(max_dist, dist)

        self.assertTrue(max_dist < 20, msg = 'Distance greater than 20 km')
    """
    

if __name__ == '__main__':
    unittest.main()



# if (a,b) in edges, then a,b in vertices

#if a has b as neighbour, b has a as neighbour

# shortest from a -> b is shortest from b->a

# breadth first

# depth first

