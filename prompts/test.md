# TEST EXECUTION MODE

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

This command focuses on comprehensive test discovery and execution across the entire project.

## Agent Discovery for Testing Excellence

### **AGENT SELECTION FROM AVAILABLE LIST**
Select agents from the explicit list of available agents above based on testing requirements. You can use multiple copies of the same agent type when beneficial for comprehensive analysis or parallel processing of different testing aspects.

### **Agent Selection Strategy for Testing**
1. **Select from available agents list** based on specific testing requirements
2. **Map testing requirements** to available agent capabilities from the explicit list above
3. **Select multiple complementary agents** for comprehensive test coverage
4. **Use multiple copies of same agent types** when beneficial for parallel analysis of different testing aspects
5. **ALWAYS prefer using more agents over fewer** when they can work independently
6. **Launch ALL selected agents in parallel** using multiple Task tool invocations in ONE message

### **Parallel Testing Agent Deployment Imperative**
Using the explicit list of available agents above:
- **NEVER use just one agent** when multiple can contribute to testing excellence
- **ALWAYS launch multiple agents simultaneously** in a single message for testing tasks
- **USE MULTIPLE COPIES**: Deploy multiple copies of the same agent type when helpful for parallel testing analysis
- **THINK ECOSYSTEM**: Consider agents across ALL available categories for holistic testing
- **MAXIMIZE PARALLEL EXECUTION**: If 7+ agents can work independently on testing aspects, launch ALL 7+ together

**CRITICAL**: Maximum parallelism is NON-NEGOTIABLE - spawn ALL independent test agents AT ONCE, never sequentially. Use multiple copies of the same agent type when beneficial.

### **Available Testing Agent Categories**
From the explicit list above, select agents from these categories for testing needs:
- **Testing & Validation**: test-guardian, empirical-validator
- **Analysis & Review**: code-reviewer, performance-profiler, assumption-checker, simplicity-advocate, edge-case-finder
- **Quality Assurance**: assumption-checker, edge-case-finder, code-reviewer
- **Implementation**: software-engineer, ai-engineer, general-purpose
- **Research**: online-researcher, documentation-finder, ai-research-scientist
- **Orchestration**: execution-orchestrator, planning-architect

## Testing Collaboration Excellence

### Comprehensive Testing Through Collaboration
I enhance test effectiveness by collaborating with specialized agents to ensure complete coverage, validate assumptions, and identify edge cases that might be missed in isolation.

### When I Collaborate on Testing

I seek testing perspectives when:
- Designing comprehensive test strategies
- Identifying untested edge cases
- Validating test assumptions
- Assessing performance test needs
- Reviewing test coverage gaps
- Clarifying acceptance criteria

### My Testing Collaboration Patterns

**Coverage Validation Pattern**:
```
Task: edge-case-finder → "What scenarios are we missing?"
Task: assumption-checker → "What assumptions do our tests make?"
Task: software-engineer → "Are tests reflecting real usage?"
[Parallel validation for comprehensive coverage]
```

**Test Quality Review Pattern**:
```
Task: simplicity-advocate → "Are tests unnecessarily complex?"
Task: performance-profiler → "Should we add performance tests?"
Task: security-specialist → "Do we need security test cases?"
[Simultaneous quality assessment from all angles]
```

### Test Context Sharing

When requesting test review, I provide:
- **Test Strategy**: Overall approach and methodology
- **Coverage Metrics**: What's tested vs. untested
- **Risk Areas**: Critical paths requiring thorough testing
- **Failure History**: Previous test failures and fixes
- **Environment Context**: Test environment specifications

### User Clarification for Testing

I seek user input on:
- "What scenarios are most critical to your users?"
- "What's the acceptable performance threshold?"
- "Should we prioritize breadth or depth of testing?"
- "Are there specific compliance requirements?"
- "What's the risk tolerance for this release?"

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

When spawning test-related agents, ALWAYS include in their instructions:
- "Use `/plan` directory for ALL test analysis files, investigation reports, and coverage artifacts - this is Claude Code's workspace, NOT for user files"
- "Create any test analysis markdown files in `/plan` directory (Claude Code's workspace)"
- "Do not modify actual test files in the main project - those belong to the user's project"
- "The `/plan` directory is Claude Code's designated workspace for test analysis artifacts - user test files remain in main workspace"
- "NEVER put user test files or user-requested test modifications in `/plan` - only Claude Code's test analysis work goes there"

