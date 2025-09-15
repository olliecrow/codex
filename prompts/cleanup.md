# CLEANUP MODE

**AVAILABLE AGENTS**: The following agents are available for use via the Task tool. You are encouraged to use MULTIPLE COPIES of the same agent type when applicable and helpful for comprehensive coverage:

**ALL AVAILABLE AGENTS**:
- general-purpose: General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks
- statusline-setup: Use this agent to configure the user's Claude Code status line setting
- output-mode-setup: Use this agent to create a Claude Code output mode
- assumption-checker: Analysis agent that verifies system invariants and assumptions are maintained
- large-file-reader: Analysis agent that processes large files exceeding context windows with lossless information preservation
- performance-profiler: Analysis agent that profiles performance bottlenecks and inefficiencies
- ai-research-scientist: Research agent specializing in AI/ML academic papers and cutting-edge research
- execution-orchestrator: Master orchestration agent that coordinates all other agents for complex tasks
- software-engineer: Implementation agent that writes production-ready code with high quality standards
- test-guardian: Validation agent that runs existing tests and reports results
- ai-engineer: Implementation agent that transforms AI/ML research into production systems
- documentation-finder: Research agent that locates and catalogs all relevant documentation
- empirical-validator: Validation agent that tests assumptions through empirical experiments
- simplicity-advocate: Analysis agent that reviews code for over-engineering and complexity
- cleanup-specialist: Implementation agent that removes temporary files and development artifacts
- edge-case-finder: Analysis agent that identifies untested edge cases and corner cases
- online-researcher: Research agent that searches extensively across the internet for information
- planning-architect: Planning agent that creates comprehensive task plans and manages execution strategy
- code-reviewer: Analysis agent that synthesizes findings from multiple agents into comprehensive reviews

**IMPORTANT**: You can and should use multiple copies of the same agent type when it will provide better coverage or parallel processing of different aspects of the task.

## Agent Strategy

This command specializes in methodical cleanup of temporary files, build artifacts, and session-specific files.

## Agent Discovery for Safe Cleanup

### **AGENT SELECTION FROM AVAILABLE LIST**
Select agents from the explicit list of available agents above based on cleanup requirements. You can use multiple copies of the same agent type when beneficial for comprehensive analysis or parallel processing of different cleanup aspects.

### **Agent Selection Strategy for Cleanup**
1. **Select from available agents list** based on specific cleanup requirements
2. **Map cleanup requirements** to available agent capabilities from the explicit list above
3. **Select multiple complementary agents** for comprehensive cleanup coverage
4. **Use multiple copies of same agent types** when beneficial for parallel analysis of different cleanup aspects
5. **ALWAYS prefer using more agents over fewer** when they can work independently
6. **Launch ALL selected agents in parallel** using multiple Task tool invocations in ONE message

### **Parallel Cleanup Agent Deployment Imperative**
Using the explicit list of available agents above:
- **NEVER use just one agent** when multiple can contribute to safe cleanup
- **ALWAYS launch multiple agents simultaneously** in a single message for cleanup tasks
- **USE MULTIPLE COPIES**: Deploy multiple copies of the same agent type when helpful for parallel cleanup analysis
- **THINK ECOSYSTEM**: Consider agents across ALL available categories for holistic cleanup
- **MAXIMIZE PARALLEL EXECUTION**: If 6+ agents can work independently on cleanup aspects, launch ALL 6+ together

**CRITICAL**: Maximum parallelism is essential - spawn all independent agents at once rather than sequentially. Use multiple copies of the same agent type when beneficial.

### **Available Cleanup Agent Categories**
From the explicit list above, select agents from these categories for cleanup needs:
- **Cleanup & Maintenance**: cleanup-specialist, general-purpose
- **Testing & Validation**: test-guardian, empirical-validator
- **Analysis & Safety**: assumption-checker, performance-profiler, edge-case-finder
- **Review**: code-reviewer, simplicity-advocate
- **Verification**: empirical-validator, test-guardian, assumption-checker
- **Orchestration**: execution-orchestrator, planning-architect

