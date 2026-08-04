"""Graph algorithms matching the NetworkX functions graphify calls.

Every function here follows the NetworkX implementation closely enough to return
the same values, including the normalization constants in the betweenness
rescaling and the ``random.Random(seed).sample`` draw that ``k``-sampled
betweenness depends on. Where NetworkX returns a lazily-evaluated generator this
module does too, so ``graphify.analyze``'s early ``break`` out of
``simple_cycles`` still prunes the search instead of paying for full enumeration.
"""
from __future__ import annotations

import math
import random
from collections import defaultdict, deque

from .classes import DiGraph, Graph, MultiDiGraph, MultiGraph
from .exception import NetworkXNoPath, NodeNotFound

__all__ = [
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
    "is_directed_acyclic_graph",
    "topological_sort",
]


# ── shortest paths ────────────────────────────────────────────────────────────


def _bfs_path(G, source, target):
    """Unweighted shortest path via BFS, returned source-first."""
    if source == target:
        return [source]
    parents = {source: None}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for nbr in G.neighbors(node):
            if nbr in parents:
                continue
            parents[nbr] = node
            if nbr == target:
                path = [target]
                while parents[path[-1]] is not None:
                    path.append(parents[path[-1]])
                path.reverse()
                return path
            queue.append(nbr)
    return None


def shortest_path(G, source=None, target=None, weight=None, method="unweighted"):
    """Unweighted shortest path between two nodes.

    graphify only ever calls the two-endpoint form, so that is what is
    implemented; the all-pairs and single-source forms raise rather than return
    something subtly different from NetworkX.
    """
    if source is None or target is None:
        raise NotImplementedError(
            "connect_my_code's bundled NetworkX shim implements shortest_path "
            "with both source and target given. Install real NetworkX for the "
            "all-pairs and single-source forms."
        )
    if source not in G:
        raise NodeNotFound(f"Source {source} is not in G")
    if target not in G:
        raise NodeNotFound(f"Target {target} is not in G")
    path = _bfs_path(G, source, target)
    if path is None:
        raise NetworkXNoPath(f"No path between {source} and {target}.")
    return path


def shortest_path_length(G, source=None, target=None, weight=None, method="unweighted"):
    return len(shortest_path(G, source, target)) - 1


def has_path(G, source, target) -> bool:
    try:
        shortest_path(G, source, target)
    except (NetworkXNoPath, NodeNotFound):
        return False
    return True


# ── betweenness centrality (Brandes) ──────────────────────────────────────────


def _single_source_shortest_path_basic(G, s):
    """Brandes' BFS pass: predecessors, sigma counts and the visit stack."""
    stack: list = []
    predecessors: dict = {v: [] for v in G}
    sigma: dict = dict.fromkeys(G, 0.0)
    distance: dict = {}
    sigma[s] = 1.0
    distance[s] = 0
    queue = deque([s])
    while queue:
        v = queue.popleft()
        stack.append(v)
        dist_v = distance[v]
        sigma_v = sigma[v]
        for w in G.neighbors(v):
            if w not in distance:
                queue.append(w)
                distance[w] = dist_v + 1
            if distance[w] == dist_v + 1:
                sigma[w] += sigma_v
                predecessors[w].append(v)
    return stack, predecessors, sigma


def _accumulate_basic(betweenness, stack, predecessors, sigma, s):
    delta = dict.fromkeys(stack, 0.0)
    while stack:
        w = stack.pop()
        coefficient = (1 + delta[w]) / sigma[w]
        for v in predecessors[w]:
            delta[v] += sigma[v] * coefficient
        if w != s:
            betweenness[w] += delta[w]
    return betweenness


