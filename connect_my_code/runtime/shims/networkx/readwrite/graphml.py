"""GraphML writer -- ``networkx.write_graphml``.

Emits the same document shape NetworkX does: a ``<key>`` declaration per
distinct attribute name and scope, then the graph with ``<data>`` children.
Consumers of graphify's GraphML export are tools like Gephi, yEd and Cytoscape,
which key off the schema and the ``attr.type`` values rather than byte-level
formatting, so this targets structural equivalence.

``graphify.export`` normalizes every attribute value through its own
``_graphml_safe`` before calling in, so what arrives here is already limited to
``str``/``int``/``float``/``bool``. :func:`_attr_type` still classifies defensively
because the writer is reachable from any graph a future upstream sync might pass.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET

__all__ = ["write_graphml", "generate_graphml"]

_NS = "http://graphml.graphdrawing.org/xmlns"
_XSI = "http://www.w3.org/2001/XMLSchema-instance"
_SCHEMA = "http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"


def _attr_type(value) -> str:
    """GraphML type name for a Python value (bool before int -- bool subclasses int)."""
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "long" if abs(value) > 2**31 - 1 else "int"
    if isinstance(value, float):
        return "double"
    return "string"


def _attr_text(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


class _KeyRegistry:
    """Allocates ``d0``, ``d1``, ... ids per (attribute name, scope) pair."""

    def __init__(self):
        self._ids: dict[tuple[str, str], str] = {}
        self.declarations: list[tuple[str, str, str, str]] = []

    def key_for(self, name: str, scope: str, value) -> str:
        entry = (name, scope)
        if entry not in self._ids:
            key_id = f"d{len(self._ids)}"
            self._ids[entry] = key_id
            self.declarations.append((key_id, scope, name, _attr_type(value)))
        return self._ids[entry]


def _build_tree(G) -> ET.Element:
    registry = _KeyRegistry()

    graphml = ET.Element("graphml")
    graphml.set("xmlns", _NS)
    graphml.set("xmlns:xsi", _XSI)
    graphml.set("xsi:schemaLocation", _SCHEMA)

    graph_el = ET.Element("graph")
    graph_el.set("edgedefault", "directed" if G.is_directed() else "undirected")
    if G.is_multigraph():
        graph_el.set("parse.edgeids", "canonical")

    for name, value in G.graph.items():
        data = ET.SubElement(graph_el, "data")
        data.set("key", registry.key_for(str(name), "graph", value))
        data.text = _attr_text(value)

    for node, attrs in G.nodes(data=True):
        node_el = ET.SubElement(graph_el, "node")
        node_el.set("id", str(node))
        for name, value in attrs.items():
            data = ET.SubElement(node_el, "data")
            data.set("key", registry.key_for(str(name), "node", value))
            data.text = _attr_text(value)

    edge_rows = (
        G.edges(keys=True, data=True) if G.is_multigraph() else G.edges(data=True)
    )
    for row in edge_rows:
        if G.is_multigraph():
            u, v, edge_key, attrs = row
        else:
            (u, v, attrs), edge_key = row, None
        edge_el = ET.SubElement(graph_el, "edge")
        edge_el.set("source", str(u))
        edge_el.set("target", str(v))
        if edge_key is not None:
            edge_el.set("id", str(edge_key))
        for name, value in attrs.items():
            data = ET.SubElement(edge_el, "data")
            data.set("key", registry.key_for(str(name), "edge", value))
            data.text = _attr_text(value)

    # <key> declarations must precede <graph>, but their set is only known after
    # the whole graph has been walked -- so they are inserted at the front here.
    for index, (key_id, scope, name, type_name) in enumerate(registry.declarations):
        key_el = ET.Element("key")
        key_el.set("id", key_id)
        key_el.set("for", scope)
        key_el.set("attr.name", name)
        key_el.set("attr.type", type_name)
        graphml.insert(index, key_el)

    graphml.append(graph_el)
    return graphml


def generate_graphml(G, encoding="utf-8", prettyprint=True):
    """Yield the GraphML document as a single string chunk."""
    root = _build_tree(G)
    if prettyprint:
        _indent(root)
    yield ET.tostring(root, encoding="unicode")


def write_graphml(G, path, encoding="utf-8", prettyprint=True, infer_numeric_types=False, **_kwargs):
    """Write ``G`` as GraphML to ``path`` (a filename or an open binary file)."""
    root = _build_tree(G)
    if prettyprint:
        _indent(root)
    tree = ET.ElementTree(root)
    if hasattr(path, "write"):
        tree.write(path, encoding=encoding, xml_declaration=True)
    else:
        with open(path, "wb") as handle:
            tree.write(handle, encoding=encoding, xml_declaration=True)


def _indent(elem, level: int = 0) -> None:
    """In-place pretty-printing (``ET.indent`` equivalent, for older Pythons)."""
    pad = "\n" + "  " * level
    if len(elem):
        if not (elem.text or "").strip():
            elem.text = pad + "  "
        for child in elem:
            _indent(child, level + 1)
            if not (child.tail or "").strip():
                child.tail = pad + "  "
        if not (elem[-1].tail or "").strip():
            elem[-1].tail = pad
    if level and not (elem.tail or "").strip():
        elem.tail = pad
