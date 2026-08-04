"""Zero-install dependency bootstrap.

connect_my_code ships the upstream graphify package byte-identical and makes it
runnable with nothing but a CPython interpreter. Everything graphify imports
from PyPI is either

  * already installed in the ambient environment -- in which case we use it and
    behave exactly like upstream, or
  * served from ``runtime/shims/`` as a pure-standard-library implementation.

The shim directory is deliberately **not** placed on ``sys.path``. It is served
by :class:`ShimFinder`, a meta-path finder appended to ``sys.meta_path``, which
claims a module name only after :func:`_real_spec` has confirmed the ambient
environment cannot supply it. That ordering is the whole design: a user who
happens to have real ``networkx`` or real ``tree_sitter`` wheels installed keeps
them, per module, with no configuration and no opt-in flag.

``tree_sitter`` is the one exception to "claim only what is missing" -- see
:data:`_ALWAYS_SHIM`. Its shim is a thin front-end that delegates to the real
C-extension parser whenever a real grammar is handed to it, and falls back to
the bundled pure-Python parsers per language otherwise. Fronting it
unconditionally is what allows a *mixed* environment (real tree_sitter, real
tree-sitter-python, but no tree-sitter-kotlin) to use the C parser for Python
and the pure parser for Kotlin in the same run.
"""
from __future__ import annotations

import importlib.abc
import importlib.machinery
import importlib.util
import os
import sys

SHIM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shims")

# Modules whose shim is a delegating front-end and must therefore load even when
# a real implementation exists. See module docstring.
_ALWAYS_SHIM = frozenset({"tree_sitter"})

# Set by install(); maps module name -> "real" | "shim" for diagnostics.
RESOLUTION: dict[str, str] = {}


def _shim_target(name: str) -> str | None:
    """Return the file backing ``name``'s shim, or None if we do not ship one.

    Package shims are directories with an ``__init__.py``; module shims are flat
    ``.py`` files. Only top-level names are resolved here -- submodules of a shim
    package (``networkx.readwrite``, ``rapidfuzz.distance``) are found by the
    normal import machinery once the parent package is loaded, because the
    parent's ``__path__`` points into the shim tree.
    """
    if "." in name:
        return None
    pkg_init = os.path.join(SHIM_DIR, name, "__init__.py")
    if os.path.isfile(pkg_init):
        return pkg_init
    module_py = os.path.join(SHIM_DIR, name + ".py")
    if os.path.isfile(module_py):
        return module_py
    return None


def _real_spec(name: str):
    """Find ``name`` in the ambient environment, ignoring our shims.

    ``PathFinder`` walks ``sys.path`` only; :class:`ShimFinder` lives on
    ``sys.meta_path`` and the shim directory is never added to ``sys.path``, so
    this cannot loop back into a shim no matter when it is called.
    """
    try:
        return importlib.machinery.PathFinder.find_spec(name, sys.path)
    except (ImportError, AttributeError, ValueError):
        return None


def real_module(name: str):
    """Import the ambient (non-shim) implementation of ``name``, or return None.

    Used by the ``tree_sitter`` front-end to reach the genuine C extension. The
    loaded module is cached in ``sys.modules`` under a private alias so it never
    collides with the shim occupying the public name.
    """
    alias = "_cmc_real_" + name
    cached = sys.modules.get(alias)
    if cached is not None:
        return cached
    spec = _real_spec(name)
    if spec is None or spec.loader is None:
        return None
    try:
        module = importlib.util.module_from_spec(spec)
        sys.modules[alias] = module
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(alias, None)
        return None
    return module


class ShimFinder(importlib.abc.MetaPathFinder):
    """Serves bundled pure-stdlib modules for names the environment lacks."""

    def find_spec(self, fullname, path=None, target=None):
        target_file = _shim_target(fullname)
        if target_file is None:
            return None
        if fullname not in _ALWAYS_SHIM and _real_spec(fullname) is not None:
            RESOLUTION[fullname] = "real"
            return None  # defer to the genuine package
        RESOLUTION[fullname] = "shim"
        if os.path.basename(target_file) == "__init__.py":
            spec = importlib.util.spec_from_file_location(
                fullname, target_file, submodule_search_locations=[os.path.dirname(target_file)]
            )
        else:
            spec = importlib.util.spec_from_file_location(fullname, target_file)
        return spec


_installed = False


def install() -> None:
    """Append the shim finder to ``sys.meta_path`` (idempotent).

    Appending rather than prepending keeps normal resolution order intact: the
    standard finders get first refusal on every name, and we are consulted only
    for what they could not supply.
    """
    global _installed
    if _installed:
        return
    sys.meta_path.append(ShimFinder())
    _installed = True


def status() -> dict[str, str]:
    """Report real-vs-shim resolution for every dependency we can stand in for.

    Drives ``cmc doctor``. Probes each shippable name rather than reading
    :data:`RESOLUTION`, so the report is complete even for modules that this run
    never happened to import.
    """
    names = set()
    for entry in os.listdir(SHIM_DIR):
        full = os.path.join(SHIM_DIR, entry)
        if entry.endswith(".py") and entry != "__init__.py":
            names.add(entry[:-3])
        elif os.path.isfile(os.path.join(full, "__init__.py")):
            names.add(entry)
    return {n: ("real" if _real_spec(n) is not None else "shim") for n in sorted(names)}
