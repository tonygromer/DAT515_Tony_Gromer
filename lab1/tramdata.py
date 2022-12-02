import json
import sys
from math import cos, sqrt, radians
import os


def build_tram_stops(jsonobject):
    temp_dictionary = json.load(jsonobject)
    stop_dictionary = {}

    # Set each tramstop as key, and assign position as value
    for i in temp_dictionary:
        pos = temp_dictionary[i]['position']
        stop_dictionary[i] = {'lat':pos[0],'lon':pos[1]}
    #print(stop_dictionary)
    return(stop_dictionary)

def build_tram_lines(lines):
    temp_lines = lines.read()
    line_dictionary = {}
    time_dictionary = {}
    current_line = ''       # Keep track of which stop you are at

    text = [t for t in temp_lines.splitlines() if t !=''] # Remove empty '' from lines
    
    for i,line in enumerate(text):
        if line[0].isdigit():
            # If first character is a number create a new key with an empty list as value
           current_line = line.strip(':')
           line_dictionary[current_line] = []
        elif line[0].isalpha():
            # If the first character is something else, remove time and add it to current stop´s list
            s = remove_non_alpha(line)
            line_dictionary[current_line].append(s)
            
            if not s in time_dictionary:
                time_dictionary[s] = {}
            # Check that we are not on the end    
            if i < (len(text)-1) and text[i+1].split(':')[1] != '' and text[i].split(':')[1] != '':
                # Calculate time
                t = int(text[i+1].split(':')[1])-int(text[i].split(':')[1])
                time_dictionary[s].update({remove_non_alpha(text[i+1]): t})

    return line_dictionary, time_dictionary
    

def build_tram_network(tramstop, tramlines):
    # Open or create tramnetwork.json and write stops, lines and times dictionaries
    with open('tramnetwork.json', 'w') as tram_network:
        json_dict = {}
        with open(tramstop) as trams:
            json_dict["stops"] = build_tram_stops(trams)
        with open(tramlines) as traml:
            build_lines = build_tram_lines(traml)
            json_dict["lines"] = build_lines[0]
            json_dict["times"] = build_lines[1]

        json.dump(json_dict, tram_network, ensure_ascii=False, indent=4)
    
    return

def remove_non_alpha(line):
    # Help-function to remove non-alpha after last letter
    last_pos = 0
    for j in range(len(line)):
        if line[j].isalpha():
            last_pos = j
    s = line[0:last_pos+1]
    return s

def lines_via_stop(lines, stop):
    # If the stop exists in the line, add it to list
    connected_lines = [line for line in lines if stop in lines[line]]
    connected_lines.sort(key = int)
    return connected_lines

def lines_between_stops(lines, stop1, stop2):
    # If both stops exists in the line, add it to list
    connected_lines = [line for line in lines if ((stop1 in lines[line]) and (stop2 in lines[line]))]
    if connected_lines:
        return connected_lines

def time_between_stops(lines, times, line, stop1, stop2):
    # list of stops in line
    line_list = lines[line]
    # Index of stops in the line
    i_stop1 = line_list.index(stop1)
    i_stop2 = line_list.index(stop2)

    # check the order of the stops, and if they are not as in the list, swap
    if i_stop2 < i_stop1:
        i_stop2, i_stop1 = i_stop1, i_stop2
    time = 0

    # Save the first stop, then add the time for each stop along the line
    prev_stop = line_list[i_stop1]
    for stop in line_list[i_stop1+1:i_stop2+1]:
        time += times[prev_stop][stop]
        prev_stop = stop
        
    return time

def distance_between_stops(stops, stop1, stop2):
    stop1_pos = stops[stop1]
    stop2_pos = stops[stop2]

    # delta latitude and longitude
    d_phi = radians(float(stop2_pos['lat'])-float(stop1_pos['lat']))
    d_lambda = radians(float(stop2_pos['lon'])-float(stop1_pos['lon']))
    # mean latitude
    phi_m = radians((float(stop2_pos['lat'])+float(stop1_pos['lat']))/2)
    
    R = 6371 #km
    d = R*sqrt(d_phi**2 + (cos(phi_m)*d_lambda)**2)
    
    return d   

def answer_query(tramdict, query):
    # answer_query recieves entire tramnetwork
    # Splits query into words to find index for words
    split_query = query.split()
    
    # Cases for different inputs. Uses " ".join() to reassemble multiple-word stops.
    # Calls appropiate function. 
    if split_query[0] == 'via':
    
        stop = " ".join(split_query[1:len(split_query)])
        l = lines_via_stop(tramdict['lines'], stop)
        if l:
            return l
        else:
            return None  

    elif split_query[0] == 'between':
        stop1 = " ".join(split_query[1:split_query.index('and')])
        stop2 = " ".join(split_query[split_query.index('and')+1:len(split_query)])

        l = lines_between_stops(tramdict['lines'], stop1, stop2)
        if l:
            return l
        else:
            return None
        
    elif split_query[0:2] == ['time', 'with']:
        line = split_query[2]
        stop1 = " ".join(split_query[4:split_query.index('to')])
        stop2 = " ".join(split_query[split_query.index('to')+1:len(split_query)])
        t = time_between_stops(tramdict['lines'], tramdict['times'], line, stop1, stop2)
        if t:
            return t
        else:
            return None

    elif split_query[0:2] == ['distance', 'from']:
        stop1 = " ".join(split_query[2:split_query.index('to')])
        stop2 = " ".join(split_query[split_query.index('to')+1:len(split_query)])
        d = distance_between_stops(tramdict['stops'], stop1, stop2)
        if d:
            return d
        else:
            return None

    else:
        return False 
    

def dialogue(jsonfile):
    with open(jsonfile) as json_file:
        tram_network = json.load(json_file)

    while True:
        query = input('>')
        if query == 'quit':
            quit()
        
        
        ans = answer_query(tram_network, query)
        if ans:
            print(ans)
        elif ans == None: 
            print("unknown paramter")
        else:
            print("sorry, try again")


dirname = os.path.dirname(__file__)
tramstop_dir = os.path.join(dirname, './data/tramstops.json')
tramline_dir = os.path.join(dirname, './data/tramlines.txt')

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(tramstop_dir, tramline_dir)

    else:
        dialogue('tramnetwork.json')			


