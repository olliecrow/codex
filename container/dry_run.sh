#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/codex_common_lib.sh"

CONTAINER_CODEX_HOME="/home/dev/.codex-container"
CONTAINER_CONFIG_FILE="$CONTAINER_CODEX_HOME/config.toml"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") /path/to/project [--shell]

Description:
  Print the exact Codex container execution plan without running Docker.
EOF
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

REPO_DIR="$1"
MODE="${2:-}"

if [[ -n "$MODE" && "$MODE" != "--shell" ]]; then
  echo "Error: unsupported mode '$MODE'" >&2
  usage
  exit 1
fi

if ! validate_directory "$REPO_DIR"; then
  exit 1
fi

REPO_DIR="$(get_absolute_path "$REPO_DIR")"
HOST_CODEX_DIR="$HOME/.codex"
HOST_TZ="$(detect_host_timezone)"

container_name="codex_$(basename "$REPO_DIR")_<pid>"
session_mode="codex tui"
if [[ "$MODE" == "--shell" ]]; then
  session_mode="interactive shell"
fi

echo "codex container dry-run"
echo "repo: $REPO_DIR"
echo "mode: $session_mode"
echo "container name: $container_name"
echo

echo "planned sequence:"
echo "1. Validate local prerequisites: docker available and host auth at $HOST_CODEX_DIR/auth.json."
echo "2. Start detached container with /workspace bind mount and /home/dev/.codex auth mount."
if [[ -d "$REPO_DIR/.git" ]]; then
  echo "3. Add read-only bind mount for $REPO_DIR/.git to protect repository history."
else
  echo "3. Skip read-only .git mount because no .git directory was found in the target path."
fi
echo "4. Write container config to $CONTAINER_CONFIG_FILE with approval_policy=never and sandbox_mode=danger-full-access."
if [[ "$MODE" == "--shell" ]]; then
  echo "5. Open a login shell inside the container."
else
  echo "5. Launch Codex TUI inside the container with --dangerously-bypass-approvals-and-sandbox."
fi
echo "6. Remove the container on exit."
echo

echo "docker run preview:"
echo "docker run -d --name \"$container_name\" \\"
echo "  --network bridge --user 1000:1000 --workdir /workspace \\"
echo "  --mount \"type=bind,source=$REPO_DIR,target=/workspace\" \\"
echo "  --mount \"type=bind,source=$HOST_CODEX_DIR,target=/home/dev/.codex\" \\"
if [[ -d "$REPO_DIR/.git" ]]; then
  echo "  --mount \"type=bind,source=$REPO_DIR/.git,target=/workspace/.git,readonly\" \\"
fi
if [[ -n "$HOST_TZ" ]]; then
  echo "  --env TZ=\"$HOST_TZ\" \\"
fi
echo "  --env CODEX_HOME=\"$CONTAINER_CODEX_HOME\" \\"
echo "  codex_container tail -f /dev/null"
echo

echo "dry-run only: no Docker commands were executed."
