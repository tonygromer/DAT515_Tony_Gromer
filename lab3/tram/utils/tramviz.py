# visualization of shortest path in Lab 3, modified to work with Django
import time
from .trams import readTramNetwork
from .graphs import dijkstra
import os
from .color_tram_svg import color_svg_network
from django.conf import settings #type: ignore

def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code
    network = readTramNetwork()

    # TODO: replace this mock-up with actual computation using dijkstra.
    # First you need to calculate the shortest and quickest paths, by using appropriate
    # cost functions in dijkstra().
    # Then you just need to use the lists of stops returned by dijkstra()
    
    # If you do Bonus 1, you could also tell which tram lines you use and where changes
    # happen. But since this was not mentioned in lab3.md, it is not compulsory.
    Bonus1 = True
    
    if Bonus1:
        network.specialize_stops_to_lines()
        
        dep_list = [stop for stop in network.vertices() if stop[0] == dep]
        dest_list = [stop for stop in network.vertices() if stop[0] == dest]
        paths_time = []
        paths_dist = []

        for stop1 in dep_list:
            for stop2 in dest_list:
                time_dij = dijkstra(network, stop1, network.specialized_transition_time)[stop2]
                dist_dij = dijkstra(network, stop1, network.specialized_geo_distance)[stop2]
                paths_time.append(time_dij)
                paths_dist.append(dist_dij)

        quickest = min(paths_time, key = lambda x: x['dist'])
        shortest = min(paths_dist, key = lambda x:x['dist'])
        
        quickest_list = [stop[0] for stop in quickest['path']]
        shortest_list = [stop[0] for stop in shortest['path']]

        timepath = 'Quickest: ' + ', '.join(quickest_list) + ', ' + str(quickest['dist']) + ' minutes'
        geopath = 'Shortest: ' + ', '.join(shortest_list) + ', ' + str(round(shortest['dist'],3)) + ' km'

    else:
        time_dij = dijkstra(network,dep, network.transition_time)[dest]
        dist_dij = dijkstra(network, dep, network.geo_distance)[dest]

        quickest = time_dij['path']
        shortest = dist_dij['path']
        
        timepath = 'Quickest: ' + ', '.join(quickest) + ', ' + str(time_dij['dist']) + ' minutes'
        geopath = 'Shortest: ' + ', '.join(shortest) + ', ' + str(dist_dij['dist']) + ' km'

    def colors(v):
        if v in shortest_list and v in quickest_list:
            return 'cyan'
        elif v in quickest_list:
            return 'orange'
        elif v in shortest_list:
            return 'green'
        else:
            return 'white'
                

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors) # type: ignore
    # return the path texts to be shown in the web page
    return timepath, geopath