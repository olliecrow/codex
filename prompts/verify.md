# VERIFY MODE

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

## CRITICAL RULE: /plan Directory - CLAUDE CODE'S WORKSPACE ONLY

**MANDATORY**: The `/plan` directory is EXCLUSIVELY Claude Code's workspace for verification and analysis activities. This is NOT for user files or project files.

**CLAUDE CODE'S `/plan` DIRECTORY**:
- **CLAUDE CODE'S WORKSPACE**: This is where Claude Code creates files during verification, analysis, and investigation work
- **NOT FOR USER FILES**: User project files and actual application code remain in the main workspace directory structure
- **VERIFICATION DOCUMENTATION**: All Claude Code's verification reports, analysis documents, test results, and investigation findings go here
- **ANALYSIS WORKSPACE**: When Claude Code performs code analysis, creates temporary test scripts, or generates investigation reports, these go in `/plan`
- **NEVER COMMITTED**: Will never be committed to the GitHub repo - this is Claude Code's temporary workspace
- **AUTO-CREATED**: Should be created by Claude Code if it doesn't exist using `mkdir -p /plan`
- **CLEANUP TARGET**: Claude Code should clean up specific files from `/plan` after verification tasks complete

**CLEAR DISTINCTION**: 
- `/plan/` = Claude Code's verification and analysis workspace
- `/workspace/` (main) = User's project files and actual codebase

## Agent Strategy

This command specializes in comprehensive verification and validation of work completed during the current conversation.

## Agent Discovery for Comprehensive Verification

### **AGENT SELECTION FROM AVAILABLE LIST**
Select agents from the explicit list of available agents above based on verification requirements. You can use multiple copies of the same agent type when beneficial for comprehensive analysis or parallel processing of different verification aspects.

### **Agent Selection Strategy for Verification**
1. **Select from available agents list** based on specific verification requirements
2. **Map verification requirements** to available agent capabilities from the explicit list above
3. **Select multiple complementary agents** for comprehensive verification coverage
4. **Use multiple copies of same agent types** when beneficial for parallel analysis of different verification aspects
5. **ALWAYS prefer using more agents over fewer** when they can work independently
6. **Launch ALL selected agents in parallel** using multiple Task tool invocations in ONE message

### **Parallel Verification Agent Deployment Imperative**
Using the explicit list of available agents above:
- **NEVER use just one agent** when multiple can contribute to verification excellence
- **ALWAYS launch multiple agents simultaneously** in a single message for verification tasks
- **USE MULTIPLE COPIES**: Deploy multiple copies of the same agent type when helpful for parallel verification analysis
- **THINK ECOSYSTEM**: Consider agents across ALL available categories for holistic verification
- **MAXIMIZE PARALLEL EXECUTION**: If 8+ agents can work independently on verification aspects, launch ALL 8+ together

**PARALLELISM IS CRITICAL**: Never launch verification agents one-by-one. ALWAYS batch multiple Task tool calls in ONE message. Use multiple copies of the same agent type when beneficial.

### **Available Verification Agent Categories**
From the explicit list above, select agents from these categories for verification needs:
- **Quality Assurance**: assumption-checker, edge-case-finder, code-reviewer, simplicity-advocate
- **Testing & Validation**: test-guardian, empirical-validator
- **Technical Review**: code-reviewer, software-engineer, ai-engineer, performance-profiler
- **Analysis & Investigation**: large-file-reader, performance-profiler, assumption-checker
- **Research & Documentation**: documentation-finder, online-researcher, ai-research-scientist
- **Orchestration**: execution-orchestrator, planning-architect
- **Maintenance**: cleanup-specialist, general-purpose

## Agent Instruction Template

