paramnet
========

``paramnet`` provides a convenience mixin, `Parametrized`, for creating subclasses of
NetworkX's `Graph` (`DiGraph`) that have numeric parameters associated with nodes and
edges (for example, a dynamical system on a network). It provides the following key features:

* Simplified reads/writes for the parameter value for a specific node/edge, without navigating NetworkX's nested dict structure
* Enforcing a well-defined node order on the graph, which in turn allows...
* Extraction of all values of a given node (edge) parameter as a 1D (2D) `numpy` array


Examples
--------
A parametrized network class can be created by subclassing from `Graph` or `DiGraph`
using the `Parametrized` mixin. The names of any node/edge parameters can be specified
in the class definition:

.. code:: python

    >>> class MyGraph(Parametrized, Graph, node_params=['x'], edge_params=['y']):
    ...    pass

    G = MyGraph()
..

Note: As with all mixins, `Parametrized` should be inherited from *first* as above.

`paramnet` automatically adds named fields for each declared parameter, supporting clean random
access (both read and write) by node or edge

.. code:: python

    >>> G.add_edge('a', 'b', y=3)
    >>> G.x['a']
    100
    >>> G.x['a'] = 4
    >>> G.y['a', 'b']
    3
    >>> G.y['a', 'b'] = 50
..

Contrast this with the more cumbersome random access in base NetworkX (which can be used interchangeably if you wish):

.. code:: python

    >>> G.nodes['a']['x']
    100
    >>> G.nodes['a']['x'] = 4
    >>> G.edges['a', 'b']['y']
    3
    >>> G.edges['a', 'b']['y'] = 50

..

What's more, `paramnet` maintains the order in which nodes were added, allowing index lookup:

.. code:: python

    >>> G.index('a')
    0
    >>> G.index('b')
    1
    >>> G.add_node('c')
    >>> G.index('c')
    2

..

But that's not all. Because the nodes are ordered, we can get a well-defined representation of *all*
values of a given node (edge) parameter at once as a vector (matrix). This is accomplished within `paramnet`
by accessing the associated parameter attribute without square brackets:

.. code:: python

    >>> G.x
    array([100, 100])
    >>> G.y
    array([[0., 3.],
           [3., 0.]])

    >>> G.A
    array([[0., 1.],
           [1., 0.]])
..

Note the special case for the weighted network adjacency matrix, which is automatically defined
for every graph through the field `A` (instead of `weight`), regardless of whether `weight` is
supplied in `edge_params`.

Under the hood, the parameter fields return View objects that wrap most `numpy` functionality,
allowing vector arithmetic and other array operations

.. code:: python

    >>> G = MyGraph()
    >>> G.add_nodes_from([(node, {'x': 5*node+1}) for node in range(5)])
    >>> G.add_cycle(range(5), y=1)

    # number of paths of length two between node pairs
    >>> np.dot(G.A, G.A)
    array([[0., 3., 1., 1., 3.],
           [3., 0., 3., 1., 1.],
           [1., 3., 0., 3., 1.],
           [1., 1., 3., 0., 3.],
           [3., 1., 1., 3., 0.]])

    >>> G.x + 1
    array([ 2,  7, 12, 17, 22])

..

Dependencies
------------
* NetworkX (>= 2.0)
* numpy

License
-------

``paramnet`` is released under the MIT license. See LICENSE for details.