## Cleanup Collaboration Excellence

### Safe Cleanup Through Collaboration
I ensure cleanup safety by consulting with other agents to validate file dependencies, confirm deletion safety, and preserve critical artifacts.

### When I Collaborate on Cleanup

I seek cleanup validation when:
- Identifying safe-to-delete artifacts
- Confirming files aren't actively used
- Validating cleanup won't break functionality
- Assessing impact on other agents' work
- Determining what should be preserved
- Clarifying user preferences on retention

### My Cleanup Collaboration Patterns

**Safety Validation Pattern**:
```
Task: assumption-checker → "Safe to delete these files?"
Task: test-guardian → "Will cleanup affect tests?"
Task: planning-architect → "Are these planning artifacts still needed?"
[Parallel safety checks before deletion]
```

**Scope Confirmation Pattern**:
```
Task: software-engineer → "Any runtime dependencies here?"
Task: verification-specialist → "Should we preserve for audit?"
User → "Should any of these be kept for review?"
[Comprehensive scope validation]
```

### Cleanup Context Sharing

When requesting cleanup validation, I provide:
- **File List**: Complete inventory of deletion candidates
- **File Origins**: How/when files were created
- **Size Impact**: Storage to be recovered
- **Risk Assessment**: Potential deletion impacts
- **Preservation Rationale**: Why certain files are kept

### User Cleanup Preferences

I clarify with users:
- "Should I preserve any artifacts for review?"
- "What's your preference on log retention?"
- "Should debug files be kept for troubleshooting?"
- "Any specific files you want preserved?"
- "How aggressive should cleanup be?"

### Collaboration Anti-Patterns to Avoid

❌ **Sequential Consultation**: Never ask agents one-by-one when parallel is possible
❌ **Context-Free Questions**: Always provide complete background
❌ **Late Validation**: Consult early, not after implementation
❌ **Assumption Making**: Always clarify ambiguity with users
❌ **Isolation Working**: Don't hesitate to seek peer perspectives
❌ **Generic Questions**: Be specific about what help you need

### Collaboration Best Practices

✅ **Parallel First**: Launch all independent consultations simultaneously
✅ **Context Rich**: Provide complete problem background
✅ **Early Engagement**: Seek input during planning, not after
✅ **User Partnership**: Proactively clarify requirements
✅ **Specific Needs**: Be precise about required assistance
✅ **Synthesis Focus**: Combine perspectives holistically

## Agent Instruction Template

When spawning cleanup-related agents, ALWAYS include in their instructions:
- "Use `/plan` directory for ALL cleanup analysis files, investigation reports, and verification artifacts - this is Claude Code's workspace, NOT for user files"
- "Create any cleanup analysis markdown files in `/plan` directory (Claude Code's workspace)"
- "Do not modify user project files during cleanup analysis - focus on safe deletion candidates"
- "The `/plan` directory is Claude Code's designated workspace for cleanup analysis - user files remain in main workspace"
- "NEVER put user files or user-requested project modifications in `/plan` - only Claude Code's cleanup analysis goes there"

## CRITICAL: The /plan Directory Rule

**CLAUDE CODE'S WORKSPACE ORGANIZATION**:
- **THE `/plan` DIRECTORY IS CLAUDE CODE'S WORKSPACE** - it is specifically for files that Claude Code creates during task execution and investigations
- **NOT FOR USER FILES**: The `/plan` directory is NOT for user files, project files, or files the user creates - those remain in the main workspace
- **CLAUDE CODE'S FILES ONLY**: ALL temporary files, markdown files (unless explicitly requested by user), artifacts, test scripts, reports, investigation files, analysis documents, or any files that Claude Code generates MUST be created inside the `/plan` directory at the root of the workspace
- **CLAUDE CODE'S SCRATCH SPACE**: The `/plan` directory is Claude Code's designated scratch space for all temporary work, thinking files, and task execution artifacts
- **CLAUDE CODE'S WORKSPACE MEMORY**: This directory serves as Claude Code's workspace memory and contains valuable project tracking from Claude Code's operations
- This directory will never be committed to the GitHub repo
- It should be created if it doesn't exist
- **USER PROJECT FILES**: User files and project files remain in the main workspace directory structure outside of `/plan`

