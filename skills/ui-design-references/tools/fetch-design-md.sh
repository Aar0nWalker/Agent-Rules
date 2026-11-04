#!/usr/bin/env bash
# Скачать DESIGN.md бренда из VoltAgent/awesome-design-md (MIT) в docs/design-refs/<brand>.md.
# Использование: bash fetch-design-md.sh <brand>   |   bash fetch-design-md.sh --list
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
if [[ "${1:-}" == "--list" || -z "${1:-}" ]]; then
  curl -fsS --max-time 20 "https://api.github.com/repos/VoltAgent/awesome-design-md/contents/design-md" \
    | python -c "import sys,json; print(' '.join(x['name'] for x in json.load(sys.stdin)))"
  exit 0
fi
brand="$1"
case "$brand" in *[!a-z0-9.-]*) echo "bad brand name" >&2; exit 1;; esac
mkdir -p "$root/docs/design-refs"
out="$root/docs/design-refs/$brand.md"
curl -fsS --max-time 30 "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/$brand/DESIGN.md" -o "$out"
echo "$out ($(wc -l < "$out") строк)"
