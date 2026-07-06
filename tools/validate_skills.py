"""Fable Skills CI validator (PLAN.md section 4).

Stdlib-only. Scans skills/*/SKILL.md and enforces library policy on top of
the Agent Skills spec. Distinguishes LIBRARY-policy failures from SPEC
failures in every message.

Usage:
    python tools/validate_skills.py [--run-scripts] [skill-name ...]

With no skill names, validates every folder under skills/. --run-scripts
additionally invokes each scripts/*.py with --self-test (scripts must exit
0; AUTHORING-GUIDE convention). Exit code 0 = all pass, 1 = errors.
"""

import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

SPEC_NAME_MAX = 64
SPEC_DESC_MAX_BYTES = 1024  # spec limit; Codex counts bytes
LIB_DESC_MAX = 500          # library policy (chars)
LIB_BODY_MAX_LINES = 500    # library policy
STALE_DAYS = 90             # warning aid for the re-verification owner

# Throwaway Phase 0 canary: exempt from library completeness rules
# (SOURCES.md, evals). Format rules still apply. Delete after the gate.
COMPLETENESS_EXEMPT = {"phase0-canary"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BACKSLASH_PATH_RE = re.compile(r"[A-Za-z0-9_.)\]]+\\[A-Za-z0-9_]")


def parse_frontmatter(text):
    """Minimal parser for our controlled frontmatter. Returns (dict, body)
    or (None, None) if the frontmatter block is missing/unclosed."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    fm = {}
    current_map = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fm, "\n".join(lines[i + 1:])
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current_map is not None:
            key, _, value = line.strip().partition(":")
            fm[current_map][key.strip()] = value.strip().strip('"').strip("'")
        elif ":" in line:
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            if value == "":
                current_map = key
                fm[key] = {}
            else:
                current_map = None
                fm[key] = value.strip('"').strip("'")
    return None, None  # never saw the closing ---


def validate_skill(skill_dir, run_scripts=False):
    errors, warnings = [], []
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return [f"SKILL.md missing"], warnings

    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        return ["frontmatter block missing or unclosed (--- ... ---)"], warnings

    # --- name (spec) ---
    fm_name = fm.get("name", "")
    if not fm_name:
        errors.append("SPEC: frontmatter 'name' missing")
    else:
        if fm_name != name:
            errors.append(f"SPEC: name '{fm_name}' != folder '{name}'")
        if not NAME_RE.match(fm_name):
            errors.append(f"SPEC: name '{fm_name}' not lowercase-hyphen")
        if len(fm_name) > SPEC_NAME_MAX:
            errors.append(f"SPEC: name exceeds {SPEC_NAME_MAX} chars")

    # --- description (spec + library policy) ---
    desc = fm.get("description", "")
    if not desc:
        errors.append("SPEC: frontmatter 'description' missing")
    else:
        desc_bytes = len(desc.encode("utf-8"))
        if desc_bytes > SPEC_DESC_MAX_BYTES:
            errors.append(
                f"SPEC: description {desc_bytes} bytes > {SPEC_DESC_MAX_BYTES} "
                "(hard spec limit; Codex counts bytes)")
        elif len(desc) > LIB_DESC_MAX:
            errors.append(
                f"LIBRARY: description {len(desc)} chars > {LIB_DESC_MAX} "
                f"(library policy — spec allows {SPEC_DESC_MAX_BYTES} bytes, "
                "we deliberately stop at 500)")
        if "use this skill when" not in desc.lower():
            warnings.append("description lacks 'Use this skill when' trigger clause")

    # --- metadata (library policy) ---
    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        errors.append("LIBRARY: metadata block missing (version, last-verified)")
    else:
        if not meta.get("version"):
            errors.append("LIBRARY: metadata.version missing")
        lv = meta.get("last-verified", "")
        if not lv:
            errors.append("LIBRARY: metadata.last-verified missing")
        else:
            try:
                lv_date = datetime.strptime(lv, "%Y-%m-%d").date()
                if (date.today() - lv_date).days > STALE_DAYS:
                    warnings.append(f"last-verified {lv} older than {STALE_DAYS} days")
            except ValueError:
                errors.append(f"LIBRARY: last-verified '{lv}' not YYYY-MM-DD")

    # --- body (library policy) ---
    body_lines = len(body.splitlines())
    if body_lines >= LIB_BODY_MAX_LINES:
        errors.append(
            f"LIBRARY: body {body_lines} lines >= {LIB_BODY_MAX_LINES}")

    # --- forward-slash paths (library policy) ---
    for fname in ("SKILL.md", "README.md"):
        f = skill_dir / fname
        if f.is_file() and BACKSLASH_PATH_RE.search(f.read_text(encoding="utf-8")):
            warnings.append(f"{fname}: backslash path-like string (use forward slashes)")

    # --- completeness (library policy) ---
    if not (skill_dir / "README.md").is_file():
        errors.append("LIBRARY: README.md missing")
    if name not in COMPLETENESS_EXEMPT:
        if not (skill_dir / "references" / "SOURCES.md").is_file():
            errors.append("LIBRARY: references/SOURCES.md missing")
        triggers = skill_dir / "evals" / "triggers.json"
        if not triggers.is_file():
            errors.append("LIBRARY: evals/triggers.json missing")
        else:
            try:
                data = json.loads(triggers.read_text(encoding="utf-8"))
                cases = data.get("cases", [])
                if not any(c.get("expect") == "no-trigger" for c in cases):
                    warnings.append("evals: no near-miss (no-trigger) cases")
            except (json.JSONDecodeError, AttributeError) as exc:
                errors.append(f"LIBRARY: evals/triggers.json invalid JSON ({exc})")
        if not (skill_dir / "evals" / "output-cases.md").is_file():
            errors.append("LIBRARY: evals/output-cases.md missing")

    # --- script invocation (Windows CI test) ---
    scripts = sorted((skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").is_dir() else []
    if run_scripts:
        for script in scripts:
            try:
                proc = subprocess.run(
                    [sys.executable, str(script), "--self-test"],
                    capture_output=True, text=True, timeout=30)
                if proc.returncode != 0:
                    errors.append(
                        f"scripts/{script.name} --self-test exit {proc.returncode}: "
                        f"{(proc.stderr or proc.stdout)[:200]}")
            except subprocess.TimeoutExpired:
                errors.append(f"scripts/{script.name} --self-test timed out (30s)")

    return errors, warnings


def main(argv):
    run_scripts = "--run-scripts" in argv
    names = [a for a in argv if not a.startswith("--")]
    if not SKILLS_DIR.is_dir():
        print(f"FAIL: {SKILLS_DIR} does not exist")
        return 1
    dirs = ([SKILLS_DIR / n for n in names] if names
            else sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir()))
    total_errors = 0
    for d in dirs:
        if not d.is_dir():
            print(f"FAIL {d.name}: no such skill folder")
            total_errors += 1
            continue
        errors, warnings = validate_skill(d, run_scripts=run_scripts)
        status = "FAIL" if errors else "PASS"
        total_errors += len(errors)
        print(f"{status} {d.name}"
              + (f" ({len(errors)} errors, {len(warnings)} warnings)"
                 if errors or warnings else ""))
        for e in errors:
            print(f"  ERROR   {e}")
        for w in warnings:
            print(f"  warning {w}")
    print(f"\n{len(dirs)} skill(s) checked, {total_errors} error(s).")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