def _accumulate_edges(betweenness, stack, predecessors, sigma, s):
    delta = dict.fromkeys(stack, 0.0)
    while stack:
        w = stack.pop()
        coefficient = (1 + delta[w]) / sigma[w]
        for v in predecessors[w]:
            contribution = sigma[v] * coefficient
            if (v, w) not in betweenness:
                betweenness[(w, v)] += contribution
            else:
                betweenness[(v, w)] += contribution
            delta[v] += contribution
        if w != s:
            betweenness[w] += delta[w]
    return betweenness


def _rescale(betweenness, n, normalized, directed=False, k=None, endpoints=False):
    """NetworkX's node-betweenness rescaling, constants included."""
    if normalized:
        if endpoints:
            scale = None if n < 2 else 1 / (n * (n - 1))
        elif n <= 2:
            scale = None
        else:
            scale = 1 / ((n - 1) * (n - 2))
    else:
        scale = None if directed else 0.5
    if scale is not None:
        if k is not None:
            scale = scale * n / k
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness


def _rescale_e(betweenness, n, normalized, directed=False, k=None):
    """NetworkX's edge-betweenness rescaling."""
    if normalized:
        scale = None if n <= 1 else 1 / (n * (n - 1))
    else:
        scale = None if directed else 0.5
    if scale is not None:
        if k is not None:
            scale = scale * n / k
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness


def _sample_sources(G, k, seed):
    """Reproduce NetworkX's ``py_random_state`` source sampling."""
    if k is None:
        return list(G)
    rng = seed if isinstance(seed, random.Random) else random.Random(seed)
    return rng.sample(list(G.nodes()), k)


def betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None):
    betweenness = dict.fromkeys(G, 0.0)
    for s in _sample_sources(G, k, seed):
        stack, predecessors, sigma = _single_source_shortest_path_basic(G, s)
        betweenness = _accumulate_basic(betweenness, stack, predecessors, sigma, s)
    return _rescale(
        betweenness, len(G), normalized=normalized, directed=G.is_directed(), k=k, endpoints=endpoints
    )


def edge_betweenness_centrality(G, k=None, normalized=True, weight=None, seed=None):
    betweenness = dict.fromkeys(G, 0.0)
    betweenness.update({e: 0.0 for e in G.edges()})
    for s in _sample_sources(G, k, seed):
        stack, predecessors, sigma = _single_source_shortest_path_basic(G, s)
        betweenness = _accumulate_edges(betweenness, stack, predecessors, sigma, s)
    for n in G:                       # keep only edge keys, as NetworkX does
        del betweenness[n]
    return _rescale_e(betweenness, len(G), normalized=normalized, directed=G.is_directed(), k=k)


# ── cycles ────────────────────────────────────────────────────────────────────


def simple_cycles(G, length_bound=None):
    """Enumerate elementary cycles, optionally bounded in length.

    Yields lazily so a caller that stops early (as ``graphify.analyze`` does
    after collecting enough cycles) never pays for the rest of the search.

    Each cycle is emitted once, canonicalised by starting at its lowest-ordered
    node and searching only nodes at or after that position -- the standard trick
    for avoiding the rotations of a cycle that a naive DFS would repeat.
    """
    if length_bound is not None and length_bound < 1:
        return

    nodes = list(G)
    order = {n: i for i, n in enumerate(nodes)}
    directed = G.is_directed()

    def successors(n):
        return G.successors(n) if directed else G.neighbors(n)

    # Self-loops are cycles of length 1 and are not reachable by the DFS below.
    for n in nodes:
        if G.has_edge(n, n):
            yield [n]

    if length_bound is not None and length_bound < 2:
        return

    for start in nodes:
        start_rank = order[start]
        path = [start]
        on_path = {start}

        def dfs(node):
            for nbr in successors(node):
                if order.get(nbr, -1) < start_rank:
                    continue                       # canonical-start pruning
                if nbr == start:
                    if directed:
                        if len(path) >= 2:
                            yield list(path)
                    elif len(path) >= 3 and order[path[1]] < order[path[-1]]:
                        # Undirected cycles appear in both directions; keep one.
                        yield list(path)
                    continue
                if nbr in on_path:
                    continue
                if length_bound is not None and len(path) >= length_bound:
                    continue
                path.append(nbr)
                on_path.add(nbr)
                yield from dfs(nbr)
                path.pop()
                on_path.discard(nbr)

        yield from dfs(start)


# ── graph combination and relabelling ─────────────────────────────────────────


def compose(G, H):
    """Union of two graphs; ``H``'s attributes win on collision, as in NetworkX."""
    if G.is_multigraph() != H.is_multigraph():
        raise ValueError("Cannot compose a multigraph with a non-multigraph")
    result = type(G)()
    result.graph.update(G.graph)
    result.graph.update(H.graph)
    for source in (G, H):
        for n, attrs in source.nodes(data=True):
            result.add_node(n, **attrs)
    for source in (G, H):
        if source.is_multigraph():
            for u, v, key, attrs in source.edges(keys=True, data=True):
                result.add_edge(u, v, key=key, **attrs)
        else:
            for u, v, attrs in source.edges(data=True):
                result.add_edge(u, v, **attrs)
    return result


def relabel_nodes(G, mapping, copy=True):
    """Rename nodes through ``mapping``; unmapped nodes keep their name.

    Attribute dicts are copied rather than shared so that mutating the relabelled
    graph -- which ``graphify.build`` does immediately afterwards -- cannot write
    through to the original.
    """
    if not copy:
        raise NotImplementedError(
            "connect_my_code's bundled NetworkX shim implements relabel_nodes "
            "with copy=True only."
        )
    result = type(G)()
    result.graph.update(G.graph)
    for n, attrs in G.nodes(data=True):
        result.add_node(mapping.get(n, n), **dict(attrs))
    if G.is_multigraph():
        for u, v, key, attrs in G.edges(keys=True, data=True):
            result.add_edge(mapping.get(u, u), mapping.get(v, v), key=key, **dict(attrs))
    else:
        for u, v, attrs in G.edges(data=True):
            result.add_edge(mapping.get(u, u), mapping.get(v, v), **dict(attrs))
    return result


# ── connectivity ──────────────────────────────────────────────────────────────


def connected_components(G):
    seen = set()
    for start in G:
        if start in seen:
            continue
        component = set()
        queue = deque([start])
        seen.add(start)
        while queue:
            node = queue.popleft()
            component.add(node)
            neighbours = (
                set(G.neighbors(node)) | set(G.predecessors(node))
                if G.is_directed()
                else G.neighbors(node)
            )
            for nbr in neighbours:
                if nbr not in seen:
                    seen.add(nbr)
                    queue.append(nbr)
        yield component


def number_connected_components(G) -> int:
    return sum(1 for _ in connected_components(G))


def descendants(G, source):
    if source not in G:
        raise NodeNotFound(f"The node {source} is not in the graph.")
    seen = {source}
    queue = deque([source])
    while queue:
        for nbr in G.neighbors(queue.popleft()):
            if nbr not in seen:
                seen.add(nbr)
                queue.append(nbr)
    seen.discard(source)
    return seen


def ancestors(G, source):
    if source not in G:
        raise NodeNotFound(f"The node {source} is not in the graph.")
    predecessors = G.predecessors if G.is_directed() else G.neighbors
    seen = {source}
    queue = deque([source])
    while queue:
        for nbr in predecessors(queue.popleft()):
            if nbr not in seen:
                seen.add(nbr)
                queue.append(nbr)
    seen.discard(source)
    return seen


def density(G) -> float:
    n, m = G.number_of_nodes(), G.number_of_edges()
    if n <= 1:
        return 0.0
    return m / (n * (n - 1)) if G.is_directed() else 2 * m / (n * (n - 1))


def topological_sort(G):
    in_degree = {n: 0 for n in G}
    for _u, v in G.edges():
        in_degree[v] += 1
    queue = deque(n for n in G if in_degree[n] == 0)
    emitted = 0
    while queue:
        node = queue.popleft()
        emitted += 1
        yield node
        for nbr in G.neighbors(node):
            in_degree[nbr] -= 1
            if in_degree[nbr] == 0:
                queue.append(nbr)
    if emitted != len(in_degree):
        from .exception import NetworkXUnfeasible

        raise NetworkXUnfeasible("Graph contains a cycle.")


def is_directed_acyclic_graph(G) -> bool:
    if not G.is_directed():
        return False
    try:
        for _ in topological_sort(G):
            pass
    except Exception:
        return False
    return True


# ── layout ────────────────────────────────────────────────────────────────────


def spring_layout(G, k=None, pos=None, iterations=50, seed=None, scale=1.0, center=None, dim=2):
    """Fruchterman-Reingold layout in pure Python.

    Feeds the optional matplotlib SVG export only. Exact coordinate parity with
    NetworkX is neither achievable (it draws from NumPy's RNG) nor meaningful for
    a force-directed drawing, so this aims for a stable, well-spread layout: same
    seed gives the same picture on every run and platform.
    """
    nodes = list(G)
    count = len(nodes)
    if count == 0:
        return {}
    if count == 1:
        return {nodes[0]: (0.0, 0.0)}

    rng = random.Random(seed if seed is not None else 0)
    positions = {n: [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)] for n in nodes}
    if k is None:
        k = 1.0 / math.sqrt(count)

    temperature = 0.1 * max(1.0, scale)
    cooling = temperature / (iterations + 1)

    for _ in range(iterations):
        displacement = {n: [0.0, 0.0] for n in nodes}
        for i, u in enumerate(nodes):
            for v in nodes[i + 1:]:
                dx = positions[u][0] - positions[v][0]
                dy = positions[u][1] - positions[v][1]
                dist_sq = dx * dx + dy * dy
                if dist_sq < 1e-12:
                    dx, dy, dist_sq = rng.uniform(-1e-3, 1e-3), rng.uniform(-1e-3, 1e-3), 1e-6
                dist = math.sqrt(dist_sq)
                force = (k * k) / dist_sq
                displacement[u][0] += dx / dist * force
                displacement[u][1] += dy / dist * force
                displacement[v][0] -= dx / dist * force
                displacement[v][1] -= dy / dist * force

        for u, v in G.edges():
            if u == v:
                continue
            dx = positions[u][0] - positions[v][0]
            dy = positions[u][1] - positions[v][1]
            dist = math.sqrt(dx * dx + dy * dy) or 1e-6
            force = dist / k
            displacement[u][0] -= dx / dist * force
            displacement[u][1] -= dy / dist * force
            displacement[v][0] += dx / dist * force
            displacement[v][1] += dy / dist * force

        for n in nodes:
            dx, dy = displacement[n]
            length = math.sqrt(dx * dx + dy * dy) or 1e-6
            capped = min(length, temperature)
            positions[n][0] += dx / length * capped
            positions[n][1] += dy / length * capped
        temperature -= cooling

    # Centre, then scale so the widest axis spans [-scale, scale].
    cx = sum(p[0] for p in positions.values()) / count
    cy = sum(p[1] for p in positions.values()) / count
    extent = max(
        max(abs(p[0] - cx) for p in positions.values()),
        max(abs(p[1] - cy) for p in positions.values()),
        1e-9,
    )
    factor = scale / extent
    origin = center or (0.0, 0.0)
    return {
        n: (
            (p[0] - cx) * factor + origin[0],
            (p[1] - cy) * factor + origin[1],
        )
        for n, p in positions.items()
    }


# Kept for callers that expect the symbol to exist alongside the algorithms.
_GRAPH_TYPES = (Graph, DiGraph, MultiGraph, MultiDiGraph)
_UNUSED = defaultdict
