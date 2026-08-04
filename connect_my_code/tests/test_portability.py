"""Portability tests -- run with ``./cmc selftest``.

These cover the shim layer, not graphify itself: upstream ships its own suite,
and the risk this port introduces is that a shim quietly returns something
subtly different from the real dependency. Numeric expectations below are
published reference values, not values captured from this implementation.
"""
from __future__ import annotations

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _entry in (ROOT, os.path.join(ROOT, "runtime", "dist")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

from runtime import bootstrap  # noqa: E402

bootstrap.install()


class TestBootstrap(unittest.TestCase):
    def test_real_dependencies_win_over_shims(self):
        """A name the environment can supply must not be served from shims."""
        for name, kind in bootstrap.status().items():
            if kind == "real":
                spec = bootstrap._real_spec(name)
                self.assertIsNotNone(spec, f"{name} reported real but is not findable")
                self.assertNotIn(
                    bootstrap.SHIM_DIR, str(getattr(spec, "origin", "")),
                    f"{name} resolved into the shim directory despite a real install",
                )

    def test_shim_directory_is_not_on_sys_path(self):
        """Shims are served by the finder only -- never by path shadowing."""
        self.assertNotIn(bootstrap.SHIM_DIR, sys.path)

    def test_package_version_resolves(self):
        from importlib.metadata import version

        self.assertEqual(version("graphifyy"), "0.9.32")


class TestRapidFuzzShim(unittest.TestCase):
    """Published reference values for each metric."""

    def test_jaro_and_jaro_winkler(self):
        from rapidfuzz.distance import Jaro, JaroWinkler

        cases = [
            ("MARTHA", "MARHTA", 0.944444, 0.961111),
            ("DWAYNE", "DUANE", 0.822222, 0.840000),
            ("DIXON", "DICKSONX", 0.766667, 0.813333),
        ]
        for a, b, jaro, winkler in cases:
            self.assertAlmostEqual(Jaro.normalized_similarity(a, b), jaro, places=5)
            self.assertAlmostEqual(JaroWinkler.normalized_similarity(a, b), winkler, places=5)

    def test_identical_and_empty_strings(self):
        from rapidfuzz.distance import Jaro, JaroWinkler

        self.assertEqual(Jaro.normalized_similarity("", ""), 1.0)
        self.assertEqual(Jaro.normalized_similarity("abc", ""), 0.0)
        self.assertEqual(JaroWinkler.normalized_similarity("abc", "abc"), 1.0)

    def test_damerau_levenshtein_is_unrestricted(self):
        """CA -> ABC is 2 unrestricted; the OSA variant would say 3."""
        from rapidfuzz.distance import DamerauLevenshtein

        self.assertEqual(DamerauLevenshtein.distance("CA", "ABC"), 2)
        self.assertEqual(DamerauLevenshtein.distance("Extractor", "Extractar"), 1)
        self.assertEqual(DamerauLevenshtein.distance("", ""), 0)


class TestNumpyShim(unittest.TestCase):
    def test_mt19937_matches_canonical_vector(self):
        """Twist/temper validated against mt19937ar's init_genrand(5489)."""
        import numpy as np

        engine = np._MT19937.__new__(np._MT19937)
        key = [5489]
        for i in range(1, 624):
            key.append((1812433253 * (key[i - 1] ^ (key[i - 1] >> 30)) + i) & 0xFFFFFFFF)
        engine.key, engine.pos = key, 624
        self.assertEqual(
            [engine.next_uint32() for _ in range(5)],
            [3499211612, 581869302, 3890346734, 3586334585, 545404204],
        )

    def test_uint64_arithmetic_wraps(self):
        import numpy as np

        self.assertEqual(int(np.uint64(2**64 - 1) + np.uint64(1)), 0)
        self.assertEqual(int(np.uint64(2**63) * np.uint64(2)), 0)

    def test_minhash_pipeline_runs(self):
        from graphify._minhash import MinHash, MinHashLSH

        similar, other = MinHash(), MinHash()
        for shingle in ("abc", "bcd", "cde"):
            similar.update(shingle.encode())
        for shingle in ("xxx", "yyy", "zzz"):
            other.update(shingle.encode())
        lsh = MinHashLSH(threshold=0.5, num_perm=128)
        lsh.insert("similar", similar)
        lsh.insert("other", other)
        self.assertEqual(lsh.query(similar), ["similar"])
        self.assertEqual((lsh.b, lsh.r), (25, 5))


class TestNetworkXShim(unittest.TestCase):
    def _sample_graph(self):
        import networkx as nx

        graph = nx.Graph()
        for a, b in [("a", "b"), ("b", "c"), ("c", "a"), ("c", "d"),
                     ("d", "e"), ("e", "f"), ("f", "d")]:
            graph.add_edge(a, b, relation="calls")
        for node in graph.nodes():
            graph.nodes[node]["label"] = node.upper()
        return graph

    def test_views_are_iterable_and_callable(self):
        graph = self._sample_graph()
        self.assertEqual(graph.number_of_nodes(), 6)
        self.assertEqual(graph.degree("c"), 3)
        self.assertEqual(dict(graph.degree())["c"], 3)
        self.assertEqual(sorted(graph.neighbors("c")), ["a", "b", "d"])
        self.assertIn(("a", "b", {"relation": "calls"}), list(graph.edges(data=True)))

    def test_attribute_writes_go_through_views(self):
        """graphify.export mutates via G.nodes[n][k] and G.edges[u, v][k]."""
        graph = self._sample_graph()
        graph.nodes["a"]["label"] = "changed"
        graph.edges["a", "b"]["relation"] = "uses"
        self.assertEqual(graph.nodes["a"]["label"], "changed")
        self.assertEqual(list(graph.edges(data=True))[0][2]["relation"], "uses")

    def test_nbunch_accepts_a_list(self):
        """serve.py calls G.edges(sorted(visited)) with an unhashable list.

        NetworkX yields every edge *incident* to the nbunch, so a-b, b-c, c-a
        and c-d all qualify.
        """
        graph = self._sample_graph()
        self.assertEqual(len(list(graph.edges(sorted(["a", "b", "c"])))), 4)

    def test_node_link_round_trip_preserves_attributes(self):
        import networkx as nx
        from networkx.readwrite import json_graph

        graph = self._sample_graph()
        data = json_graph.node_link_data(graph, edges="links")
        self.assertEqual(sorted(data), ["directed", "graph", "links", "multigraph", "nodes"])
        restored = json_graph.node_link_graph(data, edges="links")
        self.assertEqual(restored.number_of_nodes(), graph.number_of_nodes())
        self.assertEqual(restored.number_of_edges(), graph.number_of_edges())
        self.assertEqual(restored.nodes["a"], {"label": "A"})
        # The payload records multigraph: False, and the stored flag wins over
        # node_link_graph's default -- as in NetworkX.
        self.assertIsInstance(restored, nx.Graph)
        self.assertFalse(restored.is_multigraph())

    def test_multigraph_round_trip_keeps_parallel_edges(self):
        import networkx as nx
        from networkx.readwrite import json_graph

        graph = nx.MultiDiGraph()
        graph.add_edge("p", "q", relation="a")
        graph.add_edge("p", "q", relation="b")
        data = json_graph.node_link_data(graph, edges="links")
        self.assertEqual(json_graph.node_link_graph(data, edges="links").number_of_edges(), 2)

    def test_shortest_path_and_exceptions(self):
        import networkx as nx

        graph = self._sample_graph()
        self.assertEqual(nx.shortest_path(graph, "a", "f"), ["a", "c", "d", "f"])
        graph.add_node("island")
        with self.assertRaises(nx.NetworkXNoPath):
            nx.shortest_path(graph, "a", "island")
        with self.assertRaises(nx.NodeNotFound):
            nx.shortest_path(graph, "a", "absent")

    def test_louvain_recovers_planted_communities(self):
        import networkx as nx

        communities = nx.community.louvain_communities(
            self._sample_graph(), seed=42, threshold=1e-4, resolution=1.0, max_level=10
        )
        self.assertEqual(
            sorted(sorted(c) for c in communities), [["a", "b", "c"], ["d", "e", "f"]]
        )

    def test_louvain_signature_exposes_max_level(self):
        """graphify.cluster inspects the signature before passing max_level."""
        import inspect

        import networkx as nx

        self.assertIn(
            "max_level", inspect.signature(nx.community.louvain_communities).parameters
        )

    def test_bounded_simple_cycles(self):
        import networkx as nx

        digraph = nx.DiGraph([("x", "y"), ("y", "z"), ("z", "x"), ("z", "w"), ("w", "z")])
        cycles = sorted(sorted(c) for c in nx.simple_cycles(digraph, length_bound=5))
        self.assertEqual(cycles, [["w", "z"], ["x", "y", "z"]])

    def test_compose_and_relabel(self):
        import networkx as nx

        merged = nx.compose(nx.Graph([("1", "2")]), nx.Graph([("2", "3")]))
        self.assertEqual(merged.number_of_edges(), 2)
        relabelled = nx.relabel_nodes(merged, {n: f"r::{n}" for n in merged.nodes}, copy=True)
        self.assertEqual(sorted(relabelled.nodes())[0], "r::1")

    def test_graphml_writes_valid_xml(self):
        import tempfile
        import xml.etree.ElementTree as ET

        import networkx as nx

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "g.graphml")
            nx.write_graphml(self._sample_graph(), path)
            root = ET.parse(path).getroot()
        self.assertTrue(root.tag.endswith("graphml"))


