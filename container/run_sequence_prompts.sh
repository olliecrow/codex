#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/codex_common_lib.sh"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") /path/to/project /path/to/prompts.txt

Description:
  Sequentially feeds prompts to Codex CLI. Prompts are separated by blank lines,
  so each block of text (one or more lines) separated by an empty line is
  treated as a single prompt. A block that begins with /compact finalizes the
  current conversation, captures a handoff summary, and starts a fresh Codex
  conversation seeded with that summary plus any remaining text in the block.
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

HOST_HANDOFF_DIR="$PROJECT_DIR/plan/handoffs"
mkdir -p "$HOST_HANDOFF_DIR"

WORKFLOW_STATUS_FILE="$HOST_HANDOFF_DIR/workflow_status.txt"
WORKFLOW_LOG_FILE="$HOST_HANDOFF_DIR/workflow_log.txt"
echo "STARTED: $(date)" > "$WORKFLOW_STATUS_FILE"
: > "$WORKFLOW_LOG_FILE"

log() {
  local msg="$1"
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "[$ts] $msg"
}

log_message() {
  local message="$1"
  echo "$message"
  if [[ -n "${WORKFLOW_LOG_FILE:-}" ]]; then
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$message" >> "$WORKFLOW_LOG_FILE"
  fi
}

preview_block() {
  local block="$1"
  local preview
  preview=$(echo "$block" | tr '\n' ' ' | sed 's/  */ /g')
  printf '%.160s' "$preview"
}

generate_handoff_prompt() {
  cat <<'EOF'
Generate a comprehensive handoff summary of everything done in this conversation.

Include:
- What was accomplished
- Any files created or modified
- Key decisions or findings
- Current state of the project
- Important context for continuation

Be thorough but concise. This summary will be the only context passed forward.
Output in plain text format.
EOF
}

