"""Community detection -- ``networkx.community``.

Only Louvain is needed: ``graphify.cluster`` prefers Leiden from graspologic and
falls back to ``nx.community.louvain_communities`` when that is absent, which in
a zero-install checkout is always.

The implementation follows NetworkX's ``louvain.py`` step for step, including the
``seed.shuffle`` of the node visit order and the exact modularity-gain
expression. That matters: community ids end up on every node in ``graph.json``,
so an equivalent-but-different partition would show up as a diff in the tool's
output. ``graphify.cluster`` feeds in a graph whose nodes and edges were inserted
in sorted order, which combined with the seeded shuffle makes the partition
deterministic.

``graphify.cluster`` inspects this function's signature for ``max_level`` before
deciding whether to pass it, so the parameters are spelled out rather than
collected into ``**kwargs``.
"""
from __future__ import annotations

import random
from collections import defaultdict

__all__ = ["louvain_communities", "louvain_partitions", "modularity"]


def _as_random(seed):
    if isinstance(seed, random.Random):
        return seed
    return random.Random(seed)


def _degrees(G, weight):
    """Weighted degree per node, counting undirected self-loops twice."""
    result = {}
    for n in G:
        total = 0.0
        for nbr, attrs in G.adj.get(n, {}).items():
            entries = attrs.values() if G.is_multigraph() else [attrs]
            for data in entries:
                w = data.get(weight, 1) if weight else 1
                total += w * 2 if nbr == n else w
        result[n] = total
    return result


def _neighbor_weights(nbrs, node2com):
    """Total edge weight from one node into each neighbouring community."""
    weights = defaultdict(float)
    for nbr, wt in nbrs.items():
        weights[node2com[nbr]] += wt
    return weights


def modularity(G, communities, weight="weight", resolution=1):
    """Newman-Girvan modularity of a partition."""
    communities = [set(c) for c in communities]
    directed = G.is_directed()
    m = G.size(weight)
    if m == 0:
        return 0.0

    if directed:
        out_degree = {n: 0.0 for n in G}
        in_degree = {n: 0.0 for n in G}
        for u, v, data in G.edges(data=True):
            w = data.get(weight, 1) if weight else 1
            out_degree[u] += w
            in_degree[v] += w
        norm = 1 / m**2
    else:
        degree = _degrees(G, weight)
        norm = 1 / (2 * m) ** 2

    def community_contribution(community):
        comm = set(community)
        internal = 0.0
        for u, v, data in G.edges(data=True):
            if u in comm and v in comm:
                w = data.get(weight, 1) if weight else 1
                internal += w * 2 if (u != v and not directed) else w
        if directed:
            out_sum = sum(out_degree[u] for u in comm)
            in_sum = sum(in_degree[u] for u in comm)
            return internal / m - resolution * out_sum * in_sum * norm
        degree_sum = sum(degree[u] for u in comm)
        return internal / (2 * m) - resolution * degree_sum**2 * norm

    return sum(map(community_contribution, communities))


def _gen_graph(G, partition):
    """Collapse each community into a single weighted super-node."""
    from ..classes import Graph, DiGraph

    aggregated = DiGraph() if G.is_directed() else Graph()
    node2com = {}
    for i, part in enumerate(partition):
        nodes = set()
        for node in part:
            node2com[node] = i
            nodes.update(G.nodes[node].get("nodes", {node}))
        aggregated.add_node(i, nodes=nodes)

    for u, v, data in G.edges(data=True):
        w = data.get("weight", 1)
        com1, com2 = node2com[u], node2com[v]
        existing = aggregated.get_edge_data(com1, com2, default={"weight": 0})
        aggregated.add_edge(com1, com2, weight=w + existing["weight"])
    return aggregated