When spawning verification agents, ALWAYS include in their instructions:
- "Use `/plan` directory for ALL verification analysis files, reports, and investigation artifacts - this is Claude Code's workspace, NOT for user files"
- "Create any verification documentation in `/plan` directory (Claude Code's workspace)"
- "Do not modify user project files during verification - only analyze and report"
- "The `/plan` directory is Claude Code's designated workspace for verification work - user files remain in main workspace"
- "NEVER put user files or user-requested project modifications in `/plan` - only Claude Code's verification analysis goes there"

**REMEMBER**: If 5 verification agents can work independently, launch ALL 5 in ONE message!

## Verification Collaboration Excellence

### Multi-Angle Verification Through Collaboration
I ensure thorough verification by consulting multiple agents for diverse perspectives, validating against original requirements, and confirming all quality gates are met.

### When I Collaborate on Verification

I engage other agents when:
- Verifying complex implementations against requirements
- Validating performance meets expectations
- Confirming security requirements are satisfied
- Assessing code quality and maintainability
- Checking test coverage completeness
- Reviewing architectural decisions

### My Verification Collaboration Patterns

**Comprehensive Verification Pattern**:
```
Task: planning-architect → "Does implementation match original plan?"
Task: test-guardian → "Are all tests passing?"
Task: performance-profiler → "Are performance targets met?"
Task: assumption-checker → "Were all assumptions validated?"
[All run in parallel for thorough verification]
```

**Quality Gate Pattern**:
```
Task: simplicity-advocate → "Is solution appropriately simple?"
Task: software-engineer → "Does code follow best practices?"
Task: security-specialist → "Are security requirements met?"
[Simultaneous quality validation]
```

### Verification Context Provision

When requesting verification assistance, I share:
- **Original Requirements**: What was requested
- **Implementation Details**: What was built
- **Change Scope**: What was modified
- **Test Results**: Current test status
- **Known Issues**: Any identified problems

### User Verification Engagement

I confirm with users:
- "Does the implementation meet your expectations?"
- "Are there aspects requiring additional verification?"
- "What's your confidence threshold for deployment?"
- "Should we perform additional validation?"
- "Are all acceptance criteria satisfied?"

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

## Verification Awareness and Artifact Management

**Critical**: This command emphasizes meticulous verification tracking and cleanup awareness:

### Verification Scope Tracking
- **Conversation analysis**: Systematically review everything accomplished in the current conversation
- **Change impact assessment**: Identify all files, configurations, and systems potentially affected by conversation activities
- **Original objective alignment**: Compare outcomes against initial intentions, targets, goals, and constraints
- **Quality metric evaluation**: Assess work against established requirements and guidelines
- **Claude Code's /plan workspace usage**: Ensure all Claude Code's verification work happens within `/plan` directory (user files remain in main workspace)

### Intelligent Verification Cleanup
- **Claude Code's verification artifact management**: Track all temporary files, test outputs, and analysis results that Claude Code creates during verification in `/plan`
- **Context-specific cleanup**: Remove Claude Code's verification artifacts from `/plan` based on actual verification activities performed
- **Preserve Claude Code's /plan directory**: The `/plan` directory itself should remain as Claude Code's workspace for future use
- **Post-verification cleanup**: Ensure Claude Code's verification process leaves no artifacts outside `/plan` directory (user files remain untouched in main workspace)

## Core Principles

**Simplicity First**: Avoid over-engineering verification processes. Focus on straightforward, effective validation that ensures quality.

**Empirical Validation**: Verify through multiple empirical methods. Test actual functionality, not just theoretical correctness. Validate assumptions through real testing.

**Question Everything**: Ask clarifying questions when verification scope is ambiguous. Challenge assumptions and verify they hold true.

**No Artificial Work**: If implementation is correct and complete, say so. Don't manufacture verification issues where none exist.

**Test-Driven Awareness**: Tests are the foundation of verification. Always run full test suites and compare against baselines.

## Ultra-Thinking Mode for Verification

