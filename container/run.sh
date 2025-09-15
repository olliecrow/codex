#!/usr/bin/env bash
set -euo pipefail

# Run Codex CLI inside container with:
# - Full autonomy (no approvals, no OS sandbox)
# - Internet access inside the container
# - Host isolation: only /workspace (project) and ~/.codex are mounted
# - Git disabled via wrappers and no package install

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") /path/to/project [--shell]

Description:
  Launches the codex_container with the project mounted at /workspace and the host
  Codex config mounted at /home/dev/.codex. Starts Codex TUI by default, or a
  login shell if --shell is provided.

Notes:
  - Requires that you have already logged into Codex on the host so that
    ~/.codex/auth.json exists. The container mounts ~/.codex for auth.
  - The .git directory (if present) is mounted read-only to prevent repo mutations.
  - Codex runs with --dangerously-bypass-approvals-and-sandbox and approval_policy=never.
EOF
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

REPO_DIR="$1"
MODE="${2:-}"

if [[ ! -d "$REPO_DIR" ]]; then
  echo "Error: directory not found: $REPO_DIR" >&2
  exit 1
fi

# Resolve absolute path
REPO_DIR="$(cd "$REPO_DIR" && pwd)"

# Detect host timezone (macOS/Linux)
detect_host_timezone() {
  local tz=""
  if [[ -L "/etc/localtime" ]]; then
    tz=$(readlink /etc/localtime 2>/dev/null | sed 's|.*/zoneinfo/||') || true
  fi
  if [[ -z "$tz" && $(uname -s) == "Darwin" ]]; then
    tz=$(systemsetup -gettimezone 2>/dev/null | awk -F': ' '{print $2}') || true
  fi
  echo "$tz"
}

HOST_TZ="$(detect_host_timezone)"
if [[ -n "$HOST_TZ" ]]; then
  echo "Host timezone detected: $HOST_TZ"
else
  echo "Warning: could not detect timezone; container will use UTC"
fi

# Verify host Codex auth exists (best-effort)
HOST_CODEX_DIR="$HOME/.codex"
if [[ ! -d "$HOST_CODEX_DIR" ]]; then
  echo "Error: $HOST_CODEX_DIR not found. Please run 'codex login' on your host first." >&2
  exit 1
fi
if [[ ! -f "$HOST_CODEX_DIR/auth.json" ]]; then
  echo "Error: $HOST_CODEX_DIR/auth.json not found. Please run 'codex login' on your host first." >&2
  exit 1
fi

CONTAINER_NAME="codex_$(basename "$REPO_DIR")_$$"
echo "Starting container: $CONTAINER_NAME"

RUN_ARGS=(
  docker run -d
  --name "$CONTAINER_NAME"
  --network bridge
  --user 1000:1000
  --workdir /workspace
  --mount "type=bind,source=$REPO_DIR,target=/workspace"
  --mount "type=bind,source=$HOST_CODEX_DIR,target=/home/dev/.codex"
)

# Mount .git as read-only if present to prevent repo mutations
if [[ -d "$REPO_DIR/.git" ]]; then
  RUN_ARGS+=(--mount "type=bind,source=$REPO_DIR/.git,target=/workspace/.git,readonly")
fi

if [[ -n "$HOST_TZ" ]]; then
  RUN_ARGS+=(--env TZ="$HOST_TZ")
fi

RUN_ARGS+=(codex_container tail -f /dev/null)

"${RUN_ARGS[@]}" >/dev/null

cleanup() {
  echo "Cleaning up container..."
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Entering container..."
if [[ "$MODE" == "--shell" ]]; then
  docker exec -it "$CONTAINER_NAME" bash --login
else
  # Launch Codex TUI in fully autonomous mode, using desired model settings
  docker exec -it "$CONTAINER_NAME" bash -lc \
    'codex --dangerously-bypass-approvals-and-sandbox \
           --cd /workspace \
           --config approval_policy="never" \
           --config model="gpt-5" \
           --config model_reasoning_effort="high"'
fi

echo "Container session ended."
