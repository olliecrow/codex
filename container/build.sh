#!/usr/bin/env bash
set -euo pipefail

# Build Codex CLI container image (always fresh, no cache)

cd "$(dirname "$0")"

echo "Building codex_container (fresh, no cache, pull base images)..."
docker build --pull --no-cache -t codex_container .

echo "\nBuild complete: codex_container"
