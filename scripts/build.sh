#!/usr/bin/env bash
#
# Build the static site into a distribution directory.
#
# Usage:
#     ./scripts/build.sh          # builds into ./dist
#     ./scripts/build.sh outdir   # builds into ./outdir
#
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dist="${1:-dist}"
[[ "$dist" = /* ]] || dist="$root/$dist"

rm -rf "$dist"
mkdir -p "$dist"

python3 "$root/scripts/render_resume.py" "$root/resume.json" -o "$dist/index.html"
cp "$root/frontend/styles.css" "$root/frontend/counter.js" "$dist/"

echo "Built site in $dist"
ls -l "$dist"
