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
def test_edges_and_vertices():
    


# if a has b as neighbour, b has a as neighbour

# shortest from a -> b is shortest from b->a


