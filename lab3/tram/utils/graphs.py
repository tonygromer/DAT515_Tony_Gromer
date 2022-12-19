import graphviz

class Graph:
    def __init__(self, edgelist = None):
        self._adjlist = dict()
        self._valuelist = dict()

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
        return list(self._adjlist.keys())
    
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

    def add_edge(self, a, b):
        if a in self._adjlist:
            self._adjlist[a].append(b)
        else:
            self._adjlist[a] = [b]
        if b in self._adjlist:
            self._adjlist[b].append(a)
        else:
            self._adjlist[b] = [a]

    def remove_edge(self,a,b):
        if b in self._adjlist[a]:
            self._adjlist[a].remove(b)
        if a in self._adjlist[b]:
            self._adjlist[b].remove(a)



class WeightedGraph(Graph):
    def __init__(self, startlist = None):
        self._weightlist: dict
        if startlist:
            self._weightlist = startlist['weight']
            super().__init__(startlist['edgelist'])

    def get_weight(self, vertex1, vertex2):
        return self._weightlist[(vertex1, vertex2)]

    def set_weight(self, vertex1, vertex2, weight):
        if vertex1 > vertex2:
            vertex1, vertex2 = vertex2, vertex1
        self._weightlist[(vertex1, vertex2)] = weight
    


# in graphs.py
def dijkstra(graph, source, cost=lambda u,v: 1.0):
    
    shortest_paths = {}
    prev = {}
    dist = {}
    Q =[]


    for v in graph.vertices():
        dist[v] = float('inf')
        prev[v] = None
        Q.append(v)
        shortest_paths[v] = [source]
    dist[source] = 0

    while Q:
        d2 = {v:dist[v] for v in dist if v in Q}
        u =  min(d2, key = d2.get)  # type: ignore
        Q.remove(u)
        neighbours = [node for node in graph.neighbors(u) if node in Q]
        for v in neighbours:
            alt = dist[u] + cost(u,v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                shortest_paths[v] = shortest_paths[u] + [v]
    ret_list = {}
    for v in graph.vertices():
        ret_list[v] = {'path':shortest_paths[v], 'dist': dist[v]}

    return ret_list
    
    
def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot'):
    dot = graphviz.Graph()

    for v in graph.vertices():
        if str(v) in nodecolors:
            dot.node(str(v), color = nodecolors[str(v)])
        dot.node(str(v))

    for (v, w) in graph.edges():
        dot.edge(str(v), str(w))

    dot.render(view=True)

    
def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]['path']
    colormap = {str(v): 'pink' for v in path}
    print('this is colormap ', colormap)
    visualize(G, view='view', nodecolors=colormap)