For complex verification tasks, enable ultra-thinking mode:
- Think comprehensively about all aspects that need verification
- Take a holistic, bird's-eye view of the entire implementation
- Use comprehensive agent orchestration for thorough analysis
- Validate through multiple empirical methods and test approaches
- Take as much time as needed for complete verification

verify the output/work from the current conversation.

be highly critical and objective.

take a holistic view.

look back to see what the original intentions/targets/goals/objectives were, including constraints/requirements/guidelines.

critically review everything in this conversation so far.

use ultrathinking mode for this task.

think long and hard.

## Strategic Verification Orchestration

**CRITICAL**: Deploy the Task tool with MAXIMUM PARALLELISM for comprehensive verification:

**NEVER DO THIS** (Sequential - WRONG):
1. Launch agent 1, wait for completion
2. Launch agent 2, wait for completion
3. Launch agent 3, wait for completion

**ALWAYS DO THIS** (Parallel - CORRECT):
Single message with:
- Task 1: agent 1
- Task 2: agent 2  
- Task 3: agent 3
All launched SIMULTANEOUSLY!

### Orchestrated Verification Approach
**LAUNCH ALL orchestration agents AT ONCE** in a single message to coordinate comprehensive verification based on the specific changes and work completed.

### Parallel Analysis Phase
**MANDATORY: Deploy ALL analysis agents SIMULTANEOUSLY** in ONE message with multiple Task invocations:
- Task 1: code-reviewer (comprehensive review)
- Task 2: edge-case-finder (untested scenarios)
- Task 3: performance-profiler (performance impacts)
- Task 4: assumption-checker (system invariants)
ALL launched TOGETHER, never sequentially!

### Concurrent Validation Phase  
**Launch ALL validation agents IN PARALLEL** - Single message with multiple Task calls to ensure tests pass and behaviors remain intact.

### Verification Cleanup Phase
**Deploy ALL cleanup specialists AT ONCE** if multiple cleanup tasks exist. Maximum parallelism ensures efficient cleanup.

## Verification-Specific Cleanup Integration

Integrate cleanup specialists into the verification workflow to identify and remove all temporary artifacts created during verification activities within `/plan`, including test outputs, debug files, and analysis results. Ensure confirmation of cleanup scope before deletion and provide comprehensive cleanup summary in the conversation only.

**IMPORTANT**: All Claude Code's verification artifacts should be contained within `/plan` directory. Cleanup should:
- Remove specific verification files that Claude Code created from `/plan` after use
- Preserve the `/plan` directory structure itself as Claude Code's workspace
- Never delete user files outside `/plan` - only remove Claude Code's temporary project-related files if explicitly created during verification
- **USER FILES REMAIN SAFE**: Never touch user project files in the main workspace during cleanup

Cleanup operations remain git-aware without directly interacting with git commands or gitignore modifications.

do not interact with git! do not use the git command, even readonly operations.

validation and re-validate to be sure that.

take as long as you need, there is no rush.

## Task Completion

After completing verification:
1. **Review verification scope**: Document what was analyzed and verified (distinguish between user project files and Claude Code analysis in `/plan`)
2. **Validate empirically**: Confirm findings through actual testing and measurement, not just theoretical analysis
3. **Clean up verification artifacts**: Remove Claude Code's temporary analysis files from `/plan` used during verification
4. **Report actual findings**: Only report real issues found, don't manufacture problems where none exist
5. **Preserve /plan workspace**: Keep Claude Code's `/plan` directory structure for future verification work
6. **Confirm completeness**: Verify all original objectives were addressed without artificial additions
7. **Validate user files integrity**: Ensure user project files remain unmodified and properly organized

you should return with a concise verification report in the conversation only (not saved to disk).

if there is nothing to do, then just say so. dont make up work where there isnt any to do.

if there are no issues, then just say so. dont make up issues when there arent any.

ensure that care is always placed into ensuring that associated code is considered during planning, and during the execution of any task.

always ask clarifying questions if something is ambiguous or not 100% clear to you. questions are highly encouraged.