**PARALLELISM RULE**: If multiple test agents can work independently, launch them ALL in ONE message with multiple Task tool invocations

## Testing Collaboration Excellence

### Comprehensive Testing Through Collaboration
I enhance test effectiveness by collaborating with specialized agents to ensure complete coverage, validate assumptions, and identify edge cases that might be missed in isolation.

### When I Collaborate on Testing

I seek testing perspectives when:
- Designing comprehensive test strategies
- Identifying untested edge cases
- Validating test assumptions
- Assessing performance test needs
- Reviewing test coverage gaps
- Clarifying acceptance criteria

### My Testing Collaboration Patterns

**Coverage Validation Pattern**:
```
Task: edge-case-finder → "What scenarios are we missing?"
Task: assumption-checker → "What assumptions do our tests make?"
Task: software-engineer → "Are tests reflecting real usage?"
[Parallel validation for comprehensive coverage]
```

**Test Quality Review Pattern**:
```
Task: simplicity-advocate → "Are tests unnecessarily complex?"
Task: performance-profiler → "Should we add performance tests?"
Task: security-specialist → "Do we need security test cases?"
[Simultaneous quality assessment from all angles]
```

### Test Context Sharing

When requesting test review, I provide:
- **Test Strategy**: Overall approach and methodology
- **Coverage Metrics**: What's tested vs. untested
- **Risk Areas**: Critical paths requiring thorough testing
- **Failure History**: Previous test failures and fixes
- **Environment Context**: Test environment specifications

### User Clarification for Testing

I seek user input on:
- "What scenarios are most critical to your users?"
- "What's the acceptable performance threshold?"
- "Should we prioritize breadth or depth of testing?"
- "Are there specific compliance requirements?"
- "What's the risk tolerance for this release?"

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

## Test Awareness and Cleanup

**Critical**: This command emphasizes awareness of all testing activities and artifacts:

### CRITICAL RULE: /plan Directory Usage - CLAUDE CODE'S WORKSPACE ONLY
**The `/plan` directory is CLAUDE CODE'S EXCLUSIVE WORKSPACE for files that Claude Code creates:**
- **Claude Code workspace**: `/plan` is ONLY for files that Claude Code creates during test analysis and investigations
- **NOT for user files**: `/plan` is NOT for user project files, actual test files, or production code
- **Create /plan directory**: Claude Code creates `/plan` at workspace root if it doesn't exist for its own work
- **Claude Code scratch space**: `/plan` is Claude Code's designated scratch space for temporary analysis work
- **Never committed**: The `/plan` directory will NEVER be committed to GitHub - it's Claude Code's private workspace
- **Claude Code artifacts**: ALL test reports, coverage files, and analysis that Claude Code generates go in `/plan`
- **Claude Code documentation**: Test journals, debugging notes, and investigation files that Claude Code creates belong in `/plan`
- **User files stay put**: Actual project test files (like test/, __tests__/, spec/) remain in their proper workspace locations

### Test Artifact Tracking (Claude Code's Work in /plan)
- **Track test execution**: Claude Code maintains inventory of all tests run and analysis outputs in `/plan`
- **Monitor Claude Code artifacts**: Be aware of test reports, coverage files, and analysis data Claude Code generates in `/plan`
- **Document test scope**: Claude Code records which test suites, frameworks, and commands were discovered and executed in `/plan`
- **Track Claude Code files**: Note any investigation reports, analysis documents, or debugging files Claude Code creates in `/plan`
- **User test files**: Actual project test files remain in their original locations (test/, __tests__/, spec/, etc.)

