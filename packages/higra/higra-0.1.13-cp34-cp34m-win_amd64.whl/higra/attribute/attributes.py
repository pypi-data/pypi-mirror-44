############################################################################
# Copyright ESIEE Paris (2018)                                             #
#                                                                          #
# Contributor(s) : Benjamin Perret                                         #
#                                                                          #
# Distributed under the terms of the CECILL-B License.                     #
#                                                                          #
# The full license is in the file LICENSE, distributed with this software. #
############################################################################


import numpy as np
import higra as hg


@hg.data_provider("vertex_area")
def attribute_vertex_area(graph):
    """
    Compute the vertex area of the given graph.

    In general the area of a vertex if simply equal to 1. But, if the graph is a region adjacency graph then the area of
    a region is equal to the sum of the area of the vertices inside the region (obtained with a recursive call to
    attribute_vertex_area on the original graph).

    **Provider name**: "vertex_area"

    :param graph: input graph
    :return: a 1d array (Concept :class:`~higra.CptVertexWeightedGraph`)
    """
    if hg.CptRegionAdjacencyGraph.validate(graph):  # this is a rag like graph
        pre_graph = hg.CptRegionAdjacencyGraph.get_pre_graph(graph)
        pre_graph_vertex_area = attribute_vertex_area(pre_graph)
        return hg.rag_accumulate_on_vertices(graph, hg.Accumulators.sum, vertex_weights=pre_graph_vertex_area)
    res = np.ones((graph.num_vertices(),), dtype=np.int64)
    res = hg.delinearize_vertex_weights(res, graph)
    hg.CptVertexWeightedGraph.link(res, graph)
    return res


@hg.data_provider("edge_length")
def attribute_edge_length(graph):
    """
    Compute the edge length of the given graph.

    In general the legnth of an edge if simply equal to 1. But, if the graph is a region adjacency graph then the
    length of an edge is equal to the sum of length of the corresponding edges in the original graph (obtained with a
    recursive call to attribute_edge_length on the original graph).

    **Provider name**: "edge_length"

    :param graph: input graph
    :return: a nd array (Concept :class:`~higra.CptEdgeWeightedGraph`)
    """
    if hg.CptRegionAdjacencyGraph.validate(graph):  # this is a rag like graph
        pre_graph = hg.CptRegionAdjacencyGraph.get_pre_graph(graph)
        pre_graph_edge_length = attribute_edge_length(pre_graph)
        return hg.rag_accumulate_on_edges(graph, hg.Accumulators.sum, edge_weights=pre_graph_edge_length)
    res = np.ones((graph.num_edges(),), dtype=np.int64)
    hg.CptEdgeWeightedGraph.link(res, graph)
    return res


@hg.data_provider("vertex_perimeter")
@hg.argument_helper("edge_length")
def attribute_vertex_perimeter(graph, edge_length):
    """
    Compute the vertex perimeter of the given graph.
    The perimeter of a vertex is defined as the sum of the length of out-edges of the vertex.

    **Provider name**: "vertex_perimeter"

    :param graph: input graph
    :param edge_length: length of the edges of the input graph (provided by :func:`~higra.attribute_edge_length` on `graph`)
    :return: a nd array (Concept :class:`~higra.CptVertexWeightedGraph`)
    """
    res = hg.accumulate_graph_edges(edge_length, hg.Accumulators.sum, graph)
    res = hg.delinearize_vertex_weights(res, graph)
    hg.CptVertexWeightedGraph.link(res, graph)
    return res


@hg.data_provider("vertex_coordinates")
@hg.argument_helper(hg.CptGridGraph)
def attribute_vertex_coordinates(graph, shape):
    """
    Computes the coordinates of the given grid graph.

    **Provider name**: "vertex_coordinates"

    Example
    =======

    >>> g = hg.get_4_adjacency_graph((2, 3))
    >>> c = hg.attribute_vertex_coordinates(g)
    (((0, 0), (0, 1), (0, 2)),
     ((1, 0), (1, 1), (1, 2)))

    :param graph: Input graph
    :param shape: (deduced from :class:`~higra.CptGridGraph`)
    :return: a nd array (Concept :class:`~higra.CptVertexWeightedGraph`)
    """
    coords = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    coords = [c.reshape((-1, )) for c in coords]
    attribute = np.stack(reversed(coords), axis=1)
    attribute = hg.delinearize_vertex_weights(attribute, graph)
    hg.CptVertexWeightedGraph.link(attribute, graph)
    return attribute