## Initial Setup: /plan Directory

**FIRST STEP**: Before any verification work begins:
1. Check if Claude Code's `/plan` directory exists at workspace root
2. Create Claude Code's `/plan` workspace if it doesn't exist using `mkdir -p /plan`
3. Use `/plan` as Claude Code's exclusive workspace for all verification activities (user project files stay in main workspace)
4. Never commit or push Claude Code's `/plan` directory to version control
5. **REMEMBER**: `/plan` is for Claude Code's work, user files remain in their original locations

## Comprehensive Verification Documentation Strategy

### CRITICAL: Long Single Markdown Files for Verification
**CORE PRINCIPLE**: Always use comprehensive, single markdown files for verification:
- **Complete verification trail**: Document all checks, validations, and findings in ONE file
- **Historical context**: Previous verification attempts provide crucial insights
- **Issue tracking**: Keep all discovered issues and resolutions in one place
- **Unified verification narrative**: Single file tells the complete verification story

### Claude Code's Verification Documentation Workspace
- **LOCATION**: ALL Claude Code's verification documentation MUST be created in `/plan` directory (user documentation stays in main workspace)
- **ONE FILE APPROACH**: Create ONE comprehensive markdown file in Claude Code's `/plan` workspace for ALL verification work
- **CONTINUOUS DOCUMENTATION**: Append each verification step and finding to Claude Code's files in `/plan`
- **NAMING**: Use descriptive names like `/plan/claude_verification_journal.md` or `/plan/claude_analysis_report.md`
- **ACCUMULATE FINDINGS**: Build upon previous verification attempts within Claude Code's `/plan` workspace
- **PRESERVE CONTEXT**: Keep Claude Code's verification documentation in `/plan` as valuable reference (not committed to repo)
- **USER FILES UNTOUCHED**: User project documentation and files remain in their original workspace locations

### Strict No-Report Policy for Claude Code
- **NEVER** create Claude Code's verification report files outside `/plan` directory
- **NEVER** leave Claude Code's verification markdown files in the repository root that could be committed
- **ALWAYS** use Claude Code's `/plan` directory for any verification documentation or analysis files
- **EXCEPTION**: Only create persistent files outside Claude Code's `/plan` workspace when explicitly requested with phrases like "create a verification report file"
- **OUTPUT**: Present all verification findings and results directly in the conversation
- **USER PROJECT INTEGRITY**: Never create Claude Code's temporary files in user project directories

### Claude Code's Verification Cleanup Requirements
- **TRACK**: Maintain awareness of every file Claude Code creates during verification in `/plan`
- **IMMEDIATE**: Delete specific verification artifacts from Claude Code's `/plan` workspace as soon as they serve their purpose
- **ANALYSIS FILES**: Remove all temporary analysis and review files that Claude Code created from `/plan`
- **PRESERVE**: Keep Claude Code's `/plan` directory itself for future verification use
- **FINAL**: Before task completion, verify no Claude Code temporary files exist outside `/plan`
- **VERIFY**: Use LS to confirm no Claude Code verification artifacts remain outside `/plan` directory
- **USER FILES PROTECTED**: Never delete or modify user project files during cleanup - only Claude Code's temporary files in `/plan`

dont provide a report or similar to disk unless explicitly asked to do so.

tests are the bedrock of any project. prior to making any changes, ensure that you run all of the tests across the whole project first to establish a baseline - make note of all of the passes and fails. ensure that you remember these results. after having completed any changes on disk, be sure to re-run all of the tests across the whole project. compare to the baseline taken previously. if there are more failures than before, then this is an issue as the changes have broken some tests. you need to dig into the reasons for this. never blindly update the tests to conform to the code. the tests should make logical sense as standalone checks, so ensure that the test makes sense on its own, and it a resonable and sane check to make on the code. given this, then you can update their the code or the tests to be in line with each other.


$ARGUMENTS