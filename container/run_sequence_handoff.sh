#!/usr/bin/env bash

# Codex Sequential Workflow with Context Handoffs
# Each stage runs as a separate conversation with structured summaries passed between

set -euo pipefail

# Source common library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/codex_common_lib.sh"

# Usage and help functions
show_usage() {
  cat << EOF
Usage: 
  $0 <initial_task>                    # Execute in current directory
  $0 <project_directory> <initial_task> # Execute in specified directory
  $0 --help | -h                      # Show this help

Description:
  Runs a multi-stage Codex workflow with context handoffs.
  Each stage runs as a separate conversation with structured summaries.

Arguments:
  project_directory    Path to your project directory (optional, defaults to current)
  initial_task        Description of the task to complete (supports multi-line)

Examples:
  $0 "Analyze and fix test suite"
  $0 /path/to/project "Build a calculator app"
  $0 ~/myproject "Review code and suggest improvements"

Monitoring:
  - Watch terminal output for real-time progress
  - Check /workspace/plan/handoffs/ for stage files and status

Files Created:
  /workspace/plan/handoffs/workflow_status.txt    # Current status
  /workspace/plan/handoffs/workflow_log.txt       # Complete log
  /workspace/plan/handoffs/stage_N_handoff.txt    # Stage summaries
EOF
}

# Handle help flags
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  show_usage
  exit 0
fi

