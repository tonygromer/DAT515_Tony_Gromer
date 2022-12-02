import unittest
from tramdata import *

TRAM_FILE = './tramnetwork.json'
ORG_LINES = './data/tramlines.txt'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']
        
        with open(ORG_LINES) as lines:
            self.tram_lines = lines.read()
        

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    # add your own tests here

    def test_lines_exist_from_original(self):
        org_lines = {line for line in self.tram_lines if line[0].isdigit()}
        for line in org_lines:
            self.assertIn(line, self.tram_lines, msg = line + ' does not exist in original file')

 
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



    def test_feasible_distance(self):
        max_dist = 0

        for i,stop in enumerate(self.stopdict):
            for j,stops in enumerate(self.stopdict, i):
                dist = distance_between_stops(self.stopdict, stop, stops)
                max_dist = max(max_dist, dist)

        self.assertTrue(max_dist < 20, msg = 'Distance greater than 20 km')

    
    def test_dialouge(self):
        tramdict = {'stops':self.stopdict, 'lines':self.linedict, 'times':self.timedict}
        # test line via stop
        sort = True
        for stop in self.stopdict:
            query = 'via ' + stop
            via = answer_query(tramdict, query)
            if via != sorted(via, key = int):  # type: ignore
                sort = False
        self.assertTrue(sort, msg = 'Not all lists are sorted')
        
        sort = True
        # test lines between stop
        
        for stop1 in self.stopdict:
            for stop2 in self.stopdict:
                query = 'between ' + stop1 + ' and ' + stop2
                between = answer_query(tramdict, query)
                if between and (between != sorted(between, key = int)):  # type: ignore
                    sort = False
        self.assertTrue(sort, msg = 'Not all lists are sorted')
        
        # test time between stop
        for line in self.linedict:
            for i,stop1 in enumerate(self.linedict[line]):
                for stop2 in self.linedict[line][i:len(self.linedict[line])]:
                    query_f = 'time with ' + line + ' from ' + stop1 + ' to ' + stop2
                    query_b = 'time with ' + line + ' from ' + stop2 + ' to ' + stop1
                    time_forwards = answer_query(tramdict, query_f)
                    time_backwards = answer_query(tramdict, query_b)

                    self.assertEqual(time_forwards, time_backwards, msg = 'Time from A to B is not equal to B to A')

        return


if __name__ == '__main__':
    unittest.main()

