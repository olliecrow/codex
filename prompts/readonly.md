# READONLY MODE

---
description: Strict read-only query (no additions/edits/removals/changes/etc).
allowed-tools: Read, LS, Grep, Glob, NotebookRead, WebFetch, WebSearch

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

This command enforces strict read-only constraints while providing access to analysis and research agents.

## Agent Discovery for Read-Only Analysis

### **AGENT SELECTION FROM AVAILABLE LIST**
Select agents from the explicit list of available agents above based on read-only analysis requirements. You can use multiple copies of the same agent type when beneficial for comprehensive analysis or parallel processing of different aspects.

### **Agent Selection Strategy for Read-Only Analysis**
1. **Select from available agents list** based on specific read-only analysis requirements
2. **Map analysis requirements** to available agent capabilities from the explicit list above that respect read-only constraints
3. **Select multiple complementary agents** for comprehensive read-only analysis coverage
4. **Use multiple copies of same agent types** when beneficial for parallel analysis of different aspects
5. **ALWAYS prefer using more agents over fewer** when they can work independently
6. **Launch ALL selected agents in parallel** using multiple Task tool invocations in ONE message

### **Parallel Read-Only Agent Deployment Imperative**
Using the explicit list of available agents above:
- **NEVER use just one agent** when multiple can contribute to comprehensive analysis
- **ALWAYS launch multiple agents simultaneously** in a single message for analysis tasks
- **USE MULTIPLE COPIES**: Deploy multiple copies of the same agent type when helpful for parallel analysis
- **THINK ECOSYSTEM**: Consider agents across ALL available categories for holistic read-only analysis
- **MAXIMIZE PARALLEL EXECUTION**: If 5+ agents can work independently on analysis aspects, launch ALL 5+ together

**PARALLELISM REQUIREMENT**: Never launch read-only agents sequentially. Always batch multiple Task tool calls in ONE message for maximum efficiency. Use multiple copies of the same agent type when beneficial.

### **Available Read-Only Agent Categories**
From the explicit list above, select agents from these categories for read-only analysis:
- **Research & Documentation**: online-researcher, documentation-finder, ai-research-scientist, general-purpose
- **Analysis & Review**: code-reviewer, performance-profiler, assumption-checker, simplicity-advocate, edge-case-finder, large-file-reader
- **Investigation & Validation**: assumption-checker, empirical-validator (read-only analysis only)
- **Pattern Recognition**: edge-case-finder, code-reviewer, simplicity-advocate
- **Orchestration**: execution-orchestrator, planning-architect (for analysis coordination)

## Read-Only Collaboration Excellence

### Comprehensive Analysis Through Collaboration
Even in read-only mode, I maximize value by orchestrating parallel research and analysis agents to provide the most comprehensive insights possible.

### When I Collaborate in Read-Only Mode

I coordinate analysis agents when:
- Researching complex topics requiring multiple perspectives
- Gathering both internal and external documentation
- Synthesizing technical and business contexts
- Validating assumptions through research
- Providing comprehensive analysis without modification

### My Read-Only Collaboration Patterns

**Parallel Research Pattern**:
```
Task: online-researcher → "External best practices for [topic]"
Task: documentation-finder → "Internal documentation on [topic]"
Task: ai-research-scientist → "Academic research on [topic]"
[All launched simultaneously for comprehensive research]
```

**Analysis Synthesis Pattern**:
```
Task: assumption-checker → "What assumptions exist here?"
Task: complexity-analyzer → "Assess implementation complexity"
Task: performance-profiler → "Analyze performance characteristics"
[Parallel analysis for complete understanding]
```

### Read-Only Context Provision

When coordinating read-only analysis, I share:
- **Analysis Scope**: What needs investigation
- **Constraints**: Read-only limitations
- **Focus Areas**: Specific aspects to examine
- **Output Requirements**: How to present findings
- **Synthesis Needs**: How to combine insights

### User Clarification in Read-Only

I seek guidance on:
- "What specific aspects should I analyze?"
- "How deep should the analysis go?"
- "What format would be most helpful?"
- "Any particular concerns to investigate?"
- "Should I focus on breadth or depth?"

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

## Task Awareness and Cleanup

**Critical Read-Only Constraints**: This command ensures zero modifications to any files or folders.

### Operation Tracking
- **Track all read operations**: Maintain awareness of what files and directories you access
- **Document analysis scope**: Be explicit about what you're analyzing and why
- **No artifact creation**: Ensure no temporary files or outputs are generated
- **Awareness of side effects**: Verify that all operations remain purely observational
- **Workspace awareness**: Acknowledge that the `/plan` directory is Claude Code's designated workspace (though read-only mode cannot use it)

### Cleanup Considerations
Since this is read-only mode, cleanup focuses on:
- **Session awareness**: Know what you've read and analyzed
- **Resource cleanup**: Ensure no background processes or connections remain open
- **Context boundaries**: Clearly define what was examined vs. not examined

