#!/usr/bin/env bash
# Copy the Pastey scripts, prompt commands and skill into one or more projects.
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

  mkdir -p "$dest/scripts" "$dest/.github/prompts" "$dest/.copilot/skills"
  cp -v "$src"/scripts/pastey_*.py "$dest/scripts/"
  cp -v "$src"/.github/prompts/pastey-*.prompt.md "$dest/.github/prompts/"
  cp -rv "$src/.copilot/skills/pastey-api" "$dest/.copilot/skills/"
  echo "Updated $dest"
done

exit $status