class TestTreeSitterShim(unittest.TestCase):
    def _parse(self, module_name, source, language_fn="language"):
        import importlib

        from tree_sitter import Language, Parser

        grammar = getattr(importlib.import_module(module_name), language_fn)()
        return Parser(Language(grammar)).parse(source).root_node

    def _find(self, node, node_type):
        return [n for n in node.descendants() if n.type == node_type]

    def test_language_version_satisfies_graphify(self):
        """extract.py._check_tree_sitter_version() requires >= 14 and is fatal."""
        import tree_sitter

        self.assertGreaterEqual(tree_sitter.LANGUAGE_VERSION, 14)

    def test_python_declarations_fields_and_positions(self):
        source = (
            b'"""Doc."""\n'
            b"import os\n"
            b"from pathlib import Path\n\n"
            b"class Greeter(Base):\n"
            b"    def greet(self, name: str, count: int = 1) -> list[str]:\n"
            b"        return os.path.join(name)\n"
        )
        root = self._parse("tree_sitter_python", source)
        self.assertEqual(root.type, "module")

        klass = self._find(root, "class_definition")[0]
        self.assertEqual(klass.child_by_field_name("name").text, b"Greeter")
        self.assertEqual(klass.start_point[0] + 1, 5)

        function = self._find(root, "function_definition")[0]
        self.assertEqual(function.child_by_field_name("name").text, b"greet")
        params = [c.type for c in function.child_by_field_name("parameters").children]
        self.assertEqual(params, ["identifier", "typed_parameter", "typed_default_parameter"])
        self.assertEqual(function.child_by_field_name("return_type").type, "type")

        call = self._find(root, "call")[0]
        self.assertEqual(call.child_by_field_name("function").text, b"os.path.join")

        import_from = self._find(root, "import_from_statement")[0]
        self.assertEqual(import_from.child_by_field_name("module_name").text, b"pathlib")

    def test_python_parent_chain_and_byte_offsets(self):
        source = b"class A:\n    def m(self):\n        f()\n"
        root = self._parse("tree_sitter_python", source)
        call = self._find(root, "call")[0]
        chain, node = [], call
        while node is not None:
            chain.append(node.type)
            node = node.parent
        self.assertEqual(chain[-1], "module")
        self.assertIn("function_definition", chain)
        self.assertIn("class_definition", chain)
        for node in root.descendants():
            self.assertLessEqual(node.start_byte, node.end_byte)
            self.assertLessEqual(node.end_byte, len(source))

    def test_python_tolerates_a_syntax_error(self):
        """tree-sitter always returns a tree; graphify relies on that to keep going."""
        root = self._parse("tree_sitter_python", b"def broken(:\n")
        self.assertEqual(root.type, "module")
        self.assertTrue(root.has_error)

    def test_java_inheritance_and_flat_call_fields(self):
        source = (
            b"package shop;\n"
            b"public class Order extends Base implements Payable {\n"
            b"    public double total() { return helper.compute(); }\n"
            b"}\n"
        )
        root = self._parse("tree_sitter_java", source)
        klass = self._find(root, "class_declaration")[0]
        self.assertEqual(klass.child_by_field_name("superclass").text, b"Base")
        interfaces = klass.child_by_field_name("interfaces")
        self.assertEqual(interfaces.children[0].type, "type_list")

        invocation = self._find(root, "method_invocation")[0]
        self.assertEqual(invocation.child_by_field_name("name").text, b"compute")
        self.assertEqual(invocation.child_by_field_name("object").text, b"helper")

    def test_typescript_export_wraps_rather_than_consumes(self):
        source = b"export class Cart extends Base {\n  add(x: string): void { this.check(x); }\n}\n"
        root = self._parse("tree_sitter_typescript", source, "language_typescript")
        export = self._find(root, "export_statement")[0]
        self.assertEqual(export.child_by_field_name("declaration").type, "class_declaration")
        self.assertEqual(len(self._find(root, "method_definition")), 1)
        self.assertEqual(len(self._find(root, "call_expression")), 1)

    def test_c_function_declarator_chain(self):
        """graphify's _get_c_func_name walks declarator -> identifier."""
        root = self._parse("tree_sitter_c", b"static int validate(const char *s) { return 0; }\n")
        definition = self._find(root, "function_definition")[0]
        declarator = definition.child_by_field_name("declarator")
        self.assertEqual(declarator.type, "function_declarator")
        self.assertEqual(declarator.child_by_field_name("declarator").type, "identifier")
        self.assertEqual(declarator.child_by_field_name("declarator").text, b"validate")

    def test_go_receiver_precedes_the_name(self):
        root = self._parse("tree_sitter_go", b"package s\nfunc (s *Store) Add(i string) { s.save(i) }\n")
        declaration = self._find(root, "function_declaration")[0]
        self.assertEqual(declaration.child_by_field_name("name").text, b"Add")

    def test_ruby_end_delimited_bodies(self):
        source = b"class Processor < Base\n  def run\n    self.prepare\n  end\n  def prepare\n  end\nend\n"
        root = self._parse("tree_sitter_ruby", source)
        self.assertEqual(len(self._find(root, "method")), 2)
        klass = self._find(root, "class")[0]
        self.assertEqual(klass.child_by_field_name("superclass").text, b"Base")

    def test_strings_and_comments_do_not_open_blocks(self):
        """A brace inside a string or comment must not be treated as structure."""
        source = b'class A {\n  m() { const s = "}{"; /* } */ return 1; }\n}\n'
        root = self._parse("tree_sitter_javascript", source)
        self.assertEqual(len(self._find(root, "class_declaration")), 1)
        self.assertEqual(len(self._find(root, "method_definition")), 1)


