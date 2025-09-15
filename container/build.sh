#!/usr/bin/env bash
set -euo pipefail

# Build Codex CLI container image (always fresh, no cache)
#
# Usage:
#   ./build.sh [--with-toolchain]
#
# Flags:
#   --with-toolchain  Include C/C++ build tools (build-essential, pkg-config)

cd "$(dirname "$0")"

INCLUDE_TOOLCHAIN=0
if [[ "${1:-}" == "--with-toolchain" ]]; then
  INCLUDE_TOOLCHAIN=1
fi

echo "Building codex_container (fresh, no cache, pull base images)..."
if [[ "$INCLUDE_TOOLCHAIN" -eq 1 ]]; then
  echo "Including C/C++ build toolchain in image."
fi

CMD=(docker build --pull --no-cache -t codex_container)
if [[ "$INCLUDE_TOOLCHAIN" -eq 1 ]]; then
  CMD+=(--build-arg INCLUDE_BUILD_TOOLS=1)
fi
CMD+=(.)

"${CMD[@]}"

echo "\nBuild complete: codex_container"
