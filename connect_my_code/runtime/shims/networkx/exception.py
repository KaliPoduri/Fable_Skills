"""NetworkX's exception hierarchy.

graphify catches ``NetworkXNoPath`` and ``NodeNotFound`` around shortest-path
lookups, so the class identities and inheritance relationships have to match --
``except (nx.NetworkXNoPath, nx.NodeNotFound)`` must keep working unchanged.
"""
from __future__ import annotations

__all__ = [
    "NetworkXException",
    "NetworkXError",
    "NetworkXNoPath",
    "NetworkXUnfeasible",
    "NodeNotFound",
    "NetworkXPointlessConcept",
    "NetworkXAlgorithmError",
    "NetworkXNotImplemented",
    "AmbiguousSolution",
    "ExceededMaxIterations",
    "PowerIterationFailedConvergence",
]


class NetworkXException(Exception):
    """Base class for all NetworkX exceptions."""


class NetworkXError(NetworkXException):
    """A misuse of the NetworkX API."""


class NetworkXAlgorithmError(NetworkXException):
    """An algorithm failed on the given input."""


class NetworkXUnfeasible(NetworkXAlgorithmError):
    """No solution exists for the requested problem."""


class NetworkXNoPath(NetworkXUnfeasible):
    """No path exists between the requested source and target."""


class NodeNotFound(NetworkXException):
    """A requested node is not present in the graph."""


class NetworkXPointlessConcept(NetworkXException):
    """The requested concept is undefined for a null graph."""


class NetworkXNotImplemented(NetworkXException):
    """The algorithm is not defined for this graph type."""


class AmbiguousSolution(NetworkXException):
    """The problem is underspecified and admits several answers."""


class ExceededMaxIterations(NetworkXException):
    """An iterative algorithm hit its iteration ceiling."""


class PowerIterationFailedConvergence(ExceededMaxIterations):
    """Power iteration failed to converge."""

    def __init__(self, num_iterations, *args):
        super().__init__(f"power iteration failed to converge within {num_iterations} iterations", *args)
        self.num_iterations = num_iterations
