#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/codex_common_lib.sh"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") /path/to/project /path/to/prompts.txt

Description:
  Sequentially feeds prompts to Codex CLI in a single conversation. Prompts are
  separated by blank lines, so each block of text (one or more lines) separated
  by an empty line is treated as a single prompt. A block that begins with
  /compact will trigger the compact command before sending the remainder of the
  block. After the first prompt, Codex's built-in resume support (--last) keeps
  the conversation alive.
EOF
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

PROJECT_DIR=""
PROMPTS_PATH=""

if [[ $# -eq 1 ]]; then
  PROJECT_DIR="$(pwd)"
  PROMPTS_PATH="$1"
else
  PROJECT_DIR="$1"
  PROMPTS_PATH="$2"
fi

if ! validate_directory "$PROJECT_DIR"; then
  exit 1
fi

if [[ ! -f "$PROMPTS_PATH" ]]; then
  echo "Error: prompts file not found: $PROMPTS_PATH" >&2
  exit 1
fi

PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
PROMPTS_FILE="$(cd "$(dirname "$PROMPTS_PATH")" && pwd)/$(basename "$PROMPTS_PATH")"

PROMPTS=()
current_prompt=""
while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%$'\r'}"
  if [[ -z "${line// }" ]]; then
    if [[ -n "${current_prompt// }" ]]; then
      PROMPTS+=("$current_prompt")
      current_prompt=""
    fi
    continue
  fi

  if [[ -n "$current_prompt" ]]; then
    current_prompt+=$'\n'
  fi
  current_prompt+="$line"
done < "$PROMPTS_FILE"

if [[ -n "${current_prompt// }" ]]; then
  PROMPTS+=("$current_prompt")
fi

if [[ ${#PROMPTS[@]} -eq 0 ]]; then
  echo "Error: prompts file is empty: $PROMPTS_FILE" >&2
  exit 1
fi

if ! check_codex_auth; then
  exit 1
fi

log() {
  local msg="$1"
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "[$ts] $msg"
}

HOST_TZ="$(detect_host_timezone)"
HOST_CODEX_DIR="$HOME/.codex"

TEMP_CODEX_DIR="$(mktemp -d /tmp/codex-run.XXXXXX)"
log "Creating isolated Codex workspace at $TEMP_CODEX_DIR"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude 'run-prompts.*' "$HOST_CODEX_DIR/" "$TEMP_CODEX_DIR/"
else
  tar -C "$HOST_CODEX_DIR" --exclude 'run-prompts.*' -cf - . | tar -C "$TEMP_CODEX_DIR" -xf -
fi

PROJECT_NAME="$(basename "$PROJECT_DIR")"
CONTAINER_NAME="codex_prompts_${PROJECT_NAME}_$(date +%s)_$$"
log "Starting container: $CONTAINER_NAME"

CLEANUP_CMDS=(
  "log 'Stopping container $CONTAINER_NAME'"
  "docker rm -f '$CONTAINER_NAME' >/dev/null 2>&1 || true"
  "log 'Removing temporary Codex workspace'"
  "rm -rf '$TEMP_CODEX_DIR'"
)

cleanup() {
  for cmd in "${CLEANUP_CMDS[@]}"; do
    eval "$cmd"
  done
}
trap cleanup EXIT

RUN_ARGS=(
  docker run -d
  --name "$CONTAINER_NAME"
  $(get_base_docker_env_args)
  --mount "type=bind,source=$PROJECT_DIR,target=/workspace"
  --mount "type=bind,source=$TEMP_CODEX_DIR,target=/home/dev/.codex"
)

if [[ -d "$PROJECT_DIR/.git" ]]; then
  RUN_ARGS+=("--mount" "type=bind,source=$PROJECT_DIR/.git,target=/workspace/.git,readonly")
fi
if [[ -n "$HOST_TZ" ]]; then
  RUN_ARGS+=("--env" "TZ=$HOST_TZ")
fi
RUN_ARGS+=(codex_container "tail" "-f" "/dev/null")

"${RUN_ARGS[@]}" >/dev/null
sleep 1
log "Container ready"

run_codex_exec() {
  local prompt_text="$1"
  local use_resume_flag="$2"
  local remote_path="/tmp/run_sequence_prompt.txt"

  log "Copying prompt into container"
  printf '%s\n' "$prompt_text" | docker exec -i "$CONTAINER_NAME" bash -lc "cat > '$remote_path'"

  local cmd="cd /workspace && cat '$remote_path' | codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --config approval_policy=\"never\" --config model=\"gpt-5\" --config model_reasoning_effort=\"high\""
  if [[ "$use_resume_flag" == true ]]; then
    cmd="$cmd resume --last"
    log "Running codex exec with resume --last"
  else
    log "Running codex exec (new session)"
  fi

  docker exec -i "$CONTAINER_NAME" bash -lc "$cmd"
  log "Codex exec finished"
  docker exec "$CONTAINER_NAME" bash -lc "rm -f '$remote_path'" >/dev/null 2>&1 || true
}

TOTAL_MESSAGES=0
for line in "${PROMPTS[@]}"; do
  if [[ $line == /compact* ]]; then
    rest="${line#/compact}"
    rest="${rest# }"
    TOTAL_MESSAGES=$((TOTAL_MESSAGES + 1))
    [[ -n "$rest" ]] && TOTAL_MESSAGES=$((TOTAL_MESSAGES + 1))
  else
    TOTAL_MESSAGES=$((TOTAL_MESSAGES + 1))
  fi
done

log "Total prompts: ${#PROMPTS[@]}, total messages (including compact splits): $TOTAL_MESSAGES"

COUNTER=0
HAVE_SESSION=false
for original in "${PROMPTS[@]}"; do
  if [[ $original == /compact* ]]; then
    rest="${original#/compact}"
    rest="${rest# }"

    COUNTER=$((COUNTER + 1))
    log "Prompt $COUNTER/$TOTAL_MESSAGES: /compact"
    if [[ "$HAVE_SESSION" == true ]]; then
      run_codex_exec "/compact" true
    else
      log "Skipping /compact because no active conversation yet"
    fi

    if [[ -n "$rest" ]]; then
      COUNTER=$((COUNTER + 1))
      log "Prompt $COUNTER/$TOTAL_MESSAGES: $rest"
      run_codex_exec "$rest" "$HAVE_SESSION"
      HAVE_SESSION=true
    fi
  else
    COUNTER=$((COUNTER + 1))
    log "Prompt $COUNTER/$TOTAL_MESSAGES: $original"
    run_codex_exec "$original" "$HAVE_SESSION"
    HAVE_SESSION=true
  fi
done

log "All prompts processed."
