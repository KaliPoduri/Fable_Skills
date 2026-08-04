"""Matplotlib drawing helpers -- ``networkx.drawing``.

``graphify.export`` calls ``draw_networkx_nodes`` and ``draw_networkx_labels``
for the optional SVG export, which already requires matplotlib and is skipped
when it is absent. These wrappers therefore import matplotlib lazily and raise
the same ``ImportError`` NetworkX raises, so upstream's existing guard around the
SVG path keeps working unchanged rather than seeing a new failure mode.
"""
from __future__ import annotations

__all__ = [
    "draw",
    "draw_networkx",
    "draw_networkx_nodes",
    "draw_networkx_edges",
    "draw_networkx_labels",
]


def _require_matplotlib():
    try:
        import matplotlib.pyplot as plt  # noqa: F401
    except ImportError as exc:
        raise ImportError("Matplotlib required for draw()") from exc
    return plt


def _axes(ax):
    plt = _require_matplotlib()
    return ax if ax is not None else plt.gca()


def draw_networkx_nodes(
    G,
    pos,
    nodelist=None,
    node_size=300,
    node_color="#1f78b4",
    node_shape="o",
    alpha=None,
    cmap=None,
    vmin=None,
    vmax=None,
    ax=None,
    linewidths=None,
    edgecolors=None,
    label=None,
    **_kwargs,
):
    """Scatter the nodes at ``pos``; returns the matplotlib collection."""
    axes = _axes(ax)
    nodes = list(G) if nodelist is None else list(nodelist)
    if not nodes:
        return None
    xs = [pos[n][0] for n in nodes]
    ys = [pos[n][1] for n in nodes]
    return axes.scatter(
        xs,
        ys,
        s=node_size,
        c=node_color,
        marker=node_shape,
        alpha=alpha,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        linewidths=linewidths,
        edgecolors=edgecolors,
        label=label,
    )


def draw_networkx_edges(
    G,
    pos,
    edgelist=None,
    width=1.0,
    edge_color="k",
    style="solid",
    alpha=None,
    ax=None,
    **_kwargs,
):
    """Draw edges as straight line segments."""
    axes = _axes(ax)
    edges = list(G.edges()) if edgelist is None else list(edgelist)
    drawn = []
    for edge in edges:
        u, v = edge[0], edge[1]
        if u not in pos or v not in pos:
            continue
        line = axes.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color=edge_color if isinstance(edge_color, str) else "k",
            linewidth=width,
            linestyle=style,
            alpha=alpha,
            zorder=1,
        )
        drawn.extend(line)
    return drawn


def draw_networkx_labels(
    G,
    pos,
    labels=None,
    font_size=12,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    ax=None,
    horizontalalignment="center",
    verticalalignment="center",
    **_kwargs,
):
    """Place a text label at each node position."""
    axes = _axes(ax)
    text_items = {n: str(n) for n in G} if labels is None else dict(labels)
    drawn = {}
    for node, text in text_items.items():
        if node not in pos:
            continue
        x, y = pos[node]
        drawn[node] = axes.text(
            x,
            y,
            text,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
        )
    return drawn


def draw_networkx(G, pos=None, arrows=None, with_labels=True, ax=None, **kwargs):
    """Draw nodes, edges and (optionally) labels in one call."""
    from .algorithms import spring_layout

    if pos is None:
        pos = spring_layout(G)
    draw_networkx_edges(G, pos, ax=ax, **{k: v for k, v in kwargs.items() if k.startswith("edge")})
    draw_networkx_nodes(G, pos, ax=ax, **{k: v for k, v in kwargs.items() if k.startswith("node")})
    if with_labels:
        draw_networkx_labels(G, pos, ax=ax, **{k: v for k, v in kwargs.items() if k.startswith("font")})


def draw(G, pos=None, ax=None, **kwargs):
    """``nx.draw`` -- ``draw_networkx`` on bare axes, labels off by default."""
    plt = _require_matplotlib()
    axes = ax if ax is not None else plt.gca()
    kwargs.setdefault("with_labels", False)
    draw_networkx(G, pos=pos, ax=axes, **kwargs)
    axes.set_axis_off()
