import graphviz
import graphs as gr


def simplify(graph, n=4):
 
    stack = []
    while graph.vertices():
        verts = graph.vertices()
        for vert in verts:
            if len(graph._adjlist[vert]) < n:
                e = {vert:graph._adjlist[vert].copy()}
                stack.append(e)
                graph.remove_vertex(vert)
    return stack


def rebuild(graph, stack, colors):
    while stack:
        current = stack.pop()
        key = list(current.keys())[0]
        graph.add_vertex(key)
        for ver in current[key]:
            graph.add_edge(key,ver)
        neighbor_list = graph.neighbors(key)
        for color in colors:
            for vert in neighbor_list:
                if graph.get_vertex_value(vert) == color:
                    break
            else:
                graph.set_vertex_value(key, color)
                break

    return

def viz_color_graph(graph, colors):
    stack = simplify(graph, 3)
    rebuild(graph, stack, colors)
    #print(graph._valuelist)

    dot = graphviz.Graph()
    
    for v in graph.vertices():
        if graph.get_vertex_value(v) in colors:
            dot.node(str(v), style = 'filled', fillcolor = graph.get_vertex_value(v))
        dot.node(str(v))
    
    for (v, w) in graph.edges():
        dot.edge(str(v), str(w))

    dot.render(view=True)
    

def demo():
    G = gr.Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    viz_color_graph(G,['blue', 'green', 'red'])

if __name__ == '__main__':
    demo()