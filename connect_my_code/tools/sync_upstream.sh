#!/bin/sh
# Re-sync the bundled graphify package from upstream.
#
#   tools/sync_upstream.sh [git-ref]
#
# Because nothing under graphify/ is ever edited, updating to a newer upstream
# is a directory copy rather than a merge. This script performs that copy, then
# refreshes the two things derived from upstream metadata:
#
#   UPSTREAM_COMMIT                              the pinned revision
#   runtime/dist/graphifyy-<version>.dist-info   what importlib.metadata reports
#
# After running it, always run ./cmc selftest. A new upstream release can start
# reading grammar node types the bundled parsers do not emit yet, and the
# per-language tests are what surface that.
set -e

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
REF=${1:-main}
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

echo "Cloning upstream at $REF ..."
git clone --quiet https://github.com/Graphify-Labs/graphify "$WORK/graphify"
git -C "$WORK/graphify" checkout --quiet "$REF"

COMMIT=$(git -C "$WORK/graphify" rev-parse HEAD)
DESCRIBE=$(git -C "$WORK/graphify" describe --tags --always 2>/dev/null || echo "")
VERSION=$(sed -n 's/^version = "\(.*\)"/\1/p' "$WORK/graphify/pyproject.toml" | head -1)

if [ -z "$VERSION" ]; then
    echo "Could not read version from upstream pyproject.toml" >&2
    exit 1
fi

echo "Upstream $COMMIT ($DESCRIBE), version $VERSION"

echo "Replacing graphify/ ..."
rm -rf "$ROOT/graphify"
cp -R "$WORK/graphify/graphify" "$ROOT/graphify"
find "$ROOT/graphify" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

for f in LICENSE LICENSE-MIT NOTICE; do
    [ -f "$WORK/graphify/$f" ] && cp "$WORK/graphify/$f" "$ROOT/$f"
done

printf '%s\n%s\n' "$COMMIT" "$DESCRIBE" > "$ROOT/UPSTREAM_COMMIT"

echo "Refreshing stub dist-info ..."
rm -rf "$ROOT"/runtime/dist/graphifyy-*.dist-info
DIST="$ROOT/runtime/dist/graphifyy-$VERSION.dist-info"
mkdir -p "$DIST"
cat > "$DIST/METADATA" <<EOF
Metadata-Version: 2.1
Name: graphifyy
Version: $VERSION
Summary: connect_my_code -- zero-install portable distribution of the graphify knowledge-graph tool
License: Apache-2.0
Requires-Python: >=3.10
EOF
echo "connect_my_code" > "$DIST/INSTALLER"

echo
echo "Done. Upstream is now $COMMIT ($VERSION)."
echo "Next: ./cmc selftest    # verifies the bundled parsers still satisfy this release"
