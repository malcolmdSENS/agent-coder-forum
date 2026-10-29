#!/usr/bin/env bash
# Copy the Pastey scripts and skills into one or more projects.
# Usage: ./install-to-project.sh <project-dir> [<project-dir> ...]
set -euo pipefail

src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -eq 0 ]; then
  echo "Usage: $0 <project-dir> [<project-dir> ...]" >&2
  exit 1
fi

status=0
for dest in "$@"; do
  if [ ! -d "$dest" ]; then
    echo "Skipping '$dest': not a directory" >&2
    status=1
    continue
  fi

  mkdir -p "$dest/scripts" "$dest/.github/skills"
  cp -v "$src"/scripts/pastey_*.py "$dest/scripts/"
  for skill in "$src"/.github/skills/pastey-*/; do
    name="$(basename "$skill")"
    rm -rf "$dest/.github/skills/$name"
    cp -rv "$skill" "$dest/.github/skills/$name"
  done

  # Remove legacy locations from earlier installs (prompts are now skills)
  rm -fv "$dest"/.github/prompts/pastey-*.prompt.md
  rm -rfv "$dest/.copilot/skills/pastey-api"
  rmdir "$dest/.github/prompts" "$dest/.copilot/skills" "$dest/.copilot" 2>/dev/null || true
  echo "Updated $dest"
done

exit $status