class TestSkillInstallation(unittest.TestCase):
    """graphify installs itself into AI assistants; the hooks it writes must run.

    The installers embed an executable resolved via shutil.which("graphify").
    A zero-install checkout has no such binary, so without bin/graphify on PATH
    every generated hook would carry a bare `graphify` that fails at runtime.
    """

    def test_graphify_name_resolves_to_the_launcher(self):
        import shutil
        import subprocess

        # cmc.py prepends bin/ to PATH; replicate that for an in-process check.
        bin_dir = os.path.join(ROOT, "bin")
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

        from graphify.install import _resolve_graphify_exe

        self.assertEqual(shutil.which("graphify"), os.path.join(bin_dir, "graphify"))
        self.assertTrue(_resolve_graphify_exe().endswith("bin/graphify"))

        # And that path is genuinely executable.
        result = subprocess.run(
            [os.path.join(bin_dir, "graphify"), "--version"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("0.9.32", result.stdout)

    def test_generated_hook_command_is_absolute(self):
        bin_dir = os.path.join(ROOT, "bin")
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

        from graphify.install import _claude_pretooluse_hooks

        command = _claude_pretooluse_hooks()[0]["hooks"][0]["command"]
        self.assertTrue(os.path.isabs(command.split()[0]), command)
        self.assertIn("hook-guard", command)

    def test_skill_installs_into_a_project(self):
        import subprocess
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, HOME=tmp)
            result = subprocess.run(
                [sys.executable, os.path.join(ROOT, "cmc.py"), "install", "--platform", "claude"],
                cwd=tmp, capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            skill = os.path.join(tmp, ".claude", "skills", "graphify", "SKILL.md")
            self.assertTrue(os.path.isfile(skill), "SKILL.md was not written")
            self.assertTrue(
                os.path.isdir(os.path.join(tmp, ".claude", "skills", "graphify", "references")),
                "progressive-disclosure references sidecar missing",
            )


class TestEndToEndPipeline(unittest.TestCase):
    """The whole tool, on a corpus written to a temp directory."""

    def test_python_project_extracts_expected_graph(self):
        import json
        import subprocess
        import tempfile

        models = (
            '"""Models."""\n'
            "class User:\n"
            '    """A user."""\n'
            "    def display(self) -> str:\n"
            "        return self.name\n\n"
            "class Admin(User):\n"
            "    def grant(self, target: User) -> bool:\n"
            "        return target.display() is not None\n"
        )
        service = (
            "from models import User, Admin\n\n"
            "def promote(user: User) -> Admin:\n"
            "    admin = Admin()\n"
            "    return admin.grant(user)\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "models.py"), "w") as handle:
                handle.write(models)
            with open(os.path.join(tmp, "service.py"), "w") as handle:
                handle.write(service)
            result = subprocess.run(
                [sys.executable, os.path.join(ROOT, "cmc.py"), "extract", ".", "--no-cluster"],
                cwd=tmp, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(os.path.join(tmp, "graphify-out", "graph.json")) as handle:
                graph = json.load(handle)

        labels = {n["label"] for n in graph["nodes"]}
        self.assertIn("User", labels)
        self.assertIn("Admin", labels)
        relations = {
            (e["source"].split("_")[-1], e["target"].split("_")[-1], e["relation"])
            for e in graph.get("links", graph.get("edges", []))
        }
        self.assertIn(("admin", "user", "inherits"), relations)
        self.assertIn(("user", "display", "method"), relations)
        self.assertIn(("admin", "grant", "method"), relations)
        self.assertIn(("service", "models", "imports_from"), relations)
        # Cross-file call resolution: Admin() in service.py -> the class in models.py.
        self.assertIn(("promote", "admin", "calls"), relations)
        # Cross-file inherited-method call: Admin.grant calls User.display.
        self.assertIn(("grant", "display", "calls"), relations)
        # Type annotations become references.
        self.assertIn(("promote", "user", "references"), relations)


if __name__ == "__main__":
    unittest.main()