def _one_level(G, m, partition, resolution=1, is_directed=False, seed=None):
    """One Louvain sweep: move nodes greedily until modularity stops improving."""
    node2com = {u: i for i, u in enumerate(G.nodes())}
    inner_partition = [{u} for u in G.nodes()]

    if is_directed:
        in_degrees = {n: 0.0 for n in G}
        out_degrees = {n: 0.0 for n in G}
        for u, v, data in G.edges(data=True):
            w = data.get("weight", 1)
            out_degrees[u] += w
            in_degrees[v] += w
        stot_in = list(in_degrees.values())
        stot_out = list(out_degrees.values())
        nbrs = {}
        for u in G:
            nbrs[u] = defaultdict(float)
            for v, data in G._succ.get(u, {}).items():
                if v != u:
                    nbrs[u][v] += data.get("weight", 1)
            for v, data in G._pred.get(u, {}).items():
                if v != u:
                    nbrs[u][v] += data.get("weight", 1)
    else:
        degrees = _degrees(G, "weight")
        stot = list(degrees.values())
        nbrs = {
            u: {v: (data.get("weight", 1)) for v, data in G.adj.get(u, {}).items() if v != u}
            for u in G
        }

    rand_nodes = list(G.nodes)
    _as_random(seed).shuffle(rand_nodes)

    nb_moves = 1
    improvement = False
    while nb_moves > 0:
        nb_moves = 0
        for u in rand_nodes:
            best_mod = 0.0
            best_com = node2com[u]
            weights2com = _neighbor_weights(nbrs[u], node2com)
            if is_directed:
                in_degree, out_degree = in_degrees[u], out_degrees[u]
                stot_in[best_com] -= in_degree
                stot_out[best_com] -= out_degree
                remove_cost = (
                    -weights2com[best_com] / m
                    + resolution * (out_degree * stot_in[best_com] + in_degree * stot_out[best_com]) / m**2
                )
            else:
                degree = degrees[u]
                stot[best_com] -= degree
                remove_cost = -weights2com[best_com] / m + resolution * (stot[best_com] * degree) / (2 * m**2)

            for nbr_com, wt in weights2com.items():
                if is_directed:
                    gain = (
                        remove_cost
                        + wt / m
                        - resolution
                        * (out_degrees[u] * stot_in[nbr_com] + in_degrees[u] * stot_out[nbr_com])
                        / m**2
                    )
                else:
                    gain = remove_cost + wt / m - resolution * (stot[nbr_com] * degrees[u]) / (2 * m**2)
                if gain > best_mod:
                    best_mod = gain
                    best_com = nbr_com

            if is_directed:
                stot_in[best_com] += in_degrees[u]
                stot_out[best_com] += out_degrees[u]
            else:
                stot[best_com] += degrees[u]

            if best_com != node2com[u]:
                com = G.nodes[u].get("nodes", {u})
                partition[node2com[u]].difference_update(com)
                inner_partition[node2com[u]].remove(u)
                partition[best_com].update(com)
                inner_partition[best_com].add(u)
                improvement = True
                nb_moves += 1
                node2com[u] = best_com

    partition = list(filter(len, partition))
    inner_partition = list(filter(len, inner_partition))
    return partition, inner_partition, improvement


def louvain_partitions(G, weight="weight", resolution=1, threshold=0.0000001, max_level=None, seed=None):
    """Yield the partition produced at each level of the Louvain hierarchy."""
    partition = [{u} for u in G.nodes()]
    if G.number_of_edges() == 0:
        yield partition
        return

    mod = modularity(G, partition, resolution=resolution, weight=weight)
    is_directed = G.is_directed()

    if G.is_multigraph():
        graph = _convert_multigraph(G, weight, is_directed)
    else:
        graph = G.__class__()
        graph.add_nodes_from(G)
        graph.add_weighted_edges_from(G.edges(data=weight, default=1))

    m = graph.size(weight="weight")
    partition, inner_partition, improvement = _one_level(
        graph, m, partition, resolution, is_directed, seed
    )
    improvement = True
    level = 0
    while improvement:
        yield [s.copy() for s in partition]
        new_mod = modularity(graph, inner_partition, resolution=resolution, weight="weight")
        if new_mod - mod <= threshold:
            return
        mod = new_mod
        level += 1
        if max_level is not None and level >= max_level:
            return
        graph = _gen_graph(graph, inner_partition)
        partition, inner_partition, improvement = _one_level(
            graph, m, partition, resolution, is_directed, seed
        )


def louvain_communities(G, weight="weight", resolution=1, threshold=0.0000001, max_level=None, seed=None):
    """Best Louvain partition, as a list of node sets."""
    if max_level is not None and max_level <= 0:
        raise ValueError("max_level argument must be a positive integer or None")
    result = [{u} for u in G.nodes()]
    for partition in louvain_partitions(G, weight, resolution, threshold, max_level, seed):
        result = partition
    return result


def _convert_multigraph(G, weight, is_directed):
    """Fold parallel edges into one weighted edge per node pair."""
    from ..classes import Graph, DiGraph

    converted = DiGraph() if is_directed else Graph()
    converted.add_nodes_from(G)
    for u, v, wt in G.edges(data=weight, default=1):
        existing = converted.get_edge_data(u, v)
        prev = existing.get("weight", 0) if existing else 0
        converted.add_edge(u, v, weight=prev + wt)
    return converted
