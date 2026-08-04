"""connect_my_code portability runtime.

Holds the dependency bootstrap and the pure-standard-library shims that let the
bundled graphify package run straight from a git clone. Nothing in here is
imported by graphify itself -- the layer is bolted on from the launcher so the
upstream sources can stay byte-identical.
"""
