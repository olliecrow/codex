#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/codex_common_lib.sh"

usage() {
  cat <<EOF
Usage:
  $(basename "$0")

Description:
  Run non-mutating preflight checks for the Codex container workflow.
EOF
}

if [[ $# -ne 0 ]]; then
  usage
  exit 1
fi

exit_code=0

report_ok() {
  local name="$1"
  local detail="$2"
  echo "[ok] $name: $detail"
}

report_fail() {
  local name="$1"
  local detail="$2"
  echo "[fail] $name: $detail"
  exit_code=1
}

check_tool() {
  local tool="$1"
  if path="$(command -v "$tool" 2>/dev/null)"; then
    report_ok "tool $tool" "$path"
  else
    report_fail "tool $tool" "not found in PATH"
  fi
}

check_path_exists() {
  local label="$1"
  local path="$2"
  if [[ -e "$path" ]]; then
    report_ok "$label" "$path"
  else
    report_fail "$label" "missing ($path)"
  fi
}

echo "codex container doctor"
echo

check_tool docker

HOST_CODEX_DIR="$HOME/.codex"
check_path_exists "host codex dir" "$HOST_CODEX_DIR"
check_path_exists "host codex auth" "$HOST_CODEX_DIR/auth.json"

if docker info >/dev/null 2>&1; then
  report_ok "docker daemon" "reachable"
else
  report_fail "docker daemon" "unreachable, start Docker and retry"
fi

if docker image inspect codex_container >/dev/null 2>&1; then
  report_ok "image codex_container" "present"
else
  report_fail "image codex_container" "missing, run ./container/build.sh"
fi

if [[ "$exit_code" -eq 0 ]]; then
  echo
  echo "doctor result: PASS"
  exit 0
fi

echo
echo "doctor result: FAIL"
exit 1