# Input validation and argument parsing
if [ $# -eq 0 ]; then
  echo "Error: No arguments provided"
  echo ""
  show_usage
  exit 1
elif [ $# -eq 1 ]; then
  # Single argument: use current directory, argument is task
  if [ -z "$1" ]; then
    echo "Error: Initial task cannot be empty"
    echo ""
    show_usage
    exit 1
  fi
  REPO_DIR="$(pwd)"
  # Verify current directory is valid
  if ! validate_directory "$REPO_DIR"; then
    exit 1
  fi
  INITIAL_TASK="$1"
elif [ $# -eq 2 ]; then
  # Two arguments: first is directory, second is task
  if [ -z "$1" ]; then
    echo "Error: Project directory cannot be empty"
    echo ""
    show_usage
    exit 1
  fi
  if [ -z "$2" ]; then
    echo "Error: Initial task cannot be empty"
    echo ""
    show_usage
    exit 1
  fi
  if ! validate_directory "$1"; then
    exit 1
  fi
  REPO_DIR="$(get_absolute_path "$1")"  # Get absolute path
  INITIAL_TASK="$2"
else
  echo "Error: Too many arguments provided"
  echo ""
  show_usage
  exit 1
fi

SESSION_ID=$(uuidgen 2>/dev/null || echo "session-$$-$(date +%s)")

# Check Codex authentication exists (like-for-like minimal)
if ! check_codex_auth; then
  exit 1
fi

# Detect host timezone
HOST_TZ="$(detect_host_timezone)"

# Host-side paths (for file operations on host)
HOST_PLAN_DIR="$REPO_DIR/plan"
HOST_HANDOFF_DIR="$HOST_PLAN_DIR/handoffs"

# Container-side paths (for referencing inside container)
CONTAINER_HANDOFF_DIR="/workspace/plan/handoffs"
STATUS_FILE="$HOST_HANDOFF_DIR/workflow_status.txt"
LOG_FILE="$HOST_HANDOFF_DIR/workflow_log.txt"

# Create plan directory structure on host (will be mounted as /workspace/plan in container)
mkdir -p "$HOST_PLAN_DIR"

# Logging function with timestamps
log_with_timestamp() {
  local message="$1"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Create fresh handoff directory (cleanup previous runs)
if [ -d "$HOST_HANDOFF_DIR" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🧹 Cleaning up previous handoff directory..."
  rm -rf "$HOST_HANDOFF_DIR"/*
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Previous handoffs cleared"
fi
mkdir -p "$HOST_HANDOFF_DIR"

# Initialize tracking files
echo "Workflow started at $(date)" > "$LOG_FILE"
echo "WORKFLOW_STATUS=INITIALIZING" > "$STATUS_FILE"
log_with_timestamp "📁 Fresh handoff directory created: $HOST_HANDOFF_DIR"

# Update workflow status
update_workflow_status() {
  local status="$1"
  local current_stage="${2:-}"
  local details="${3:-}"

  echo "WORKFLOW_STATUS=$status" > "$STATUS_FILE"
  echo "CURRENT_STAGE=$current_stage" >> "$STATUS_FILE"
  echo "SESSION_ID=$SESSION_ID" >> "$STATUS_FILE"
  echo "LAST_UPDATE=$(date)" >> "$STATUS_FILE"
  if [ -n "$details" ]; then
    echo "DETAILS=$details" >> "$STATUS_FILE"
  fi

  log_with_timestamp "Status updated: $status ${current_stage:+- Stage: $current_stage} ${details:+- $details}"
}

# Simple retry mechanism for Codex operations (one retry)
retry_codex_operation() {
  local operation_description="$1"
  local operation_command="$2"
  local max_retries=1

  for attempt in 1 2; do
    log_with_timestamp "🔄 $operation_description (attempt $attempt)"

    if eval "$operation_command"; then
      if [ $attempt -eq 2 ]; then
        log_with_timestamp "✅ $operation_description succeeded on retry"
      fi
      return 0
    else
      local exit_code=$?
      if [ $attempt -le $max_retries ]; then
        log_with_timestamp "⚠️  $operation_description failed (attempt $attempt), retrying in 5 seconds..."
        sleep 5
      else
        log_with_timestamp "❌ $operation_description failed after $max_retries retry (exit code: $exit_code)"
        return $exit_code
      fi
    fi
  done
}

log_with_timestamp "=================================="
log_with_timestamp "Codex Handoff Workflow STARTED"
log_with_timestamp "=================================="
log_with_timestamp "Project: $REPO_DIR"
log_with_timestamp "Session ID: $SESSION_ID"
if [ -n "$HOST_TZ" ]; then
  log_with_timestamp "Host timezone: $HOST_TZ"
fi
log_with_timestamp "Handoff Dir: $HOST_HANDOFF_DIR"
log_with_timestamp "Status File: $STATUS_FILE"
log_with_timestamp "Log File: $LOG_FILE"
log_with_timestamp ""

update_workflow_status "STARTING" "" "Initializing workflow components"

# PRODUCTION STAGES
# If SHORT_WORKFLOW=1, run a reduced set of stages to speed up validation while preserving coverage.
if [[ "${SHORT_WORKFLOW:-}" == "1" ]]; then
  STAGES=(
    "investigate"
    "plan"
    "executeverify"
    "cleanup"
    "summary"
  )
else
  STAGES=(
    "investigate"
    "plan"
    # "plan"
    "executeverify"
    # "executeverify"
    "replan"
    "executeverify"
    # "executeverify"
    "cleanup"
    "summary"
  )
fi

# Rolling handoff prompt - consolidates all prior work into current summary
generate_handoff_prompt() {
  local stage_name="$1"
  local stage_num="$2"
  cat <<EOF
Save all information from this chat into your plan/notes files, then generate a comprehensive handoff summary.

BEFORE YOU WRITE ANYTHING:
- Examine the handoff directory at /workspace/plan/handoffs/ and read ALL prior stage handoff files (stage_1_handoff.txt, stage_2_handoff.txt, etc.).
- Consolidate the original task, all prior work, and the work completed in this stage.

STRICT FORMAT REQUIREMENTS:
- Use the EXACT section headers below, each on its own line, starting with "## ":
  ## Consolidated Workflow Summary: $stage_name (Stage $stage_num)
  ## Complete Task Context
  ## Current Workflow State
  ## For Next Stage
  ## Instructions
- Do NOT include markdown code fences or extra headings.
- Output as plain text with those header lines (no additional markdown features).
 - Output as plain text with those header lines (no additional markdown features).
$( if [ "${SHORT_WORKFLOW:-}" = "1" ]; then echo "- Keep it concise: target 600 words or less; avoid repeating unchanged context."; fi )

CONTENT GUIDANCE (under the required headers above):
- Complete Task Context: Original task; all work completed across ALL stages; files created/modified/deleted (code + plan/docs); critical decisions; blockers; a timeline across all stages.
- Current Workflow State: Status of the main objective; relevant files/dirs; intermediate results; overall progress.
- For Next Stage: Focus areas; constraints; files/dirs to inspect; all context needed to continue; if complete, state clearly.
- Instructions: This handoff will be the ONLY context for the next stage; include everything critical; prefer actionable and specific content and file paths.

Write a detailed handoff for another engineer to take over.
EOF
}

# Validate that a handoff file contains the required headers.
validate_handoff_file() {
  local file="$1"
  local missing=0
  grep -q '^## Consolidated Workflow Summary' "$file" || missing=1
  grep -q '^## Complete Task Context' "$file" || missing=1
  grep -q '^## Current Workflow State' "$file" || missing=1
  grep -q '^## For Next Stage' "$file" || missing=1
  grep -q '^## Instructions' "$file" || missing=1
  return $missing
}

# Build context prompt from most recent handoff only (rolling summary approach)
build_context_from_handoffs() {
  local current_stage_num="$1"
  local context=""

  # For Stage 1, only provide original task
  if [ "$current_stage_num" -eq 1 ]; then
    if [ -f "$HOST_HANDOFF_DIR/initial_task.txt" ]; then
      context="## Original Task
$(cat "$HOST_HANDOFF_DIR/initial_task.txt")

"
    fi
  else
    # For Stage 2+, only provide the most recent handoff (which contains all consolidated info)
    local most_recent_stage=$((current_stage_num - 1))
    local most_recent_handoff="$HOST_HANDOFF_DIR/stage_${most_recent_stage}_handoff.txt"

    if [ -f "$most_recent_handoff" ]; then
      context="## Previous Stage Summary (All Workflow Context)
$(cat "$most_recent_handoff")

"
    else
      # Fallback to original task if no prior handoff exists
      if [ -f "$HOST_HANDOFF_DIR/initial_task.txt" ]; then
        context="## Original Task
$(cat "$HOST_HANDOFF_DIR/initial_task.txt")

"
      fi
    fi
  fi

  echo "$context"
}

# Common prompt fragments to avoid repetition
DEBUG_HELP="dont hesitate to use standalone/one-off/debugging scripts & add print lines during this task if helpful. test and check all assumptions."
UPDATE_PLAN="update the plan as you go. ensure that the planning/markdown file(s) are always up to date."
USE_AGENTS="use many agents."
PLAN_SUFFIX="$DEBUG_HELP $UPDATE_PLAN $USE_AGENTS"

# Get which iteration of this stage type we're at
get_stage_iteration() {
  local stage_name="$1"
  local current_stage_num="$2"
  local iteration=1

  for ((i=0; i<current_stage_num-1; i++)); do
    if [ "${STAGES[$i]}" = "$stage_name" ]; then
      ((iteration++))
    fi
  done

  echo "$iteration"
}

# Get stage-specific prompt
get_stage_prompt() {
  local stage_name="$1"
  local stage_num="$2"
  local iteration=$(get_stage_iteration "$stage_name" "$stage_num")

  # PRODUCTION STAGES
  case "$stage_name" in
    "investigate") echo "conduct deep and thorough investigations, research, testing, debugging, etc on the task at hand. do not plan/execute yet, just investigate/research. $PLAN_SUFFIX" ;;
    "plan") echo "create/continue to flesh out the plan. ensure that there is defined scope, no ambiguity, and no chance for overly complex solutions or overengineering. do not start executing the plan yet, just plan. $PLAN_SUFFIX" ;;
    "executeverify") echo "review the plan and context to date - figure out if there are remaining tasks left to complete. if there is nothing left to execute then verify everything. if there is nothing left to execute or verify, then just return (do nothing). otherwise, execute all remaining tasks then verify that everything has been completed correctly in accordance with the plan and project principles. $PLAN_SUFFIX" ;;
    "replan") echo "take a moment to take a step back and take in everything in /plan/handoffs/. review all the investigations, planning, execution, verification to date. establish a consolidated plan for moving forward. what has been done, and what needs to be done. if there is nothing left to execute then verify everything. review everything against the original task and requirements. if there is nothing left to execute or verify, then just return (do nothing). otherwise, create a new plan for getting to the finish line from here. $PLAN_SUFFIX" ;;
    "cleanup") echo "conduct a deep and thorough cleanup of the project. remove all files and directories that are no longer needed. dont remove the /plan/handoffs directory." ;;
    "summary") echo "summarize this conversation so far. output the summary here (not into a file). dont remove the /plan/handoffs directory." ;;
  esac

  # # DEBUG STAGES
  # case "$stage_name" in
  #   "test_joke") echo "/joke Create a test file called debug_test.txt with the session ID in it. Output all jokes so far in your context into a file unique to this stage.txt" ;;
  # esac
}

# Stream arbitrary content into a file inside the container without risking
# heredoc delimiter collisions (e.g. when the payload already contains "EOF").
copy_into_container_file() {
  local content="$1"
  local destination="$2"

  {
    printf '%s' "$content"
    printf '\n'
  } | docker exec -i "$CONTAINER_NAME" bash -c "cat > \"$destination\""
}

# Execute a single stage with handoff
execute_stage_with_handoff() {
  local stage_name="$1"
  local stage_num="$2"
  local total_stages="$3"
  local stage_start_time=$(date +%s)

  log_with_timestamp "=================================="
  log_with_timestamp "STAGE $stage_num/$total_stages: $stage_name"
  log_with_timestamp "Session: $SESSION_ID"
  log_with_timestamp "Start time: $(date)"
  log_with_timestamp "=================================="

  update_workflow_status "STAGE_STARTING" "$stage_name" "Stage $stage_num of $total_stages"

  log_with_timestamp "🔍 Building context from previous handoffs..."
  # Build context from previous handoffs
  local context=$(build_context_from_handoffs "$stage_num")
  local context_length=$(echo "$context" | wc -w)
  log_with_timestamp "📝 Context built: $context_length words from previous stages"

  log_with_timestamp "🎯 Generating stage-specific prompt for: $stage_name"
  local stage_prompt=$(get_stage_prompt "$stage_name" "$stage_num")

  # Create full prompt with SLASH COMMAND FIRST, then context
  local full_prompt="$stage_prompt

## Context from Previous Stages
$context"

  local prompt_length=$(echo "$full_prompt" | wc -w)
  log_with_timestamp "📄 Full prompt created: $prompt_length total words"

  # Save prompt to file for debugging
  local prompt_file="$HOST_HANDOFF_DIR/stage_${stage_num}_prompt.txt"
  echo "$full_prompt" > "$prompt_file"
  log_with_timestamp "💾 Prompt saved to: $prompt_file"

  log_with_timestamp "🚀 EXECUTING STAGE $stage_name..."
  update_workflow_status "STAGE_EXECUTING" "$stage_name" "Codex processing stage $stage_num"

  # Send prompt into container temp file
  log_with_timestamp "📤 Sending prompt to Codex container..."
  local prompt_send_start=$(date +%s)
  copy_into_container_file "$full_prompt" "/tmp/stage_prompt.txt"
  local prompt_send_end=$(date +%s)
  local prompt_send_duration=$((prompt_send_end - prompt_send_start))
  log_with_timestamp "⏱️  Prompt transfer took ${prompt_send_duration}s"

  # Run the stage with retry mechanism
  log_with_timestamp "⚡ Codex is processing stage $stage_name..."
  local codex_start_time=$(date +%s)
  retry_codex_operation "Codex stage execution for $stage_name" "docker exec '$CONTAINER_NAME' bash -lc 'cd /workspace && cat /tmp/stage_prompt.txt | codex exec --dangerously-bypass-approvals-and-sandbox --sandbox danger-full-access --skip-git-repo-check --config approval_policy=\"never\" --config sandbox_mode=\"danger-full-access\" --config model=\"gpt-5.2-codex-max\" --config model_reasoning_effort=\"high\"'"
  local stage_exit_code=$?
  local codex_end_time=$(date +%s)
  local codex_duration=$((codex_end_time - codex_start_time))

  if [ $stage_exit_code -ne 0 ]; then
    log_with_timestamp "⚠️  WARNING: Stage $stage_name failed with exit code $stage_exit_code"
    update_workflow_status "STAGE_ERROR" "$stage_name" "Exit code: $stage_exit_code"
  else
    log_with_timestamp "✅ Stage $stage_name completed successfully in ${codex_duration}s"
  fi

  # Generate handoff summary (separate Codex call)
  log_with_timestamp "📋 GENERATING HANDOFF SUMMARY..."
  update_workflow_status "GENERATING_HANDOFF" "$stage_name" "Creating handoff summary"

  local handoff_prompt=$(generate_handoff_prompt "$stage_name" "$stage_num")

  # Time the handoff prompt send
  local handoff_prompt_start=$(date +%s)
  copy_into_container_file "$handoff_prompt" "/tmp/handoff_prompt.txt"
  local handoff_prompt_end=$(date +%s)
  local handoff_prompt_duration=$((handoff_prompt_end - handoff_prompt_start))
  log_with_timestamp "⏱️  Handoff prompt transfer took ${handoff_prompt_duration}s"

  # Capture handoff summary with retry mechanism
  local handoff_file="$HOST_HANDOFF_DIR/stage_${stage_num}_handoff.txt"
  local handoff_start_time=$(date +%s)
  log_with_timestamp "🔄 Requesting handoff summary from Codex..."

  retry_codex_operation "Codex handoff generation for $stage_name" "docker exec '$CONTAINER_NAME' bash -lc 'cd /workspace && cat /tmp/handoff_prompt.txt | codex exec --dangerously-bypass-approvals-and-sandbox --sandbox danger-full-access --skip-git-repo-check --config approval_policy=\"never\" --config sandbox_mode=\"danger-full-access\" --config model=\"gpt-5.2-codex-max\" --config model_reasoning_effort=\"high\"' > '$handoff_file'"
  local handoff_end_time=$(date +%s)
  local handoff_duration=$((handoff_end_time - handoff_start_time))

  # Check handoff quality
  local handoff_words=$(wc -w < "$handoff_file" 2>/dev/null || echo "0")
  log_with_timestamp "📊 Handoff summary: $handoff_words words, generated in ${handoff_duration}s"
  log_with_timestamp "💾 Handoff saved to: $handoff_file"
  # Validate required headers; if missing, re-prompt once with stricter instructions
  if ! validate_handoff_file "$handoff_file"; then
    log_with_timestamp "⚠️  Handoff missing required headers; attempting corrective regeneration..."
    local correction_prompt="The previously generated handoff summary did not include the exact required section headers. Regenerate it now.\n\nREQUIREMENTS (must match exactly):\n## Consolidated Workflow Summary: $stage_name (Stage $stage_num)\n## Complete Task Context\n## Current Workflow State\n## For Next Stage\n## Instructions\n\nRules:\n- No code fences.\n- Use plain text with exactly the headers above and detailed content under each.\n- Before writing, re-examine /workspace/plan/handoffs/ to include ALL prior context and the current stage's results."
    copy_into_container_file "$correction_prompt" "/tmp/handoff_prompt_strict.txt"
    retry_codex_operation "Codex handoff correction for $stage_name" "docker exec '$CONTAINER_NAME' bash -lc 'cd /workspace && cat /tmp/handoff_prompt_strict.txt | codex exec --dangerously-bypass-approvals-and-sandbox --sandbox danger-full-access --skip-git-repo-check --config approval_policy=\"never\" --config sandbox_mode=\"danger-full-access\" --config model=\"gpt-5.2-codex-max\" --config model_reasoning_effort=\"high\"' > '$handoff_file'"
    if validate_handoff_file "$handoff_file"; then
      log_with_timestamp "✅ Corrective regeneration succeeded; required headers present."
    else
      log_with_timestamp "⚠️  Corrective regeneration still missing required headers; proceeding with existing file."
    fi
  fi

  # Clean up temp files
  docker exec "$CONTAINER_NAME" rm -f "/tmp/stage_prompt.txt" "/tmp/handoff_prompt.txt" || true

  # Calculate total stage time
  local stage_end_time=$(date +%s)
  local total_stage_duration=$((stage_end_time - stage_start_time))

  log_with_timestamp "🏁 Stage $stage_name COMPLETE - Total time: ${total_stage_duration}s"
  update_workflow_status "STAGE_COMPLETED" "$stage_name" "Completed in ${total_stage_duration}s"

  # Create stage summary file
  local stage_summary_file="$HOST_HANDOFF_DIR/stage_${stage_num}_summary.txt"
  cat > "$stage_summary_file" << EOF
STAGE SUMMARY: $stage_name (Stage $stage_num/$total_stages)
========================================================
Start Time: $(date -r $stage_start_time)
End Time: $(date -r $stage_end_time)
Total Duration: ${total_stage_duration}s

TIMING BREAKDOWN:
-----------------
Context Building: $((prompt_send_start - stage_start_time))s
Prompt Transfer: ${prompt_send_duration}s
Codex Execution: ${codex_duration}s
Handoff Prompt Transfer: ${handoff_prompt_duration}s
Handoff Generation: ${handoff_duration}s
Cleanup/Other: $((stage_end_time - handoff_end_time))s

PERFORMANCE METRICS:
--------------------
Words per second (Codex): $([ $codex_duration -gt 0 ] && echo "scale=2; $prompt_length / $codex_duration" | bc || echo "N/A")
Words per second (Handoff): $([ $handoff_duration -gt 0 ] && echo "scale=2; $handoff_words / $handoff_duration" | bc || echo "N/A")

DATA SIZES:
-----------
Prompt Length: $prompt_length words
Context Length: $context_length words
Handoff Length: $handoff_words words
Exit Code: $stage_exit_code
Status: $([ $stage_exit_code -eq 0 ] && echo "SUCCESS" || echo "ERROR")

FILES:
------
- $prompt_file
- $handoff_file
- $stage_summary_file
EOF

  log_with_timestamp "📋 Stage summary saved to: $stage_summary_file"
  log_with_timestamp ""

  sleep 2
}

# Save initial task
log_with_timestamp "💾 Saving initial task to: $HOST_HANDOFF_DIR/initial_task.txt"
echo "$INITIAL_TASK" > "$HOST_HANDOFF_DIR/initial_task.txt"
task_words=$(echo "$INITIAL_TASK" | wc -w)
log_with_timestamp "📝 Initial task: $task_words words"

# Container setup with unique naming for multi-project support
PROJECT_NAME=$(basename "$REPO_DIR")
UNIQUE_ID="$(date +%s)_$(hostname)_$$"
CONTAINER_NAME="codex_handoff_${PROJECT_NAME}_${UNIQUE_ID}"
log_with_timestamp "🐳 Container name: $CONTAINER_NAME"

cleanup() {
  log_with_timestamp "🧹 Cleaning up container and finalizing logs..."
  # Preserve WORKFLOW_STATUS=WORKFLOW_COMPLETED; write cleanup details separately
  if [ -n "$HOST_HANDOFF_DIR" ]; then
    echo "CLEANUP_AT=$(date)" > "$HOST_HANDOFF_DIR/workflow_cleanup.txt"
    echo "CONTAINER=$CONTAINER_NAME" >> "$HOST_HANDOFF_DIR/workflow_cleanup.txt"
    log_with_timestamp "🗒️  Cleanup note saved to: $HOST_HANDOFF_DIR/workflow_cleanup.txt"
  fi
  docker rm -f "$CONTAINER_NAME" > /dev/null 2>&1 || true

  # Create final workflow summary
  local workflow_end_time=$(date)
  cat >> "$HOST_HANDOFF_DIR/workflow_final_summary.txt" << EOF
WORKFLOW COMPLETED: $workflow_end_time
==========================================
Session ID: $SESSION_ID
Project: $REPO_DIR
Total Stages: ${#STAGES[@]}
Container: $CONTAINER_NAME
Handoff Directory: $HOST_HANDOFF_DIR

All files in handoff directory:
$(ls -la "$HOST_HANDOFF_DIR" 2>/dev/null | grep -v "^total")
EOF
  log_with_timestamp "📋 Final workflow summary saved to: $HOST_HANDOFF_DIR/workflow_final_summary.txt"
}

trap cleanup EXIT

log_with_timestamp "🐳 Starting Codex container..."
update_workflow_status "CONTAINER_STARTING" "" "Starting Docker container"

CONTAINER_START_TIME=$(date +%s)
docker run -d --name "$CONTAINER_NAME" \
  --mount type=bind,source="$REPO_DIR",target=/workspace \
  --mount type=bind,source="$HOME/.codex",target=/home/dev/.codex \
  $(get_base_docker_env_args) \
  ${HOST_TZ:+--env TZ="$HOST_TZ"} \
  codex_container tail -f /dev/null > /dev/null 2>&1

sleep 2
CONTAINER_END_TIME=$(date +%s)
CONTAINER_STARTUP_DURATION=$((CONTAINER_END_TIME - CONTAINER_START_TIME))
log_with_timestamp "✅ Container started successfully in ${CONTAINER_STARTUP_DURATION}s"
update_workflow_status "CONTAINER_READY" "" "Container ready for stages"

# Execute all stages
log_with_timestamp "🚀 STARTING WORKFLOW EXECUTION"
log_with_timestamp "Total stages to execute: ${#STAGES[@]}"
log_with_timestamp "Stages: ${STAGES[*]}"

TOTAL_STAGES=${#STAGES[@]}
WORKFLOW_START_TIME=$(date +%s)
update_workflow_status "WORKFLOW_EXECUTING" "" "Executing ${TOTAL_STAGES} stages"

for i in "${!STAGES[@]}"; do
  STAGE="${STAGES[$i]}"
  STAGE_NUM=$((i + 1))

  log_with_timestamp ""
  log_with_timestamp "⏭️  Proceeding to stage $STAGE_NUM of $TOTAL_STAGES: $STAGE"
  execute_stage_with_handoff "$STAGE" "$STAGE_NUM" "$TOTAL_STAGES"

  # Show progress
  progress_percent=$(( (STAGE_NUM * 100) / TOTAL_STAGES ))
  log_with_timestamp "📊 Progress: $STAGE_NUM/$TOTAL_STAGES stages complete ($progress_percent%)"
done

# Final workflow completion
WORKFLOW_END_TIME=$(date +%s)
TOTAL_WORKFLOW_DURATION=$((WORKFLOW_END_TIME - WORKFLOW_START_TIME))
WORKFLOW_DURATION_MINUTES=$((TOTAL_WORKFLOW_DURATION / 60))
WORKFLOW_DURATION_SECONDS=$((TOTAL_WORKFLOW_DURATION % 60))

log_with_timestamp "🎉 =================================="
log_with_timestamp "🎉 HANDOFF WORKFLOW COMPLETE!"
log_with_timestamp "🎉 =================================="
log_with_timestamp "📊 Total execution time: ${WORKFLOW_DURATION_MINUTES}m ${WORKFLOW_DURATION_SECONDS}s"
log_with_timestamp "📁 All handoff summaries saved in: $HOST_HANDOFF_DIR"
log_with_timestamp "🆔 Session ID: $SESSION_ID"
log_with_timestamp "📋 Check workflow_status.txt for current status"
log_with_timestamp "📜 Check workflow_log.txt for detailed logs"

update_workflow_status "WORKFLOW_COMPLETED" "" "All ${TOTAL_STAGES} stages completed in ${WORKFLOW_DURATION_MINUTES}m ${WORKFLOW_DURATION_SECONDS}s"

# Create performance analysis file
PERFORMANCE_FILE="$HOST_HANDOFF_DIR/performance_analysis.txt"
cat > "$PERFORMANCE_FILE" << EOF
WORKFLOW PERFORMANCE ANALYSIS
==============================
Session ID: $SESSION_ID
Total Stages: $TOTAL_STAGES
Total Duration: ${WORKFLOW_DURATION_MINUTES}m ${WORKFLOW_DURATION_SECONDS}s
Container Startup: ${CONTAINER_STARTUP_DURATION}s

STAGE PERFORMANCE SUMMARY:
--------------------------
EOF

# Append stage timing data
for i in "${!STAGES[@]}"; do
  STAGE_NUM=$((i + 1))
  SUMMARY_FILE="$HOST_HANDOFF_DIR/stage_${STAGE_NUM}_summary.txt"
  if [ -f "$SUMMARY_FILE" ]; then
    echo "" >> "$PERFORMANCE_FILE"
    echo "Stage $STAGE_NUM (${STAGES[$i]}):" >> "$PERFORMANCE_FILE"
    grep -A 6 "TIMING BREAKDOWN" "$SUMMARY_FILE" | tail -n 6 >> "$PERFORMANCE_FILE" || true
  fi
done

log_with_timestamp "📊 Performance analysis saved to: $PERFORMANCE_FILE"

# List all generated files for easy reference
log_with_timestamp ""
log_with_timestamp "📂 FILES GENERATED:"
ls -la "$HOST_HANDOFF_DIR" | while read line; do
  if [[ "$line" != "total "* ]]; then
    log_with_timestamp "   $line"
  fi
done