write_handoff_from_output() {
  local source_file="$1"
  local destination_file="$2"

  if [[ -z "$source_file" || ! -f "$source_file" ]]; then
    printf 'Warning: Missing conversation output for handoff\n' | tee "$destination_file"
    return
  fi

  local summary_header=""
  local header_candidates=(
    "## HANDOFF SUMMARY"
    "## Comprehensive Handoff Summary"
    "## Handoff Summary"
  )

  for header in "${header_candidates[@]}"; do
    if grep -q "^$header" "$source_file"; then
      summary_header="$header"
      break
    fi
  done

  if [[ -n "$summary_header" ]]; then
    awk -v header="$summary_header" '$0 == header {printing=1} printing {print}' "$source_file" > "$destination_file"
    if [[ ! -s "$destination_file" ]]; then
      cp "$source_file" "$destination_file"
    fi
  else
    cp "$source_file" "$destination_file"
  fi
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
  local output_file="${3:-}"
  local remote_path="/tmp/run_sequence_prompt.txt"
  local char_count=${#prompt_text}
  local line_count
  line_count=$(printf '%s\n' "$prompt_text" | awk 'END{print NR}')

  log_message "Copying prompt into container: $remote_path (${line_count} line(s), ${char_count} character(s))"
  printf '%s\n' "$prompt_text" | docker exec -i "$CONTAINER_NAME" bash -lc "cat > '$remote_path'"

  local cmd="cd /workspace && cat '$remote_path' | codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --config approval_policy="never" --config model="gpt-5-codex" --config model_reasoning_effort="high""
  if [[ "$use_resume_flag" == true ]]; then
    cmd="$cmd resume --last"
    log "Running codex exec with resume --last"
  else
    log "Running codex exec (new session)"
  fi

  local exit_code=0
  if [[ -n "$output_file" ]]; then
    log_message "Streaming Codex output to $output_file"
    set +e
    docker exec -i "$CONTAINER_NAME" bash -lc "$cmd" | tee -a "$output_file"
    exit_code=${PIPESTATUS[0]}
    set -e
  else
    set +e
    docker exec -i "$CONTAINER_NAME" bash -lc "$cmd"
    exit_code=$?
    set -e
  fi

  log "Codex exec finished (exit code: $exit_code)"
  docker exec "$CONTAINER_NAME" bash -lc "rm -f '$remote_path'" >/dev/null 2>&1 || true
  log_message "Removed temporary prompt file from container: $remote_path"

  if [[ $exit_code -ne 0 ]]; then
    return $exit_code
  fi

  return 0
}

run_prompt_with_handoff() {
  local prompt_text="$1"
  local conversation_num="$2"
  local is_handoff_continuation="$3"
  local previous_handoff="$4"
  local conversation_output_file="$HOST_HANDOFF_DIR/conversation_${conversation_num}_output.txt"

  log_message "=================================="
  log_message "Conversation $conversation_num"
  log_message "=================================="

  local full_prompt
  if [[ "$is_handoff_continuation" == true && -n "$previous_handoff" ]]; then
    full_prompt="Previous conversation summary:
$previous_handoff

Current task:
$prompt_text"
  else
    full_prompt="$prompt_text"
  fi

  local preview
  preview="$(echo "$prompt_text" | head -c 100)"
  if [[ ${#prompt_text} -gt 100 ]]; then
    log_message "Prompt preview: ${preview}..."
  else
    log_message "Prompt: $preview"
  fi

  log_message "Conversation $conversation_num output file: $conversation_output_file"
  : > "$conversation_output_file"

  log_message "Starting Codex conversation..."
  run_codex_exec "$full_prompt" false "$conversation_output_file"
  local exit_code=$?

  log_message "Conversation $conversation_num completed (exit code: $exit_code)"
  log_message "Conversation $conversation_num raw output captured at $conversation_output_file"
  LAST_CONVERSATION_OUTPUT_FILE="$conversation_output_file"

  return $exit_code
}

process_current_conversation() {
  if [[ ${#CURRENT_CONVERSATION_PROMPTS[@]} -eq 0 ]]; then
    log_message "Conversation $CONVERSATION_NUM: no queued prompt blocks to process."
    return
  fi

  local combined_prompt=""
  log_message "Conversation $CONVERSATION_NUM: combining ${#CURRENT_CONVERSATION_PROMPTS[@]} block(s): ${CURRENT_BLOCK_IDS[*]}"
  for idx in "${!CURRENT_CONVERSATION_PROMPTS[@]}"; do
    local prompt_block="${CURRENT_CONVERSATION_PROMPTS[$idx]}"
    local block_ref="${CURRENT_BLOCK_IDS[$idx]:-?}"
    log_message " - Block ${block_ref} preview: $(preview_block "$prompt_block")"
    if [[ -n "$combined_prompt" ]]; then
      combined_prompt+=$'\n\n'
    fi
    combined_prompt+="$prompt_block"
  done

  combined_prompt+=$'\n\n'
  combined_prompt+="$(generate_handoff_prompt)"
  log_message "Conversation $CONVERSATION_NUM: auto handoff summary prompt appended."

  if [[ $CONVERSATION_NUM -eq 1 ]]; then
    run_prompt_with_handoff "$combined_prompt" "$CONVERSATION_NUM" false ""
  else
    run_prompt_with_handoff "$combined_prompt" "$CONVERSATION_NUM" true "$PREVIOUS_HANDOFF"
  fi

  local handoff_file="$HOST_HANDOFF_DIR/prompt_${CONVERSATION_NUM}_handoff.txt"
  write_handoff_from_output "$LAST_CONVERSATION_OUTPUT_FILE" "$handoff_file"
  if [[ -f "$handoff_file" ]]; then
    PREVIOUS_HANDOFF="$(cat "$handoff_file")"
    log_message "Handoff saved: $handoff_file"
  else
    PREVIOUS_HANDOFF=""
    log_message "Warning: handoff file missing for conversation $CONVERSATION_NUM"
  fi

  CURRENT_CONVERSATION_PROMPTS=()
  CURRENT_BLOCK_IDS=()
  CONVERSATION_NUM=$((CONVERSATION_NUM + 1))
}

log_message "Prompt file: $PROMPTS_FILE"
log_message "Project directory: $PROJECT_DIR"
log_message "Total prompt blocks detected: ${#PROMPTS[@]}"

for idx in "${!PROMPTS[@]}"; do
  block_num=$((idx + 1))
  block_text="${PROMPTS[$idx]}"
  if [[ $block_text == /compact* ]]; then
    log_message "Block #$block_num: /compact marker encountered."
  else
    log_message "Block #$block_num preview: $(preview_block "$block_text")"
  fi
done

log "Total prompt blocks: ${#PROMPTS[@]}"

CONVERSATION_NUM=1
CURRENT_CONVERSATION_PROMPTS=()
CURRENT_BLOCK_IDS=()
PREVIOUS_HANDOFF=""
FIRST_PROMPT=""
LAST_CONVERSATION_OUTPUT_FILE=""

for idx in "${!PROMPTS[@]}"; do
  prompt_block="${PROMPTS[$idx]}"
  block_num=$((idx + 1))

  if [[ $CONVERSATION_NUM -eq 1 && -z "$FIRST_PROMPT" ]]; then
    FIRST_PROMPT="$prompt_block"
    echo "$FIRST_PROMPT" > "$HOST_HANDOFF_DIR/initial_task.txt"
    log_message "Initial task saved to $HOST_HANDOFF_DIR/initial_task.txt (block #$block_num)."
  fi

  if [[ $prompt_block == /compact* ]]; then
    log_message "Block #$block_num issued /compact. Processing current queue for conversation $CONVERSATION_NUM."
    process_current_conversation

    rest="${prompt_block#/compact}"
    rest="${rest# }"
    CURRENT_BLOCK_IDS=()
    if [[ -n "$rest" ]]; then
      log_message "Block #$block_num remainder queued for next conversation: $(preview_block "$rest")"
      CURRENT_CONVERSATION_PROMPTS+=("$rest")
      CURRENT_BLOCK_IDS+=("${block_num}*")
    fi
  else
    CURRENT_CONVERSATION_PROMPTS+=("$prompt_block")
    CURRENT_BLOCK_IDS+=("$block_num")
    log_message "Queued block #$block_num for conversation $CONVERSATION_NUM (queued blocks: ${CURRENT_BLOCK_IDS[*]})."
  fi
done

process_current_conversation

echo "COMPLETED: $(date)" >> "$WORKFLOW_STATUS_FILE"

log "All prompts processed."
log_message "All prompts processed successfully. Conversations executed: $((CONVERSATION_NUM - 1))"
log_message "Handoff files saved in: $HOST_HANDOFF_DIR"
