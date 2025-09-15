#!/usr/bin/env bash
set -euo pipefail

# Build Codex CLI container image (always fresh, no cache)
#
# Usage:
#   ./build.sh

cd "$(dirname "$0")"

# Core toolchain and extras are included by default
INCLUDE_TOOLCHAIN=1
INCLUDE_EXTRAS=1

echo "Building codex_container (fresh, no cache, pull base images)..."
echo "Including core native build toolchain in image."
echo "Including extras (clang/lld, ccache, gdb, valgrind, patchelf, wget, unzip, libfreetype6-dev, libpng-dev, libgomp1)."

CMD=(docker build --pull --no-cache -t codex_container)
CMD+=(--build-arg INCLUDE_BUILD_TOOLS=$INCLUDE_TOOLCHAIN)
CMD+=(--build-arg INCLUDE_EXTRA_TOOLS=$INCLUDE_EXTRAS)
CMD+=(.)

"${CMD[@]}"

echo "\nBuild complete: codex_container"
