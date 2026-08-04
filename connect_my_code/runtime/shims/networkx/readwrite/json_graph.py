"""``networkx.readwrite.json_graph`` -- node-link serialization.

This is the shim's highest-traffic surface: ``graphify-out/graph.json`` is the
tool's primary artefact, read and written on nearly every command, so the format
has to match NetworkX byte for byte.

Both spellings of the edge list are supported because graphify writes both. The
``edges`` keyword selects the key, and callers that predate it fall back to a
bare call; NetworkX's historical default for that bare call is ``"links"``, which
is what :func:`node_link_data` uses when ``edges`` is omitted -- graphify's
``except TypeError`` fallback in ``paths.load_node_link_graph`` documents exactly
that expectation.
"""
from __future__ import annotations

from ..classes import DiGraph, Graph, MultiDiGraph, MultiGraph

__all__ = ["node_link_data", "node_link_graph"]


def node_link_data(
    G,
    *,
    source="source",
    target="target",
    name="id",
    key="key",
    edges=None,
):
    """Serialize a graph to the node-link dict NetworkX produces."""
    edges_key = "links" if edges is None else edges
    multigraph = G.is_multigraph()

    data = {
        "directed": G.is_directed(),
        "multigraph": multigraph,
        "graph": G.graph,
        "nodes": [{**attrs, name: n} for n, attrs in G.nodes(data=True)],
    }

    if multigraph:
        data[edges_key] = [
            {**attrs, source: u, target: v, key: k}
            for u, v, k, attrs in G.edges(keys=True, data=True)
        ]
    else:
        data[edges_key] = [
            {**attrs, source: u, target: v} for u, v, attrs in G.edges(data=True)
        ]
    return data


def node_link_graph(
    data,
    directed=False,
    multigraph=True,
    *,
    source="source",
    target="target",
    name="id",
    key="key",
    edges=None,
):
    """Rebuild a graph from a node-link dict.

    ``directed``/``multigraph`` are defaults only: a serialized graph carries its
    own flags and those win, matching NetworkX.
    """
    edges_key = "links" if edges is None else edges
    directed = data.get("directed", directed)
    multigraph = data.get("multigraph", multigraph)

    if multigraph:
        graph = MultiDiGraph() if directed else MultiGraph()
    else:
        graph = DiGraph() if directed else Graph()

    graph.graph.update(data.get("graph", {}))

    for node_data in data["nodes"]:
        attrs = {k: v for k, v in node_data.items() if k != name}
        graph.add_node(node_data.get(name), **attrs)

    # KeyError here (rather than a silent empty graph) mirrors NetworkX and is
    # what graphify.paths.load_node_link_graph normalizes against by rewriting
    # an "edges"-keyed payload to "links" before calling in.
    for edge_data in data[edges_key]:
        skip = {source, target, key} if multigraph else {source, target}
        attrs = {k: v for k, v in edge_data.items() if k not in skip}
        u, v = edge_data.get(source), edge_data.get(target)
        if multigraph:
            graph.add_edge(u, v, key=edge_data.get(key), **attrs)
        else:
            graph.add_edge(u, v, **attrs)

    return graph
