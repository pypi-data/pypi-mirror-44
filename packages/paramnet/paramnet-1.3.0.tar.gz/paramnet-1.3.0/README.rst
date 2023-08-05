paramnet
========

``paramnet`` provides a convenience mixin, `Parametrized`, for creating subclasses of
NetworkX's `Graph` (`DiGraph`) that have expected parameters associated with each
node and/or edge (e.g., in a network dynamical system). It provides a few key features:

* Enforces the existence of specified attributes for each node or edge
* Allows easy acccess to the value of a parameter by node or edge, without navigating NetworkX's nested dict structure
* Permits extracting a given parameter for all nodes (edges) as a 1D (2D) `numpy` array
* This is accomplished by maintaining a well-defined order for the network nodes, complete with index lookup

of specified named attributes for the (Di)Graph's nodes/edges, and also maintains
a well-defined order for the nodes. This allows the user to extract a given node (edge)
parameters as a well-defined vector (matrix).

Examples
--------
A parametrized network class can be created by subclassing from `Graph` or `DiGraph`
using the `Parametrized` mixin. The names of any node/edge parameters should be specified
in the class definition:

.. code:: python

    >>> class MyGraph(Parametrized, Graph, node_params=['x'], edge_params=['y']):
    ...    pass

    G = MyGraph()
..

Note: As with all mixins, `Parametrized` should be inherited from *first* as above.

Instances of this class will enforce the existence of the parameters for all new nodes/edges.
Trying to add nodes/edges without them raises a `NodeParameterError` or `EdgeParameterError`:

.. code:: python

    >>> G.add_node('a')
    NodeParameterError: Tried to add node 'a' without all required parameters: ['x']

    >>> G.add_nodes_from(['a', 'b'], x=100)
    >>> G.add_edge('a', 'b')
    EdgeParameterError: Tried to add edge ('a', 'b') without all required parameters: ['y']
..

`paramnet` automatically adds named fields for each declared parameter, supporting clean random
access by node or edge

.. code:: python

    >>> G.add_edge('a', 'b', y=3)
    >>> G.x['a']
    100
    >>> G.y['a', 'b']
    3
..

Contrast this with the more cumbersome random access in base NetworkX (which can be used interchangeably if you wish):

.. code:: python

    >>> G.nodes['a']['x']
    100
    >>> G.edges['a', 'b']['y']
    3

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

The fact that nodes are ordered also allows a well-defined representation of *all* values of
a given node (edge) parameter as a vector (matrix). This can be obtained by accessing
the associated attribute without square brackets.

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

Note the special case for the network adjacency matrix, which is automatically defined
for every graph through the field `A` regardless of whether the associated edge attribute
(`weight`) is listed among the required parameters.

Under the hood, the parameter fields return View objects that wrap most `numpy` functionality,
allowing easy array operations on parameters including vector arithmetic and matrix
multiplication:

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