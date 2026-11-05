#!/usr/bin/env bash
#
# Build the static site into a distribution directory.
#
# Usage:
#     ./scripts/build.sh          # builds into ./dist
#     ./scripts/build.sh outdir   # builds into ./outdir
#
# Environment:
#     COUNTER_API_URL   Visitor counter endpoint from cloud-resume-backend.
#                       If unset, the site builds without a visit counter.
#
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dist="${1:-dist}"
[[ "$dist" = /* ]] || dist="$root/$dist"

rm -rf "$dist"
mkdir -p "$dist"

python3 "$root/scripts/render_resume.py" "$root/resume.json" -o "$dist/index.html"
cp "$root/frontend/styles.css" "$root/frontend/counter.js" "$dist/"

api_url="${COUNTER_API_URL:-}"
[[ -n "$api_url" ]] || echo "Warning: COUNTER_API_URL not set; visit counter disabled" >&2
python3 -c 'import json, sys; print(f"window.COUNTER_API_URL = {json.dumps(sys.argv[1] or None)};")' \
  "$api_url" > "$dist/config.js"

echo "Built site in $dist"
ls -l "$dist"
