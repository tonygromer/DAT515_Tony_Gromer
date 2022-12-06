
from hypothesis import given, strategies as st
from graphs import *
# if (a,b) in edges, then a,b in vertices

# generate small integers, 0...10
smallints = st.integers(min_value=0, max_value=10)
# generate pairs of small integers
twoints = st.tuples(smallints, smallints)
# generate lists of pairs of small integers
# where x != y for each pair (x, y)
st_edge_list = st.lists(twoints, unique_by=(lambda x: x[0], lambda x: x[1]))


@given(st_edge_list)
def test_edges_and_vertices(eds):
    G = Graph()
    verts = set()
    for (a,b) in eds:
        G.add_edge(a,b)
        verts.add(a)
        verts.add(b)

    assert all(v in verts for v in G.vertices())
    

# if a has b as neighbour, b has a as neighbour
@given(st_edge_list)
def test_neighbours(eds):
    G = Graph()
    for (a,b) in eds:
        G.add_edge(a,b)
    verts = G.vertices()
    for v in verts:
        for u in G.neighbors(v):
            assert v in G.neighbors(u)


# shortest from a -> b is shortest from b->a
@given(st_edge_list)
def test_a_b(eds):
    G = Graph()
    for (a,b) in eds:
        G.add_edge(a,b)
    cost=lambda u,v: 1
    for (a,b) in eds:
        ab = dijkstra(G, a, cost, )[b]['dist'] 
        ba = dijkstra(G, b, cost, )[a]['dist']
        assert ab == ba


if __name__ == '__main__':
    print('testing if (a,b) in edges, then a,b in vertices')
    test_edges_and_vertices()
    print('testing if a is neighbour to b, then b is neighbour to a')
    test_neighbours()
    print('test that shortest path from a->b is shortest path from b->a')
    test_a_b()
    print('all tests successful')