**CRITICAL CLEANUP RULE**: The `/plan` directory and its contents must NEVER be deleted during cleanup operations - it contains valuable project memory and work tracking from Claude Code's task execution.

## Core Principles

**Simplicity First**: Avoid over-engineering cleanup strategies. Focus on straightforward, effective cleanup that gets the job done.

**Empirical Validation**: Validate cleanup safety through multiple methods. Test that cleanup doesn't break functionality empirically.

**Question Everything**: Ask clarifying questions when cleanup scope is ambiguous. Questions are highly encouraged for safe cleanup.

**No Artificial Work**: If workspace is already clean, say so. Don't create cleanup tasks where none exist.

**Test-Driven Awareness**: Cleanup should never break tests. Always verify test integrity before and after cleanup.

approach cleanup methodically and cautiously:

1. first, investigate files and folders created during the current conversation:
   - review all files modified or created in this session
   - identify temporary test files, debug outputs, or exploratory code OUTSIDE of `/plan` (which is Claude Code's workspace)
   - check for empty files and directories that serve no purpose (except `/plan` which is Claude Code's workspace)
   - look for one-off scripts or test data created for validation outside of `/plan`
   - examine any reports or logs generated during the conversation outside of `/plan`
   - identify failed attempts or backup files from edits outside of `/plan`
   - **NOTE**: Files in `/plan` are Claude Code's intentional workspace files created during task execution and investigations and should be preserved

2. identify common temporary and build artifacts (but NOT runtime dependencies):
   - build directories: build/, dist/, out/, target/, .next/, .nuxt/, .vite/ (only if not needed for running)
   - cache directories: .cache/, node_modules/.cache/, __pycache__/, .pytest_cache/, .mypy_cache/
   - coverage reports: coverage/, .coverage, htmlcov/, lcov-report/
   - temporary files: *.tmp, *.temp, *.log, *.swp, .DS_Store, Thumbs.db
   - test outputs: test-results/, test-reports/, junit.xml
   - compiled files: *.pyc, *.pyo (but NOT compiled binaries needed for execution)
   - package manager artifacts: NEVER delete node_modules/, vendor/, or similar dependency directories
   - IDE files: .idea/, .vscode/ (unless they contain shared project settings)
   - environment files: venv/, env/ (only if confirmed not in use), .env.local (preserve if contains config)

3. identify project-specific temporary files OUTSIDE of `/plan` (Claude Code's workspace):
   - random markdown reports or notes that were generated during debugging (should have been in Claude Code's `/plan` workspace)
   - temporary test files created during development (should have been in Claude Code's `/plan` workspace)
   - backup files: *.bak, *.backup, *~ (outside of Claude Code's `/plan` workspace)
   - debug output files (outside of Claude Code's `/plan` workspace)
   - temporary data files or databases used for testing (outside of Claude Code's `/plan` workspace)
   - screenshots or images from test runs (outside of Claude Code's `/plan` workspace)
   - profiling data and performance reports (outside of Claude Code's `/plan` workspace)
   - **IMPORTANT**: If any of these are found outside Claude Code's `/plan` workspace, they are cleanup candidates

4. before deleting, always:
   - list all files that will be deleted
   - group them by category (build artifacts, caches, temporary files, etc.)
   - show file sizes to indicate impact
   - ask for confirmation on anything that seems important or unclear
   - preserve files that might contain valuable configuration or documentation
   - verify that files are not needed to run the current implementation

5. never delete without checking:
   - source code files
   - configuration files (unless clearly temporary)
   - documentation (unless clearly temporary/draft)
   - test files (the actual test code)
   - data files that might be needed
   - any files mentioned in .gitignore that might be intentionally preserved locally
   - **THE /plan DIRECTORY AND ALL ITS CONTENTS (Claude Code's critical workspace memory for task execution and investigations - NEVER DELETE)**
   - dependencies required to run the code (node_modules/, vendor/, pip packages, etc.)
   - compiled output that is actually used for execution (dist/ if it's the entry point)
   - environment configuration files (.env, .env.local, etc.) that contain active settings

6. be conservative when uncertain:
   - if a file's purpose is unclear, ask before deleting
   - if a directory contains mixed content, be selective
   - consider the file's age - very recent files might still be in use
   - check if files are referenced in code or configuration

7. handle empty files and directories:
   - identify empty files that serve no purpose
   - find empty directories (excluding intentional placeholder dirs)
   - remove empty files/dirs unless they're required by the project structure
   - preserve empty __init__.py files in Python projects
   - keep .gitkeep or .keep files that maintain directory structure in git

8. provide clear reporting in the conversation (not to disk):
   - show what was deleted and total space freed
   - list what was skipped and why
   - note any files that need manual review

## Comprehensive Cleanup Documentation Strategy

### CRITICAL: Prefer Long Single Markdown Files IN /plan (Claude Code's Workspace)
**FUNDAMENTAL PRINCIPLE**: Use comprehensive, single markdown files for cleanup documentation IN CLAUDE CODE'S `/plan` WORKSPACE:
- **Complete cleanup history**: Document all cleanup decisions and rationale in ONE file in Claude Code's `/plan` workspace
- **Context for decisions**: Keep records of why certain files were preserved or deleted in Claude Code's workspace
- **Investigation trail**: Document the analysis process that led to cleanup decisions in Claude Code's workspace
- **Future reference**: Comprehensive cleanup logs help understand past decisions from Claude Code's task execution
- **LOCATION**: ALL cleanup documentation created by Claude Code MUST be created in Claude Code's `/plan` workspace directory

### Claude Code's Cleanup Documentation Workspace
- **ONE FILE RULE**: Maintain ONE comprehensive markdown file for cleanup documentation in Claude Code's `/plan` workspace
- **DECISION LOGGING**: Record every cleanup decision with reasoning in Claude Code's `/plan` workspace
- **NAMING**: Use descriptive names like `/plan/comprehensive_cleanup_log.md` in Claude Code's workspace
- **PRESERVE RATIONALE**: Document why files were kept or removed in Claude Code's workspace
- **SELECTIVE PRESERVATION**: Claude Code's `/plan` directory serves as permanent workspace memory for Claude Code's task execution

### Strict No-Report Policy (Outside of Claude Code's /plan Workspace)
- **NEVER** create cleanup report files, summary files, or documentation files for the user OUTSIDE of Claude Code's `/plan` workspace
- **NEVER** leave markdown files in the repository root or source directories that could be committed
- **ALWAYS** use Claude Code's `/plan` workspace directory for any markdown files, reports, or documentation during Claude Code's task execution
- **EXCEPTION**: Only create persistent files OUTSIDE Claude Code's `/plan` workspace when explicitly requested with phrases like "create a cleanup report file" or "save the cleanup results to a file"
- **OUTPUT**: Present all cleanup findings and results directly in the conversation
- **CLAUDE CODE'S WORKSPACE**: Use Claude Code's `/plan` workspace for all working documents and temporary files that Claude Code creates

### Cleanup Requirements
- **TRACK**: Maintain awareness of every file Claude Code creates during cleanup analysis
- **USE CLAUDE CODE'S /plan**: Create all temporary analysis files that Claude Code generates in Claude Code's `/plan` workspace directory
- **PRESERVE CLAUDE CODE'S /plan**: NEVER delete Claude Code's `/plan` workspace directory or its contents during cleanup
- **CLEAN OUTSIDE**: Focus cleanup on files outside Claude Code's `/plan` workspace that shouldn't be committed
- **VERIFY**: Use LS to confirm no artifacts remain outside Claude Code's `/plan` workspace from the cleanup process

do not interact with git! do not use the git command, even readonly operations.

always err on the side of caution - it's better to leave a file than delete something important.

## Agent Instruction Template

When spawning cleanup-related agents, ALWAYS include in their instructions:
- "Use `/plan` directory for ALL cleanup analysis files and investigation reports - this is Claude Code's workspace, NOT for user files"
- "Create any cleanup documentation in `/plan` directory (Claude Code's workspace)"
- "Do not delete user project files - focus cleanup on appropriate temporary files and Claude Code's artifacts in `/plan`"
- "The `/plan` directory is Claude Code's designated workspace - cleanup should organize it but never delete the directory itself"
- "NEVER delete user files or user-requested project files - only clean up actual temporary artifacts"

if the cleanup seems too aggressive or might delete important files, stop and ask for clarification.

## Task Completion

After completing any cleanup task:
1. **Review cleanup scope**: Document what files/directories were cleaned (distinguish between user project files and Claude Code files in `/plan`)
2. **Validate project integrity**: Ensure core functionality remains intact through empirical testing
3. **Clean up cleanup artifacts**: Remove any Claude Code temporary analysis files from `/plan` used during cleanup process
4. **Report actual impact**: Only report what was actually cleaned, don't manufacture results
5. **Preserve /plan workspace**: Ensure Claude Code's `/plan` directory structure remains for future use
6. **Verify no over-cleanup**: Confirm no important files were accidentally removed
7. **Confirm user files safe**: Verify user project files remain properly organized and untouched

validation: after cleanup, ensure the project still works by checking that key files and directories remain intact.

## Enhanced Cleanup Awareness

This command represents the pinnacle of cleanup awareness and methodical execution:

### Pre-Cleanup Assessment
- **Session-specific tracking**: Identify exactly what files and directories were created during the current conversation OUTSIDE of Claude Code's `/plan` workspace
- **Context-aware analysis**: Understand the purpose and origin of each potential cleanup target
- **Dependency mapping**: Recognize files that might be interconnected or serve ongoing purposes
- **Claude Code's workspace preservation**: Ensure Claude Code's `/plan` workspace directory and its contents are never targeted for cleanup

### Methodical Cleanup Execution
- **Targeted cleanup approach**: Base cleanup decisions on actual session activities and file creation patterns
- **Layered validation**: Use multiple verification methods to ensure cleanup safety
- **Progressive cleanup**: Clean in stages, validating after each stage

### Agent Orchestration for Safe Cleanup

**ALWAYS deploy multiple agents in parallel** - Launch all independent agents simultaneously:
- **Primary cleanup agents + Verification agents + Analysis agents**: All launched in the SAME message with multiple Task tool invocations
- **Batch all independent operations**: Never wait for one agent to complete before launching another if they don't depend on each other
- **Example**: Launch cleanup-specialist, assumption-checker, and test-guardian agents ALL AT ONCE in a single message
- **Agent workspace**: All agents should use Claude Code's `/plan` workspace directory for their temporary files and reports that they create during task execution

### Post-Cleanup Validation

After cleanup operations:
1. **Comprehensive verification**: Ensure core functionality remains intact
2. **Report cleanup impact**: Document what was cleaned and space freed (report in conversation, log in Claude Code's `/plan` workspace if needed)
3. **Record preservation decisions**: Note what was intentionally preserved and why (especially Claude Code's `/plan` workspace directory)
4. **Validate system integrity**: Confirm no critical dependencies were affected
5. **Verify Claude Code's /plan intact**: Confirm Claude Code's `/plan` workspace directory and its contents remain untouched

$ARGUMENTS