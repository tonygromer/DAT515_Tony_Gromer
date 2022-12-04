import graphviz
import networkx

class Graph:
    def __init__(self, edgelist = None):
        self._adjlist = dict()
        self._valuelist =  dict()

        if edgelist:
            for edge in edgelist:
                if edge[0] in self._adjlist:
                    self._adjlist[edge[0]].append(edge[1])
                else:
                    self._adjlist[edge[0]] = [edge[1]]
                if edge[1] in self._adjlist:
                    self._adjlist[edge[1]].append(edge[0])
                else:
                    self._adjlist[edge[1]] = [edge[0]]


    def neighbors(self,vertex):
        return self._adjlist[vertex]
    
    def vertices(self):
        return self._adjlist.keys()
    
    def edges(self):
        edges = []
        for ver1 in self._adjlist:
            for ver2 in self._adjlist[ver1]:
                if not ((ver1, ver2) in edges or (ver2, ver1) in edges):
                    edges.append((ver1, ver2))

        return edges
    
    def __len__(self):
        return len(self._adjlist)
    
    def add_vertex(self, vertex):
        self._adjlist[vertex] = []

    def remove_vertex(self, vertex):
        self._adjlist.pop(vertex, None)
        self._valuelist.pop(vertex, None)

    def get_vertex_value(self, vertex):
        return self._valuelist[vertex]

    def set_vertex_value(self, vertex, value):
        self._valuelist[vertex] = value


class WeightedGraph(Graph):
    def __init__(self, startlist = None):
        super().__init__()
        self._weightlist: dict
        if startlist:
            self._weightlist = startlist

    def get_weight(self, vertex1, vertex2):
        return self._weightlist[(vertex1, vertex2)]

    def set_weight(self, vertex1, vertex2, weight):
        if vertex1 > vertex2:
            vertex1, vertex2 = vertex2, vertex1
        self._weightlist[(vertex1, vertex2)] = weight
    


# in graphs.py
def dijkstra(graph, source, cost=lambda u,v: 1):
    """
    shortest_paths = {}
    prev = {}
    dist = {}
    Q =[]


    for v in graph.vertices():
        dist[v] = float('inf')
        prev[v] = None
        Q.append(v)
        shortest_paths[v] = []
    dist[source] = 0
       
    while Q:
        d2 = {v:dist[v] for v in dist if v in Q}
        u =  min(d2, key = dist.get)
        Q.remove(u)
        
        neighbours = [node for node in graph.neighbors(u) if node in Q]
        for v in neighbours:
            alt = dist[u] + cost(u,v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                shortest_paths[v] = shortest_paths[u]
    print(shortest_paths)
    ret_list = {'path':}
    return ret_list
    """
    def costs2attributes(G, cost, attr='weight'):
        for a, b in G.edges():
            G[a][b][attr] = cost(a, b)
    return networkx.shortest_path(graph, source=None, target=None, weight=None, method='dijkstra')

    
def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot'):
    dot = graphviz.Graph()

    for v in graph.vertices():
        dot.node(str(v))

    for (v, w) in graph.edges():
        dot.edge(str(v), str(w))

    dot.render(view=True)

    
def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]['path']
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)

def demo():
    G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo()