"""Graph containers matching NetworkX's public behaviour.

Implements ``Graph``, ``DiGraph``, ``MultiGraph`` and ``MultiDiGraph`` with the
adjacency layout NetworkX uses -- ``_node`` maps node to attribute dict, ``_adj``
maps node to neighbour to attribute dict (to key-to-attribute dict for the
multigraph variants), and the directed classes additionally keep ``_pred``/
``_succ``. Keeping that internal shape means the view semantics below fall out
naturally rather than being special-cased.

The views (``G.nodes``, ``G.edges``, ``G.degree``) reproduce NetworkX's dual
nature: each is directly iterable *and* callable, so ``for n in G.nodes`` and
``G.nodes(data=True)`` both work, as do ``G.degree(n)`` returning a scalar and
``G.degree()`` returning pairs.

One deliberate divergence: :meth:`Graph.subgraph` returns an independent copy
rather than NetworkX's read-only view. NetworkX forbids mutating a subgraph view
at all, so a copy accepts every operation a view would -- it only differs if a
caller mutates the parent and expects the subgraph to follow, which no read-only
view permits either.
"""
from __future__ import annotations

from .exception import NetworkXError

__all__ = ["Graph", "DiGraph", "MultiGraph", "MultiDiGraph"]


def _nbunch_iter(graph, nbunch):
    """Resolve NetworkX's ``nbunch`` argument to a list of nodes in the graph.

    ``None`` means every node; a node present in the graph means just that node;
    anything else iterable is filtered down to nodes the graph actually has.
    """
    if nbunch is None:
        return list(graph._node)
    try:
        if nbunch in graph._node:
            return [nbunch]
    except TypeError:
        # Unhashable (a list of nodes, as G.edges(sorted(visited)) passes) --
        # it cannot be a single node, so fall through to the container case.
        pass
    try:
        return [n for n in nbunch if n in graph._node]
    except TypeError:
        return []


class _NodeView:
    """``G.nodes`` -- iterable of nodes, indexable for attributes, callable for data."""

    __slots__ = ("_graph",)

    def __init__(self, graph):
        self._graph = graph

    def __iter__(self):
        return iter(self._graph._node)

    def __len__(self):
        return len(self._graph._node)

    def __contains__(self, n):
        return n in self._graph._node

    def __getitem__(self, n):
        try:
            return self._graph._node[n]
        except KeyError:
            raise KeyError(n) from None

    def __call__(self, data=False, default=None):
        if data is False:
            return self
        return _NodeDataView(self._graph, data, default)

    def keys(self):
        return self._graph._node.keys()

    def items(self):
        return self._graph._node.items()

    def get(self, n, default=None):
        return self._graph._node.get(n, default)

    def __repr__(self):
        return f"NodeView({list(self._graph._node)!r})"


class _NodeDataView:
    """Result of ``G.nodes(data=...)``."""

    __slots__ = ("_graph", "_data", "_default")

    def __init__(self, graph, data, default):
        self._graph = graph
        self._data = data
        self._default = default

    def __iter__(self):
        for n, attrs in self._graph._node.items():
            if self._data is True:
                yield n, attrs
            else:
                yield n, attrs.get(self._data, self._default)

    def __len__(self):
        return len(self._graph._node)

    def __contains__(self, item):
        try:
            n, _ = item
        except (TypeError, ValueError):
            return item in self._graph._node
        return n in self._graph._node

    def __repr__(self):
        return f"NodeDataView({list(self)!r})"


class _EdgeView:
    """``G.edges`` for the non-multigraph classes."""

    __slots__ = ("_graph", "_in_edges", "_out_edges")

    def __init__(self, graph, in_edges=False, out_edges=False):
        self._graph = graph
        self._in_edges = in_edges
        self._out_edges = out_edges

    def _iter_edges(self, nbunch=None):
        """Yield ``(u, v, attrs)`` once per edge.

        Undirected graphs store each edge under both endpoints, so ``seen``
        suppresses the duplicate. Directed graphs walk successors only (or
        predecessors, for the ``in_edges`` view) and need no deduplication.
        """
        graph = self._graph
        nodes = _nbunch_iter(graph, nbunch)
        if graph.is_directed():
            if self._in_edges:
                for n in nodes:
                    for u, attrs in graph._pred.get(n, {}).items():
                        yield u, n, attrs
            else:
                for n in nodes:
                    for v, attrs in graph._succ.get(n, {}).items():
                        yield n, v, attrs
            return
        seen = set()
        for n in nodes:
            for v, attrs in graph._adj.get(n, {}).items():
                if (v, n) in seen:
                    continue
                seen.add((n, v))
                yield n, v, attrs

    def __iter__(self):
        for u, v, _ in self._iter_edges():
            yield u, v

    def __len__(self):
        return sum(1 for _ in self._iter_edges())

    def __contains__(self, item):
        try:
            u, v = item
        except (TypeError, ValueError):
            return False
        return self._graph.has_edge(u, v)

    def __getitem__(self, item):
        u, v = item
        return self._graph._adj[u][v]

    def __call__(self, nbunch=None, data=False, default=None, keys=False):
        return _EdgeDataView(self, nbunch, data, default)

    def __repr__(self):
        return f"EdgeView({list(self)!r})"


class _EdgeDataView:
    __slots__ = ("_view", "_nbunch", "_data", "_default")

    def __init__(self, view, nbunch, data, default):
        self._view = view
        self._nbunch = nbunch
        self._data = data
        self._default = default

    def __iter__(self):
        for u, v, attrs in self._view._iter_edges(self._nbunch):
            if self._data is False:
                yield u, v
            elif self._data is True:
                yield u, v, attrs
            else:
                yield u, v, attrs.get(self._data, self._default)

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, item):
        return any(item == e for e in self)

    def __repr__(self):
        return f"EdgeDataView({list(self)!r})"


class _MultiEdgeView(_EdgeView):
    """``G.edges`` for the multigraph classes -- adds the ``keys`` flag."""

    def _iter_edges(self, nbunch=None):
        graph = self._graph
        nodes = _nbunch_iter(graph, nbunch)
        if graph.is_directed():
            if self._in_edges:
                for n in nodes:
                    for u, keyed in graph._pred.get(n, {}).items():
                        for key, attrs in keyed.items():
                            yield u, n, key, attrs
            else:
                for n in nodes:
                    for v, keyed in graph._succ.get(n, {}).items():
                        for key, attrs in keyed.items():
                            yield n, v, key, attrs
            return
        seen = set()
        for n in nodes:
            for v, keyed in graph._adj.get(n, {}).items():
                for key, attrs in keyed.items():
                    if (v, n, key) in seen:
                        continue
                    seen.add((n, v, key))
                    yield n, v, key, attrs

    def __iter__(self):
        for u, v, _key, _attrs in self._iter_edges():
            yield u, v

    def __getitem__(self, item):
        """Look up edge attributes by ``(u, v, key)`` or, leniently, ``(u, v)``.

        Real NetworkX requires the 3-tuple on a multigraph and raises
        ``ValueError`` on a 2-tuple. This accepts both **deliberately**:
        ``graphify/export.py:to_graphml`` iterates ``for u, v in H.edges()`` and
        then indexes ``H.edges[u, v]``, which is an upstream bug that makes
        GraphML export fail outright against real NetworkX on the multigraphs
        graphify itself writes.

        Keeping the 2-tuple form working is what lets `cmc export graphml`
        succeed on the zero-install path. Do not "fix" this to match NetworkX
        strictly without first fixing the upstream call site -- doing so trades a
        working exporter for bug-compatibility nobody benefits from. The
        divergence is recorded in README's known-issues section.
        """
        if len(item) == 3:
            u, v, key = item
            return self._graph._adj[u][v][key]
        u, v = item
        keyed = self._graph._adj[u][v]
        # Return the first parallel edge's attribute dict, mirroring what the
        # 2-tuple caller expects from a simple graph.
        return next(iter(keyed.values())) if keyed else {}

    def __call__(self, nbunch=None, data=False, default=None, keys=False):
        return _MultiEdgeDataView(self, nbunch, data, default, keys)


class _MultiEdgeDataView:
    __slots__ = ("_view", "_nbunch", "_data", "_default", "_keys")

    def __init__(self, view, nbunch, data, default, keys):
        self._view = view
        self._nbunch = nbunch
        self._data = data
        self._default = default
        self._keys = keys

    def __iter__(self):
        for u, v, key, attrs in self._view._iter_edges(self._nbunch):
            payload = ()
            if self._keys:
                payload += (key,)
            if self._data is True:
                payload += (attrs,)
            elif self._data is not False:
                payload += (attrs.get(self._data, self._default),)
            yield (u, v) + payload

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, item):
        return any(item == e for e in self)

    def __repr__(self):
        return f"MultiEdgeDataView({list(self)!r})"


class _DegreeView:
    """``G.degree`` -- callable, iterable and subscriptable, as in NetworkX."""

    __slots__ = ("_graph", "_mode")

    def __init__(self, graph, mode="total"):
        self._graph = graph
        self._mode = mode

    def _degree_of(self, n, weight=None):
        graph = self._graph
        if n not in graph._node:
            raise KeyError(n)
        if graph.is_directed():
            sources = []
            if self._mode in ("total", "in"):
                sources.append(graph._pred.get(n, {}))
            if self._mode in ("total", "out"):
                sources.append(graph._succ.get(n, {}))
        else:
            sources = [graph._adj.get(n, {})]

        total = 0
        for adj in sources:
            for nbr, payload in adj.items():
                entries = payload.values() if graph.is_multigraph() else [payload]
                for attrs in entries:
                    increment = attrs.get(weight, 1) if weight is not None else 1
                    total += increment
                    # An undirected self-loop contributes 2 to the degree.
                    if nbr == n and not graph.is_directed():
                        total += increment
        return total

    def __call__(self, nbunch=None, weight=None):
        if nbunch is not None and nbunch in self._graph._node:
            return self._degree_of(nbunch, weight)
        nodes = _nbunch_iter(self._graph, nbunch)
        return _DegreeIter((n, self._degree_of(n, weight)) for n in nodes)

    def __getitem__(self, n):
        return self._degree_of(n)

    def __iter__(self):
        for n in self._graph._node:
            yield n, self._degree_of(n)

    def __len__(self):
        return len(self._graph._node)

    def __repr__(self):
        return f"DegreeView({list(self)!r})"


class _DegreeIter:
    """Materialised ``(node, degree)`` pairs that can be iterated more than once."""

    __slots__ = ("_pairs",)

    def __init__(self, pairs):
        self._pairs = list(pairs)

    def __iter__(self):
        return iter(self._pairs)

    def __len__(self):
        return len(self._pairs)

    def __repr__(self):
        return repr(self._pairs)


class Graph:
    """Undirected graph with self-loops, matching ``networkx.Graph``."""

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph: dict = {}
        self._node: dict = {}
        self._adj: dict = {}
        if incoming_graph_data is not None:
            self._load(incoming_graph_data)
        self.graph.update(attr)

    # ── construction helpers ──────────────────────────────────────────────
    def _load(self, data):
        if isinstance(data, Graph):
            self.graph.update(data.graph)
            for n, attrs in data._node.items():
                self.add_node(n, **attrs)
            if data.is_multigraph():
                for u, v, _key, attrs in data.edges(keys=True, data=True):
                    self.add_edge(u, v, **attrs)
            else:
                for u, v, attrs in data.edges(data=True):
                    self.add_edge(u, v, **attrs)
            return
        try:
            for item in data:
                if len(item) == 3:
                    u, v, attrs = item
                    self.add_edge(u, v, **attrs)
                else:
                    u, v = item
                    self.add_edge(u, v)
        except TypeError:
            raise NetworkXError(f"Input is not a known graph type: {data!r}") from None

    # ── introspection ─────────────────────────────────────────────────────
    def is_directed(self) -> bool:
        return False

    def is_multigraph(self) -> bool:
        return False

    @property
    def name(self) -> str:
        return self.graph.get("name", "")

    @name.setter
    def name(self, value) -> None:
        self.graph["name"] = value

    def __len__(self) -> int:
        return len(self._node)

    def __iter__(self):
        return iter(self._node)

    def __contains__(self, n) -> bool:
        try:
            return n in self._node
        except TypeError:
            return False

    def __getitem__(self, n):
        return self.adj[n]

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__} with {self.number_of_nodes()} nodes "
            f"and {self.number_of_edges()} edges"
        )

    # ── views ─────────────────────────────────────────────────────────────
    @property
    def nodes(self):
        return _NodeView(self)

    @property
    def edges(self):
        return _EdgeView(self)

    @property
    def degree(self):
        return _DegreeView(self)

    @property
    def adj(self):
        return self._adj

    # ── mutation ──────────────────────────────────────────────────────────
    def add_node(self, node_for_adding, **attr) -> None:
        if node_for_adding not in self._node:
            self._node[node_for_adding] = {}
            self._adj[node_for_adding] = {}
        self._node[node_for_adding].update(attr)

    def add_nodes_from(self, nodes_for_adding, **attr) -> None:
        for item in nodes_for_adding:
            # NetworkX accepts a bare node or a (node, attrdict) pair.
            if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], dict):
                node, node_attrs = item
                self.add_node(node, **{**attr, **node_attrs})
            else:
                self.add_node(item, **attr)

    def add_edge(self, u_of_edge, v_of_edge, **attr) -> None:
        u, v = u_of_edge, v_of_edge
        self.add_node(u)
        self.add_node(v)
        attrs = self._adj[u].get(v)
        if attrs is None:
            attrs = {}
            self._adj[u][v] = attrs
            self._adj[v][u] = attrs      # shared dict: an undirected edge has one attr store
        attrs.update(attr)

    def add_edges_from(self, ebunch_to_add, **attr) -> None:
        for item in ebunch_to_add:
            if len(item) == 3:
                u, v, edge_attrs = item
                self.add_edge(u, v, **{**attr, **edge_attrs})
            else:
                u, v = item
                self.add_edge(u, v, **attr)

    def add_weighted_edges_from(self, ebunch_to_add, weight="weight", **attr) -> None:
        for u, v, w in ebunch_to_add:
            self.add_edge(u, v, **{weight: w, **attr})

    def remove_node(self, n) -> None:
        if n not in self._node:
            raise NetworkXError(f"The node {n} is not in the graph.")
        for nbr in list(self._adj[n]):
            if nbr != n:
                self._adj[nbr].pop(n, None)
        del self._adj[n]
        del self._node[n]

    def remove_nodes_from(self, nodes) -> None:
        for n in list(nodes):
            if n in self._node:
                self.remove_node(n)

    def remove_edge(self, u, v) -> None:
        try:
            del self._adj[u][v]
            if u != v:
                del self._adj[v][u]
        except KeyError:
            raise NetworkXError(f"The edge {u}-{v} is not in the graph") from None

    def remove_edges_from(self, ebunch) -> None:
        for item in ebunch:
            u, v = item[0], item[1]
            if self.has_edge(u, v):
                self.remove_edge(u, v)

    def clear(self) -> None:
        self._node.clear()
        self._adj.clear()
        self.graph.clear()

    def update(self, edges=None, nodes=None) -> None:
        if isinstance(edges, Graph):
            self._load(edges)
            return
        if nodes is not None:
            self.add_nodes_from(nodes)
        if edges is not None:
            self.add_edges_from(edges)

    # ── queries ───────────────────────────────────────────────────────────
    def has_node(self, n) -> bool:
        return n in self._node

    def has_edge(self, u, v) -> bool:
        return u in self._adj and v in self._adj[u]

    def neighbors(self, n):
        try:
            return iter(self._adj[n])
        except KeyError:
            raise NetworkXError(f"The node {n} is not in the graph.") from None

    def number_of_nodes(self) -> int:
        return len(self._node)

    def order(self) -> int:
        return len(self._node)

    def number_of_edges(self, u=None, v=None) -> int:
        if u is None:
            return len(self.edges)
        return 1 if self.has_edge(u, v) else 0

    def size(self, weight=None) -> float:
        if weight is None:
            return len(self.edges)
        return sum(attrs.get(weight, 1) for _u, _v, attrs in self.edges(data=True))

    def get_edge_data(self, u, v, default=None):
        try:
            return self._adj[u][v]
        except KeyError:
            return default

    # ── derived graphs ────────────────────────────────────────────────────
    def _new(self):
        """Empty graph of this class, carrying the graph-level attributes."""
        fresh = type(self)()
        fresh.graph.update(self.graph)
        return fresh

    def copy(self, as_view=False):
        fresh = self._new()
        for n, attrs in self._node.items():
            fresh.add_node(n, **attrs)
        if self.is_multigraph():
            for u, v, key, attrs in self.edges(keys=True, data=True):
                fresh.add_edge(u, v, key=key, **attrs)
        else:
            for u, v, attrs in self.edges(data=True):
                fresh.add_edge(u, v, **attrs)
        return fresh

    def subgraph(self, nodes):
        """Node-induced subgraph.

        Returns an independent graph rather than NetworkX's frozen view; see the
        module docstring for why that is safe.
        """
        keep = {n for n in nodes if n in self._node}
        fresh = self._new()
        for n in keep:
            fresh.add_node(n, **self._node[n])
        if self.is_multigraph():
            for u, v, key, attrs in self.edges(keys=True, data=True):
                if u in keep and v in keep:
                    fresh.add_edge(u, v, key=key, **attrs)
        else:
            for u, v, attrs in self.edges(data=True):
                if u in keep and v in keep:
                    fresh.add_edge(u, v, **attrs)
        return fresh

    def edge_subgraph(self, edges):
        keep_edges = list(edges)
        keep_nodes = {n for e in keep_edges for n in e[:2]}
        fresh = self._new()
        for n in keep_nodes:
            if n in self._node:
                fresh.add_node(n, **self._node[n])
        for e in keep_edges:
            u, v = e[0], e[1]
            data = self.get_edge_data(u, v)
            if data is not None:
                fresh.add_edge(u, v, **(data if not self.is_multigraph() else {}))
        return fresh

    def to_undirected(self, as_view=False):
        fresh = Graph()
        fresh.graph.update(self.graph)
        for n, attrs in self._node.items():
            fresh.add_node(n, **attrs)
        if self.is_multigraph():
            for u, v, _key, attrs in self.edges(keys=True, data=True):
                fresh.add_edge(u, v, **attrs)
        else:
            for u, v, attrs in self.edges(data=True):
                fresh.add_edge(u, v, **attrs)
        return fresh

    def to_directed(self, as_view=False):
        fresh = MultiDiGraph() if self.is_multigraph() else DiGraph()
        fresh.graph.update(self.graph)
        for n, attrs in self._node.items():
            fresh.add_node(n, **attrs)
        if self.is_multigraph():
            for u, v, key, attrs in self.edges(keys=True, data=True):
                fresh.add_edge(u, v, key=key, **attrs)
                if u != v:
                    fresh.add_edge(v, u, key=key, **attrs)
        else:
            for u, v, attrs in self.edges(data=True):
                fresh.add_edge(u, v, **attrs)
                if u != v:
                    fresh.add_edge(v, u, **attrs)
        return fresh

    def nbunch_iter(self, nbunch=None):
        return iter(_nbunch_iter(self, nbunch))


class DiGraph(Graph):
    """Directed graph, matching ``networkx.DiGraph``."""

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph = {}
        self._node = {}
        self._succ = {}
        self._pred = {}
        self._adj = self._succ
        if incoming_graph_data is not None:
            self._load(incoming_graph_data)
        self.graph.update(attr)

    def is_directed(self) -> bool:
        return True

    @property
    def edges(self):
        return _EdgeView(self)

    @property
    def out_edges(self):
        return _EdgeView(self, out_edges=True)

    @property
    def in_edges(self):
        return _EdgeView(self, in_edges=True)

    @property
    def in_degree(self):
        return _DegreeView(self, mode="in")

    @property
    def out_degree(self):
        return _DegreeView(self, mode="out")

    @property
    def succ(self):
        return self._succ

    @property
    def pred(self):
        return self._pred

    def add_node(self, node_for_adding, **attr) -> None:
        if node_for_adding not in self._node:
            self._node[node_for_adding] = {}
            self._succ[node_for_adding] = {}
            self._pred[node_for_adding] = {}
        self._node[node_for_adding].update(attr)

    def add_edge(self, u_of_edge, v_of_edge, **attr) -> None:
        u, v = u_of_edge, v_of_edge
        self.add_node(u)
        self.add_node(v)
        attrs = self._succ[u].get(v)
        if attrs is None:
            attrs = {}
            self._succ[u][v] = attrs
            self._pred[v][u] = attrs
        attrs.update(attr)

    def remove_node(self, n) -> None:
        if n not in self._node:
            raise NetworkXError(f"The node {n} is not in the graph.")
        for v in list(self._succ[n]):
            self._pred[v].pop(n, None)
        for u in list(self._pred[n]):
            self._succ[u].pop(n, None)
        del self._succ[n]
        del self._pred[n]
        del self._node[n]

    def remove_edge(self, u, v) -> None:
        try:
            del self._succ[u][v]
            del self._pred[v][u]
        except KeyError:
            raise NetworkXError(f"The edge {u}-{v} is not in the graph") from None

    def has_edge(self, u, v) -> bool:
        return u in self._succ and v in self._succ[u]

    def neighbors(self, n):
        try:
            return iter(self._succ[n])
        except KeyError:
            raise NetworkXError(f"The node {n} is not in the graph.") from None

    def successors(self, n):
        return self.neighbors(n)

    def predecessors(self, n):
        try:
            return iter(self._pred[n])
        except KeyError:
            raise NetworkXError(f"The node {n} is not in the graph.") from None

    def clear(self) -> None:
        self._node.clear()
        self._succ.clear()
        self._pred.clear()
        self.graph.clear()


class MultiGraph(Graph):
    """Undirected multigraph, matching ``networkx.MultiGraph``."""

    def is_multigraph(self) -> bool:
        return True

    @property
    def edges(self):
        return _MultiEdgeView(self)

    def add_edge(self, u_for_edge, v_for_edge, key=None, **attr):
        u, v = u_for_edge, v_for_edge
        self.add_node(u)
        self.add_node(v)
        keyed = self._adj[u].get(v)
        if keyed is None:
            keyed = {}
            self._adj[u][v] = keyed
            self._adj[v][u] = keyed     # shared dict, as in the simple-graph case
        if key is None:
            key = len(keyed)
            while key in keyed:
                key += 1
        keyed.setdefault(key, {}).update(attr)
        return key

    def remove_edge(self, u, v, key=None) -> None:
        try:
            keyed = self._adj[u][v]
        except KeyError:
            raise NetworkXError(f"The edge {u}-{v} is not in the graph") from None
        if key is None:
            key = next(iter(keyed))
        try:
            del keyed[key]
        except KeyError:
            raise NetworkXError(f"The edge {u}-{v} with key {key} is not in the graph") from None
        if not keyed:
            del self._adj[u][v]
            if u != v:
                del self._adj[v][u]

    def remove_edges_from(self, ebunch) -> None:
        for item in ebunch:
            u, v = item[0], item[1]
            key = item[2] if len(item) > 2 and not isinstance(item[2], dict) else None
            if self.has_edge(u, v):
                self.remove_edge(u, v, key)

    def number_of_edges(self, u=None, v=None) -> int:
        if u is None:
            return len(list(self.edges(keys=True)))
        try:
            return len(self._adj[u][v])
        except KeyError:
            return 0

    def size(self, weight=None) -> float:
        if weight is None:
            return self.number_of_edges()
        return sum(attrs.get(weight, 1) for _u, _v, attrs in self.edges(data=True))

    def get_edge_data(self, u, v, key=None, default=None):
        try:
            keyed = self._adj[u][v]
        except KeyError:
            return default
        return keyed if key is None else keyed.get(key, default)


class MultiDiGraph(MultiGraph, DiGraph):
    """Directed multigraph, matching ``networkx.MultiDiGraph``."""

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph = {}
        self._node = {}
        self._succ = {}
        self._pred = {}
        self._adj = self._succ
        if incoming_graph_data is not None:
            self._load(incoming_graph_data)
        self.graph.update(attr)

    def is_directed(self) -> bool:
        return True

    def is_multigraph(self) -> bool:
        return True

    @property
    def edges(self):
        return _MultiEdgeView(self)

    @property
    def out_edges(self):
        return _MultiEdgeView(self, out_edges=True)

    @property
    def in_edges(self):
        return _MultiEdgeView(self, in_edges=True)

    add_node = DiGraph.add_node
    remove_node = DiGraph.remove_node
    neighbors = DiGraph.neighbors
    successors = DiGraph.successors
    predecessors = DiGraph.predecessors
    clear = DiGraph.clear

    def has_edge(self, u, v) -> bool:
        return u in self._succ and v in self._succ[u]

    def add_edge(self, u_for_edge, v_for_edge, key=None, **attr):
        u, v = u_for_edge, v_for_edge
        self.add_node(u)
        self.add_node(v)
        keyed = self._succ[u].get(v)
        if keyed is None:
            keyed = {}
            self._succ[u][v] = keyed
            self._pred[v][u] = keyed
        if key is None:
            key = len(keyed)
            while key in keyed:
                key += 1
        keyed.setdefault(key, {}).update(attr)
        return key

    def remove_edge(self, u, v, key=None) -> None:
        try:
            keyed = self._succ[u][v]
        except KeyError:
            raise NetworkXError(f"The edge {u}-{v} is not in the graph") from None
        if key is None:
            key = next(iter(keyed))
        try:
            del keyed[key]
        except KeyError:
            raise NetworkXError(f"The edge {u}-{v} with key {key} is not in the graph") from None
        if not keyed:
            del self._succ[u][v]
            del self._pred[v][u]

    def number_of_edges(self, u=None, v=None) -> int:
        if u is None:
            return len(list(self.edges(keys=True)))
        try:
            return len(self._succ[u][v])
        except KeyError:
            return 0

    def get_edge_data(self, u, v, key=None, default=None):
        try:
            keyed = self._succ[u][v]
        except KeyError:
            return default
        return keyed if key is None else keyed.get(key, default)
