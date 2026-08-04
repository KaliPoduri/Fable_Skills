"""Pure-standard-library stand-in for the slice of NetworkX graphify uses.

NetworkX is graphify's most pervasive dependency -- 18 modules import it -- but
the surface is narrow and well defined: four graph classes, the node-link JSON
round-trip, Louvain community detection, and a handful of algorithms
(shortest_path, betweenness, simple_cycles, compose, relabel_nodes) plus the
GraphML and matplotlib exporters.

Everything upstream reaches for is re-exported here under the same names, so
``import networkx as nx`` and ``from networkx.readwrite import json_graph`` work
untouched. Submodules mirror NetworkX's layout (``networkx.community``,
``networkx.readwrite.json_graph``) rather than being flattened, because graphify
imports them by path.

``__version__`` reports a shim-marked string. ``graphify.multigraph_compat``
records it into diagnostics output, so it deliberately does not impersonate a
real NetworkX release number -- a bug report from a zero-install checkout should
say where the graph code actually came from.
"""
from __future__ import annotations

from . import community, drawing, readwrite  # noqa: F401
from .algorithms import (  # noqa: F401
    ancestors,
    betweenness_centrality,
    compose,
    connected_components,
    density,
    descendants,
    edge_betweenness_centrality,
    has_path,
    is_directed_acyclic_graph,
    number_connected_components,
    relabel_nodes,
    shortest_path,
    shortest_path_length,
    simple_cycles,
    spring_layout,
    topological_sort,
)
from .classes import DiGraph, Graph, MultiDiGraph, MultiGraph  # noqa: F401
from .drawing import (  # noqa: F401
    draw,
    draw_networkx,
    draw_networkx_edges,
    draw_networkx_labels,
    draw_networkx_nodes,
)
from .exception import (  # noqa: F401
    AmbiguousSolution,
    ExceededMaxIterations,
    NetworkXAlgorithmError,
    NetworkXError,
    NetworkXException,
    NetworkXNoPath,
    NetworkXNotImplemented,
    NetworkXPointlessConcept,
    NetworkXUnfeasible,
    NodeNotFound,
    PowerIterationFailedConvergence,
)
from .readwrite import json_graph  # noqa: F401
from .readwrite.graphml import generate_graphml, write_graphml  # noqa: F401

__version__ = "3.4.2+connect_my_code-shim"


def empty_graph(n=0, create_using=None, default=Graph):
    """NetworkX's ``empty_graph`` -- used internally by node-link deserialization."""
    graph_class = create_using if create_using is not None else default
    graph = graph_class() if isinstance(graph_class, type) else graph_class
    graph.add_nodes_from(range(n))
    return graph


__all__ = [
    "Graph",
    "DiGraph",
    "MultiGraph",
    "MultiDiGraph",
    "community",
    "readwrite",
    "json_graph",
    "drawing",
    "empty_graph",
    "shortest_path",
    "shortest_path_length",
    "has_path",
    "betweenness_centrality",
    "edge_betweenness_centrality",
    "simple_cycles",
    "compose",
    "relabel_nodes",
    "spring_layout",
    "connected_components",
    "number_connected_components",
    "descendants",
    "ancestors",
    "density",
    "topological_sort",
    "is_directed_acyclic_graph",
    "write_graphml",
    "generate_graphml",
    "draw",
    "draw_networkx",
    "draw_networkx_nodes",
    "draw_networkx_edges",
    "draw_networkx_labels",
    "NetworkXException",
    "NetworkXError",
    "NetworkXNoPath",
    "NetworkXUnfeasible",
    "NodeNotFound",
    "__version__",
]