### Intelligent Test Cleanup (Claude Code's /plan Workspace)
- **Context-specific cleanup**: Remove Claude Code's analysis artifacts from `/plan` based on actual investigation activities
- **Preserve /plan directory**: The `/plan` directory itself should be preserved for Claude Code's future use
- **Clean Claude Code temporaries**: Remove temporary investigation files, debug outputs, and analysis data Claude Code created in `/plan`
- **Maintain test integrity**: Ensure cleanup doesn't affect user's actual test files or future test execution capability
- **Preserve baselines in /plan**: Keep essential analysis outputs that Claude Code created as baselines within `/plan`
- **User files untouched**: Never clean up or modify actual project test files - only Claude Code's `/plan` workspace

## Core Principles

**Simplicity First**: Avoid over-engineering test strategies. Focus on clear, straightforward test execution that gets the job done.

**Empirical Validation**: Tests ARE empirical validation. Validate and re-validate through multiple test methods. Test assumptions empirically whenever possible.

**Question Everything**: Ask clarifying questions when test behavior is ambiguous. Questions are highly encouraged for better test understanding.

**No Artificial Work**: If tests are passing and comprehensive, say so. Don't create testing issues where none exist.

**Test-Driven Awareness**: Tests are the bedrock of any project. Always establish test baselines before any changes and validate against them after.

Tests are the foundation of reliable software. This command takes a systematic approach to finding and executing tests.

1. discover test frameworks and test files by examining:
   - package.json, requirements.txt, Cargo.toml, go.mod, or other dependency files
   - common test directories: test/, tests/, spec/, __tests__/, etc.
   - test file patterns: *test*, *spec*, test_*.py, *.test.js, *.spec.ts, etc.
   - Makefile, scripts/, or other build configuration files
   - README.md or other documentation for test commands

2. identify and run all available test commands:
   - npm test, yarn test, pnpm test
   - pytest, python -m unittest, nose2
   - cargo test, go test, mvn test, gradle test
   - make test, make check
   - custom test scripts defined in package.json or other config files
   - any test runners specific to the project

