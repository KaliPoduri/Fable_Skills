"""Auto-activate the shim layer for interpreters launched outside ``cmc``.

Python imports ``sitecustomize`` at startup whenever it is importable from
``sys.path``, and ``PYTHONPATH`` entries are on ``sys.path`` by then. So putting
this directory on ``PYTHONPATH`` is enough to make a plain ``python3 -m
graphify ...`` behave exactly like ``./cmc ...``.

That is what ``bin/python3`` does, and it is what makes graphify's git hooks
work: the generated ``post-commit`` hook probes for an interpreter where
``importlib.util.find_spec('graphify')`` succeeds, then runs the rebuild with
it. Without this, no interpreter on the machine can satisfy that probe in a
zero-install checkout, and every commit prints "could not locate a Python with
graphify installed".

Kept deliberately quiet and defensive: this runs at the start of *every* Python
process that inherits the variable, so it must never raise or print.
"""
from __future__ import annotations

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    for _entry in (_ROOT, os.path.join(_ROOT, "runtime", "dist")):
        if _entry not in sys.path:
            sys.path.insert(0, _entry)

    from runtime import bootstrap

    bootstrap.install()
except Exception:  # pragma: no cover - startup hook must never break a process
    pass