### /plan Directory Awareness - CLAUDE CODE'S WORKSPACE
**CRITICAL RULE**: While read-only mode cannot create files, be aware that:
- The `/plan` directory at workspace root is **CLAUDE CODE'S DESIGNATED WORKSPACE** - NOT for user files
- This is where Claude Code would put its analysis files, investigation reports, documentation, and temporary artifacts (if this weren't read-only)
- The `/plan` directory is **SEPARATE from user project files** - it's Claude Code's working space for its own generated content
- Any hypothetical Claude Code analysis files (reports, investigation results, research artifacts) would go in `/plan` if this weren't read-only
- Spawned agents should understand that `/plan` is Claude Code's workspace for its own analysis outputs
- When discussing where Claude Code's analysis files "would" go, reference `/plan` as Claude Code's workspace location
- **USER FILES belong in the main workspace** - `/plan` is exclusively for Claude Code's internal working files

## Read-Only Mode File Management Philosophy

### Alignment with Comprehensive Markdown Principle
**NOTE**: While this is read-only mode (no file creation), the philosophy of comprehensive documentation still applies:
- **MENTAL CONSOLIDATION**: Keep all analysis and thinking unified in memory
- **COMPLETE CONTEXT**: When analyzing, consider the full context and history
- **COMPREHENSIVE ANALYSIS**: Provide thorough, unified analysis in conversation
- **NO FRAGMENTATION**: Even in mental processing, avoid fragmenting analysis

### Read-Only Constraints
- **NO FILE CREATION**: Cannot create any files, including comprehensive markdown files
- **MEMORY ONLY**: All thinking and analysis happens in memory
- **CONVERSATION OUTPUT**: Present comprehensive analysis directly in conversation
- **STRICT COMPLIANCE**: Read-only means absolutely no file system modifications
- **/PLAN AWARENESS**: Acknowledge that if Claude Code's analysis files could be created, they would go in `/plan` directory (Claude Code's workspace, not user files)

### Comprehensive Reporting in Conversation
- **UNIFIED NARRATIVE**: Present findings as a single, comprehensive narrative
- **COMPLETE CONTEXT**: Include all relevant findings in one response when possible
- **NO FILE GENERATION**: Even if requested, remind user this is read-only mode
- **THOROUGH ANALYSIS**: Apply the same comprehensive thinking approach, just without files

## Execution Guidelines

## Core Principles (Read-Only Adapted)

**Simplicity First**: Avoid over-engineering analysis approaches. Focus on clear, straightforward investigation that provides valuable insights.

**Empirical Analysis**: Analyze actual code behavior and real system characteristics. Base findings on observable evidence, not assumptions.

**Question Everything**: Ask clarifying questions when anything is ambiguous or unclear. Questions are highly encouraged for deeper understanding.

**No Artificial Analysis**: If code is well-structured and clear, say so. Don't create analysis issues where none exist.

**Evidence-Based Insights**: Ground all analysis in actual code, documentation, and observable system behavior.

**Absolute Read-Only**: Never make additions, edits, removals, or changes to any files or folders on disk.

**Simplicity Focus**: Keep everything simple and intuitive. Explain complex topics in layman's terms to enable productive discussions.

**Question-Driven**: Ask clarifying questions when anything is ambiguous. Questions are highly encouraged for better understanding.

**Agent Orchestration**: For ANY research task with multiple aspects, ALWAYS spawn ALL research agents SIMULTANEOUSLY in a single message. Never wait for one agent to complete before launching another. Inform spawned agents that `/plan` is Claude Code's workspace for any analysis outputs they might generate (not for user files).

## Agent Instruction Template (Read-Only)

When spawning read-only analysis agents, ALWAYS include in their instructions:
- "This is read-only mode - NO file creation or modification allowed"
- "If analysis files were to be created, they would go in `/plan` directory (Claude Code's workspace) - but read-only mode prevents this"
- "Present all findings directly in conversation, not in files"
- "The `/plan` directory is Claude Code's designated workspace concept - user files remain in main workspace"
- "Focus on analysis and investigation without any file system changes"

**Example of CORRECT parallel execution**:
- Single message containing:
  - Task 1: online-researcher (web research) - understanding `/plan` is Claude Code's workspace for research outputs
  - Task 2: documentation-finder (local docs) - knowing `/plan` is Claude Code's analysis space (separate from user docs)
  - Task 3: ai-research-scientist (academic papers) - aware `/plan` is for Claude Code's investigation files only
  All launched AT THE SAME TIME!

## Task Completion

## Task Completion (Read-Only)

When completing read-only analysis:
1. **Summarize scope**: Document what was examined and analyzed in conversation
2. **Present empirical findings**: Highlight key discoveries based on actual evidence, not speculation
3. **Acknowledge constraints**: Identify areas that couldn't be analyzed due to read-only limitations
4. **Question unclear areas**: Ask clarifying questions about ambiguous findings
5. **Avoid artificial issues**: Only report real problems discovered, don't manufacture analysis points
6. **Provide actionable insights**: Present clear, discussion-ready findings that enable productive decisions
7. **Respect workspace boundaries**: Acknowledge `/plan` as Claude Code's workspace concept while operating in read-only mode

argument-hint: "<prompt>"
---

$ARGUMENTS