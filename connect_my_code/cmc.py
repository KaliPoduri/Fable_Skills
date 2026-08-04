#!/usr/bin/env python3
"""connect_my_code launcher -- run the tool straight from a git clone.

    git clone <repo> && cd connect_my_code && ./cmc extract .

No virtualenv, no ``pip``/``uv``/``npm``, no build step. This script puts the
bundled sources on ``sys.path``, installs the dependency bootstrap (real wheels
win, pure-stdlib shims fill the gaps -- see ``runtime/bootstrap.py``), and hands
straight over to the upstream ``graphify`` CLI entry point.

Two launcher-only subcommands are handled here rather than being passed down,
because both must work before anything heavyweight is imported:

  ``doctor``   report which dependencies resolved real vs shimmed
  ``selftest`` run the bundled portability test suite
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

MIN_PYTHON = (3, 10)


def _require_python() -> None:
    if sys.version_info < MIN_PYTHON:
        sys.stderr.write(
            "connect_my_code needs Python %d.%d or newer; this is %s.\n"
            "Point the CMC_PYTHON environment variable at a newer interpreter, e.g.\n"
            "    CMC_PYTHON=python3.12 ./cmc extract .\n"
            % (MIN_PYTHON[0], MIN_PYTHON[1], sys.version.split()[0])
        )
        raise SystemExit(2)


def _prepare() -> None:
    """Make the bundled package importable and activate the shim layer."""
    for entry in (ROOT, os.path.join(ROOT, "runtime", "dist")):
        if entry not in sys.path:
            sys.path.insert(0, entry)

    # graphify's skill/hook installers embed an executable path resolved with
    # shutil.which("graphify"). A zero-install checkout has no such binary, so
    # every generated hook would carry a bare `graphify` that fails at runtime.
    # bin/graphify is this launcher under that name; putting it first on PATH
    # makes which() resolve to it, so installers write a working absolute path.
    bin_dir = os.path.join(ROOT, "bin")
    if os.path.isdir(bin_dir):
        path = os.environ.get("PATH", "")
        if bin_dir not in path.split(os.pathsep):
            os.environ["PATH"] = bin_dir + os.pathsep + path

    from runtime import bootstrap

    bootstrap.install()


def _doctor() -> int:
    from runtime import bootstrap

    status = bootstrap.status()
    print("connect_my_code doctor")
    print("  python      %s" % sys.version.split()[0])
    print("  interpreter %s" % sys.executable)
    print("  root        %s" % ROOT)
    print()
    print("  dependency resolution (real = installed wheel, shim = bundled pure-Python):")
    width = max(len(n) for n in status) if status else 0
    for name, kind in sorted(status.items(), key=lambda kv: (kv[1], kv[0])):
        print("    %-*s  %s" % (width, name, kind))
    shimmed = sum(1 for k in status.values() if k == "shim")
    print()
    print("  %d of %d dependencies served by bundled shims." % (shimmed, len(status)))
    return 0


def _selftest(argv: list[str]) -> int:
    import unittest

    loader = unittest.TestLoader()
    suite = (
        loader.discover(os.path.join(ROOT, "tests"), pattern="test_*.py", top_level_dir=ROOT)
        if not argv
        else loader.loadTestsFromNames(argv)
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main() -> int:
    _require_python()
    _prepare()

    argv1 = sys.argv[1] if len(sys.argv) > 1 else ""
    if argv1 == "doctor":
        return _doctor()
    if argv1 == "selftest":
        return _selftest(sys.argv[2:])

    # graphify's CLI reads sys.argv directly and reports errors via SystemExit.
    from graphify.__main__ import main as graphify_main

    graphify_main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