3. execute tests systematically:
   - create `/plan` directory if it doesn't exist for Claude Code's test analysis artifacts
   - run each discovered test command on user's actual test files
   - capture and report all output (save Claude Code's analysis logs to `/plan` if needed)
   - note passes, failures, skips, and errors
   - identify test coverage if available (save Claude Code's coverage analysis to `/plan`)
   - check for integration tests, unit tests, e2e tests separately if configured
   - user's test files remain in their original project locations

4. provide comprehensive results:
   - total tests run across all test suites
   - number of passes, failures, skips
   - specific failure details and error messages
   - test execution time
   - any tests that couldn't be run and why

## Ultra-Thinking Mode for Complex Testing

For complex test scenarios, enable ultra-thinking mode:
- Think comprehensively about all possible test frameworks and execution paths
- Take a holistic view of the entire test ecosystem
- Use comprehensive agent orchestration for thorough test discovery
- Validate test results through multiple verification methods
- Take as much time as needed for complete test analysis

validate that tests are actually being executed, not just commands running without finding tests.

if no tests are found, investigate why and report what was checked.

if test commands fail to run, diagnose the issue (missing dependencies, configuration problems, etc).

be thorough - ensure no test suite is missed. check multiple potential test commands even if one succeeds.

do not modify any tests or code. only execute existing tests as they are.

do not interact with git! do not use the git command, even readonly operations.

provide clear, structured output showing all test results.

## Agent Orchestration for Comprehensive Testing

**ALWAYS leverage MAXIMUM parallel agent execution** - Launch ALL independent agents TOGETHER:

### For Coverage Gaps
**Launch ALL analysis agents SIMULTANEOUSLY** in ONE message to identify untested scenarios, validate assumptions, and analyze performance. Never launch them one-by-one!

### For Test Performance Issues
**Deploy ALL performance agents AT ONCE** - Use a single message with multiple Task invocations for profiling, bottleneck analysis, and resource usage analysis.

### For Test Quality Assessment
**Launch ALL quality analysis agents TOGETHER** - Single message containing:
- Task 1: assumption-checker (verify test assumptions)
- Task 2: edge-case-finder (identify untested scenarios)
- Task 3: test-guardian (validate test execution)
All launched SIMULTANEOUSLY!

## Comprehensive Test Documentation Strategy

### CRITICAL: Long Single Markdown Files for Testing
**CORE PRINCIPLE**: Always maintain comprehensive, single markdown files for all testing activities:
- **Complete test history**: Document all test runs, failures, debugging steps in ONE file
- **Context preservation**: Keep all test-related thinking and analysis together
- **Debugging continuity**: Previous test failures and fixes provide crucial context
- **Single source of truth**: One file contains the complete testing narrative

### Test Documentation Workspace (Claude Code's /plan Only)
- **ONE FILE APPROACH**: Claude Code creates ONE comprehensive markdown file for ALL its test analysis documentation in `/plan`
- **LOCATION**: ALL Claude Code test documentation MUST be created in `/plan` directory (e.g., `/plan/comprehensive_test_journal.md`)
- **CONTINUOUS LOGGING**: Claude Code appends each test analysis, investigation, and findings to the same file in `/plan`
- **NAMING**: Claude Code uses descriptive names like `/plan/comprehensive_test_journal.md` for its analysis work
- **ACCUMULATE KNOWLEDGE**: Failed test analysis and debugging steps are valuable context Claude Code maintains in `/plan`
- **SELECTIVE CLEANUP**: Preserve Claude Code's comprehensive test documentation in `/plan` for future reference
- **User documentation**: Any user-requested documentation goes in appropriate project locations, NOT in `/plan`

### Strict No-Report Policy (Claude Code Files Only)
- **NEVER** create Claude Code's analysis files, investigation reports, or test summaries in the workspace root or project directories
- **ALWAYS** use `/plan` directory for Claude Code's test documentation, analysis reports, or investigation files
- **NEVER** leave Claude Code's analysis markdown files outside `/plan` that could be committed
- **EXCEPTION**: Only create persistent files outside `/plan` when user explicitly requests with phrases like "save test results to a file" - these go in appropriate project locations, NOT `/plan`
- **OUTPUT**: Present all test results and findings directly in the conversation
- **SAFE ZONE**: The `/plan` directory is Claude Code's safe workspace for temporary analysis and will never be committed
- **User files**: User-requested files belong in proper project locations, not in Claude Code's `/plan` workspace

### Test Artifact Cleanup Requirements (Claude Code's /plan Workspace)
- **TRACK**: Claude Code maintains awareness of every analysis file it creates during investigations, especially in `/plan`
- **IMMEDIATE**: Delete Claude Code's analysis artifacts from `/plan` as soon as they serve their purpose
- **COVERAGE FILES**: Claude Code stores its coverage analysis in `/plan`, removes after analysis unless explicitly requested by user
- **TEST OUTPUTS**: Claude Code directs all its investigation files, analysis logs, and debug data to `/plan` for cleanup
- **PRESERVE /plan**: The `/plan` directory itself should remain for Claude Code's future use
- **FINAL**: Before task completion, verify all Claude Code's temporary files in `/plan` are cleaned (but keep `/plan` itself)
- **VERIFY**: Use LS to confirm no Claude Code artifacts remain outside `/plan`
- **USER FILES UNTOUCHED**: Never clean up or modify user's actual project files - only Claude Code's `/plan` workspace

## Test Completion and Cleanup

After test execution:
1. **Create /plan if needed**: Ensure `/plan` directory exists at workspace root for Claude Code's analysis artifacts
2. **Review test scope**: Document what test frameworks, commands, and files were analyzed (distinguish between user project test files and Claude Code analysis in `/plan`)
3. **Cleanup Claude Code artifacts**: Remove Claude Code's temporary analysis files, debug outputs, and investigation data from `/plan`
4. **Preserve essential outputs**: Keep Claude Code's analysis reports and coverage data in `/plan` ONLY if explicitly requested by user
5. **Validate test integrity**: Ensure cleanup doesn't affect user's actual test files or future test execution capability
6. **Report empirical results**: Present comprehensive test execution summary in conversation with actual pass/fail counts
7. **Preserve /plan directory**: Keep the `/plan` directory itself for Claude Code's future analysis and documentation
8. **Confirm no artificial issues**: Only report real test failures and issues, not manufactured problems
9. **USER FILES SAFE**: Never modify, move, or clean user's actual project test files - they remain in their proper locations

$ARGUMENTS