@hg.data_provider("area")
@hg.argument_helper(hg.CptHierarchy, ("leaf_graph", "vertex_area"))
def attribute_area(tree, vertex_area=None, leaf_graph=None):
    """
    Compute the area of each node the given tree.
    The area of a node is equal to the sum of the area of the leaves of the subtree rooted in the node.

    **Provider name**: "area"

    :param tree: input tree (Concept :class:`~higra.CptHierarchy`)
    :param vertex_area: area of the vertices of the leaf graph of the tree (provided by :func:`~higra.attribute_vertex_area` on `leaf_graph` )
    :param leaf_graph: (deduced from :class:`~higra.CptHierarchy`)
    :return: a 1d array (Concept :class:`~higra.CptValuedHierarchy`)
    """
    if vertex_area is None:
        vertex_area = np.ones((tree.num_leaves(),), dtype=np.int64)

    if leaf_graph is not None:
        vertex_area = hg.linearize_vertex_weights(vertex_area, leaf_graph)
    return hg.accumulate_sequential(vertex_area, hg.Accumulators.sum, tree)


@hg.data_provider("volume")
@hg.argument_helper(hg.CptValuedHierarchy, ("tree", "area"))
def attribute_volume(altitudes, tree, area):
    """
    Compute the volume of each node the given tree.
    The volume :math:`V(n)` of a node :math:`n` defined recursively as:

    .. math::

        V(n) = area(n) * |altitude(n) - altitude(parent(n))| + \sum_{c \in children(n)} V(c)

    **Provider name**: "volume"

    :param altitudes: node altitudes of the input tree  (Concept :class:`~higra.CptValuedHierarchy`)
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param area: area of the nodes of the input hierarchy (provided by :func:`~higra.attribute_area`)
    :return: a 1d array (Concept :class:`~higra.CptValuedHierarchy`)
    """
    height = np.abs(altitudes[tree.parents()] - altitudes)
    height = height * area
    volume_leaves = height[:tree.num_leaves()]
    return hg.accumulate_and_add_sequential(height, volume_leaves, hg.Accumulators.sum, tree)


@hg.data_provider("lca_map")
@hg.argument_helper(hg.CptHierarchy)
def attribute_lca_map(tree, leaf_graph):
    """
    Compute for each edge `(i, j)` of the `leaf_graph`, the lowest common ancestor of `i` and `j` in the given tree.

    Complexity: :math:`\mathcal{O}(n\log(n)) + \mathcal{O}(m)` where :math:`n` is the number of nodes in `tree` and
    :math:`m` is the number of edges in `leaf_graph`.

    **Provider name**: "lca_map"

    :param tree: input tree (Concept :class:`~higra.CptHierarchy`)
    :param leaf_graph: graph on the leaves of the input tree (deduced from :class:`~higra.CptHierarchy`)
    :return: a 1d array (Concept :class:`~higra.CptEdgeWeightedGraph`)
    """
    lca = hg.LCAFast(tree)
    res = lca.lca(leaf_graph)
    hg.CptEdgeWeightedGraph.link(res, leaf_graph)
    return res


@hg.data_provider("frontier_length")
@hg.argument_helper(hg.CptHierarchy, ("tree", "lca_map"), ("leaf_graph", "edge_length"))
def attribute_frontier_length(tree, lca_map, edge_length, leaf_graph=None):
    """
    In a partition tree, each node represent the merging of 2 or more regions.
    The frontier of a node is then defined as the common contour between the merged regions.
    This function compute the length of these common contours as the sum of the length of edges going from one of the
    merged region to the other one.

    **Provider name**: "frontier_length"

    :param tree: input tree
    :param lca_map: indicates for each edge `(i, j)` of the `leaf_graph`, the lowest common ancestor of `i` and `j` in the given tree (provided by :func:`~higra.attribute_lca_map` on `tree`)
    :param edge_length: length of th edges of the leaf graph (provided by :func:`~higra.attribute_edge_length` on `leaf_graph`)
    :param leaf_graph: graph on the leaves of the input tree (deduced from :class:`~higra.CptHierarchy`)
    :return: a 1d array (Concept :class:`~higra.CptValuedHierarchy`)
    """
    frontier_length = np.zeros((tree.num_vertices(),), dtype=np.int64)
    np.add.at(frontier_length, lca_map, edge_length)
    hg.CptValuedHierarchy.link(frontier_length, tree)
    return frontier_length


