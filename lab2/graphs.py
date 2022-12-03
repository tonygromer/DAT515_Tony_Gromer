class Graph:
    def __init__(self, edgelist = None):
        self._adjlist: dict
        self._valuelist: dict

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
    shortest_paths = {}
    prev = {}
    dist = {}
    Q =[]


    for v in graph.vertices():
        dist[v] = float('inf')
        prev[v] = None
        Q.append(v)
    dist[source] = 0
       
    while Q:
        #u = vertex in Q with min dist[u]
        #Q.remove(u)
          
        for v in u.neighbor() in Q:
            alt = dist[u] + graph.edges(u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev
    
def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot'):
    print('a')