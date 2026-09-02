#!/usr/bin/env bash
# Package each skill as its own zip for upload to claude.ai or the Claude desktop app.
#
# Each zip holds one skill folder at its root, which is the shape the Skills settings
# page expects:
#     humanizer.zip -> humanizer/SKILL.md, humanizer/references/...
#
# Output goes to dist/, which is gitignored.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="$repo_root/plugins/cloverleaf-sales/skills"
dist_dir="$repo_root/dist"

if [ ! -d "$skills_dir" ]; then
  echo "No skills directory at $skills_dir" >&2
  exit 1
fi

rm -rf "$dist_dir"
mkdir -p "$dist_dir"

count=0
for skill_path in "$skills_dir"/*/; do
  skill="$(basename "$skill_path")"
  [ -f "$skill_path/SKILL.md" ] || { echo "Skipping $skill: no SKILL.md" >&2; continue; }
  (cd "$skills_dir" && zip -q -r "$dist_dir/$skill.zip" "$skill" -x '*.DS_Store' -x '*__pycache__*')
  size="$(du -h "$dist_dir/$skill.zip" | cut -f1 | tr -d ' ')"
  printf '  %-32s %s\n' "$skill.zip" "$size"
  count=$((count + 1))
done

echo
echo "Packaged $count skills into $dist_dir"
echo "Upload them at claude.ai > Settings > Capabilities > Skills, or hand them to an org admin."