@hg.data_provider("perimeter_length")
@hg.argument_helper(hg.CptHierarchy, ("leaf_graph", "vertex_perimeter"), ("tree", "frontier_length"))
def attribute_perimeter_length(tree, vertex_perimeter, frontier_length, leaf_graph=None):
    """
    Compute the length of the perimeter of each node of the given tree.

    **Provider name**: "perimeter_length"

    :param tree: input tree (Concept :class:`~higra.CptHierarchy`)
    :param vertex_perimeter: perimeter length of each vertex of the leaf graph (provided by :func:`~higra.attribute_vertex_perimeter` on `leaf_graph`)
    :param frontier_length: length of common contour between merging regions (provided by :func:`~higra.attribute_frontier_length` on `tree`)
    :param leaf_graph: (deduced from :class:`~higra.CptHierarchy`)
    :return: a 1d array (Concept :class:`~higra.CptValuedHierarchy`)
    """
    if leaf_graph is not None:
        vertex_perimeter = hg.linearize_vertex_weights(vertex_perimeter, leaf_graph)

    return hg.accumulate_and_add_sequential(-2 * frontier_length, vertex_perimeter, hg.Accumulators.sum, tree)


@hg.data_provider("compactness")
@hg.argument_helper("area", "perimeter_length")
def attribute_compactness(tree, area, perimeter_length, normalize=True):
    """
    The compactness of a node is defined as its area divided by the square of its perimeter length.

    **Provider name**: "compactness"

    :param tree: input tree
    :param area: node area of the input tree (provided by :func:`~higra.attribute_area` on `tree`)
    :param perimeter_length: node perimeter length of the input tree (provided by :func:`~higra.attribute_perimeter_length` on `tree`)
    :param normalize: if True the result is divided by the maximal compactness value in the tree
    :return: a 1d array (Concept :class:`~higra.CptValuedHierarchy`)
    """
    compactness = area / (perimeter_length * perimeter_length)
    if normalize:
        max_compactness = np.nanmax(compactness)
        res = compactness / max_compactness
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.data_provider("mean_weights")
@hg.argument_helper(hg.CptHierarchy, "area")
def attribute_mean_weights(tree, vertex_weights, area, leaf_graph=None):
    """
    Compute for each node, the mean weight of the leaf graph vertices inside this node.

    **Provider name**: "mean_weights"

    :param tree: input tree (Concept :class:`~higra.CptHierarchy`)
    :param vertex_weights: vertex weights of the leaf graph of the input tree
    :param area: area of the tree nodes  (provided by :func:`~higra.attribute_area` on `tree`)
    :param leaf_graph: leaf graph of the input tree (deduced from :class:`~higra.CptHierarchy`)
    :return: a nd array (Concept :class:`~higra.CptValuedHierarchy`)
    """

    if leaf_graph is not None:
        vertex_weights = hg.linearize_vertex_weights(vertex_weights, leaf_graph)

    attribute = hg.accumulate_sequential(vertex_weights.astype(np.float64), hg.Accumulators.sum, tree) / area.reshape((-1, 1))
    hg.CptValuedHierarchy.link(attribute, tree)
    return attribute


@hg.data_provider("sibling")
def attribute_sibling(tree, skip=1):
    """
    For each node `n` which is the `k`-th child of its parent node `p` among `N` children,
    the attribute sibling of `n` is the index of the `(k + skip) % N`-th child of `p`.

    The sibling of the root node is itself.

    The sibling attribute enables to easily emulates a (doubly) linked list among brothers.

    In a binary tree, the sibling attribute of a node is effectively its only brother (with `skip` equals to 1).

    **Provider name**: "sibling"

    :param tree: Input tree
    :param skip: Number of skipped element in the children list (including yourself)
    :return: a nd array (Concept :class:`~higra.CptValuedHierarchy`)
    """
    attribute = hg.cpp._attribute_sibling(tree, skip)
    hg.CptValuedHierarchy.link(attribute, tree)
    return attribute


@hg.data_provider("depth")
def attribute_depth(tree):
    """
    The depth of a node `n` of the tree `t` is equal to the number of ancestors of `n` in `t`.

    The depth of the root node is equalt to 0.

    **Provider name**: "depth"

    :param tree: Input tree
    :return: a nd array (Concept :class:`~higra.CptValuedHierarchy`)
    """
    attribute = hg.cpp._attribute_depth(tree)
    hg.CptValuedHierarchy.link(attribute, tree)
    return attribute


@hg.data_provider("regular_altitudes")
@hg.argument_helper("depth")
def attribute_regular_altitudes(tree, depth):
    """
    The regular altitudes is comprised between 0 and 1 and is inversely proportional to its depth

    **Provider name**: "regular_altitudes"

    :param tree: input tree
    :param depth: depth of the tree node (provided by :func:`~higra.attribute_depth` on `tree`)
    :return: a nd array (Concept :class:`~higra.CptValuedHierarchy`)
    """

    altitudes = 1 - depth / np.max(depth)
    altitudes[:tree.num_leaves()] = 0
    hg.CptValuedHierarchy.link(altitudes, tree)
    return altitudes
