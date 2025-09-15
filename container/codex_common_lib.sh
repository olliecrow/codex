#!/usr/bin/env bash
# codex_common_lib.sh - Common utilities for Codex scripts
#
# IMPORTANT: This library:
# - Does NOT set any trap handlers (scripts manage their own)
# - Does NOT call exit (returns error codes instead)
# - Does NOT output to stderr (maintains stdout for compatibility)
# - Does NOT source other libraries (avoid circular dependencies)

set -euo pipefail

# Detect host timezone (Linux/macOS heuristics)
detect_host_timezone() {
  local HOST_TZ=""
  if [ -f "/etc/localtime" ]; then
    HOST_TZ=$(readlink /etc/localtime 2>/dev/null | sed 's|.*/zoneinfo/||') || true
  fi
  if [ -z "${HOST_TZ:-}" ]; then
    HOST_TZ=$(systemsetup -gettimezone 2>/dev/null | awk -F': ' '{print $2}') || true
  fi
  if [ -z "${HOST_TZ:-}" ]; then
    HOST_TZ=$(date +%Z 2>/dev/null) || true
  fi
  echo "${HOST_TZ:-}"
}

# Check Codex authentication presence (directory check, like-for-like minimal)
check_codex_auth() {
  if [ ! -d "$HOME/.codex" ]; then
    echo "Error: No Codex authentication found on your system"
    echo "Please run 'codex login' on your host and try again"
    return 1
  fi
  return 0
}

# Validate directory exists
validate_directory() {
  local dir="$1"
  if [ ! -d "$dir" ]; then
    echo "Error: Directory '$dir' does not exist"
    return 1
  fi
  return 0
}

# Get absolute path of directory (assumes already validated)
get_absolute_path() {
  local dir="$1"
  cd "$dir" && pwd
}

# Get base Docker environment args as a string
# Usage: Add $(get_base_docker_env_args) to docker run command
get_base_docker_env_args() {
  echo "--network bridge \
--user 1000:1000 \
--workdir /workspace \
--env TERM=xterm-256color"
}

