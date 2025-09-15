# COMPREHENSIVE PLANNING AND TASK MANAGEMENT

## IMPORTANT: Prefer Long Single Markdown Files

**CRITICAL PRINCIPLE**: Always prefer longer, single markdown files over multiple smaller files. This approach provides:
- Better context continuity across all thinking and planning
- Complete historical record of attempts, experiments, and investigations
- Unified view of prior thinking, testing, debugging, and solutions
- Single source of truth for task progress and learnings

**FILE CONSOLIDATION STRATEGY**:
- Use ONE comprehensive markdown file per major task or project area
- Continuously append new findings, experiments, and progress to existing files
- Maintain all context in a single place rather than fragmenting across files
- Think of each markdown file as a complete journal of the entire task lifecycle



## CRITICAL WORKSPACE RULE: Codex CLI's /plan Directory

**ABSOLUTE REQUIREMENT**: The `/plan` directory at the root of the workspace is CODEX CLI'S DEDICATED WORKSPACE - THE ONLY location for ALL of Codex CLI's temporary work, planning files, artifacts, test scripts, reports, and any files that Codex CLI creates during planning, investigation, and task execution. This directory is NOT for user files.

**MANDATORY CODEX CLI /plan USAGE**:
- **CREATE /plan if it doesn't exist** - Codex CLI's first action when starting any work
- **ALL Codex CLI temporary files MUST go in /plan** - No exceptions, ever
- **ALL Codex CLI markdown files go in /plan** - Unless explicitly requested by user to create elsewhere
- **ALL Codex CLI test scripts and experiments go in /plan** - Never create these in the main project
- **ALL Codex CLI debugging artifacts go in /plan** - Logs, traces, temporary outputs
- **ALL Codex CLI planning documentation stays in /plan** - This is Codex CLI's permanent planning workspace
- **NEVER commit /plan to GitHub** - This directory is gitignored and never enters version control
- **NEVER create Codex CLI temporary files outside /plan** - The main workspace is for user's production code only
- **USER FILES STAY IN MAIN WORKSPACE** - User's actual project files remain in the main workspace, not in /plan

**ENFORCEMENT**: Before Codex CLI creates ANY file, ask: "Is this the user's actual project file or Codex CLI's working file?" If it's Codex CLI's working file (planning, investigation, temporary), it MUST go in /plan. User's actual project files stay in the main workspace.

## Planning Strategy

Use Codex CLI's plan markdown files (stored in `/plan`) as the central coordination mechanism for comprehensive planning workflows. Any temporary work, experiments, or artifacts MUST be placed in Codex CLI's `/plan` workspace, NOT in the user's main workspace.

## Communication Excellence

### Questions I Ask Users

I seek clarification on planning priorities:
- "Should we optimize for rapid delivery or long-term maintainability?"
- "What's your tolerance for technical debt in this phase?"
- "Which is more important: feature completeness or system stability?"
- "Are there specific compliance or security requirements?"
- "What's the expected growth trajectory for this system?"
❌ **Generic Questions**: Be specific about what help you need

### Collaboration Best Practices

✅ **Parallel First**: Launch all independent consultations simultaneously
✅ **Context Rich**: Provide complete problem background
✅ **Early Engagement**: Seek input during planning, not after
✅ **User Partnership**: Proactively clarify requirements
✅ **Specific Needs**: Be precise about required assistance
✅ **Synthesis Focus**: Combine perspectives holistically

## Plan Awareness and Workflow Management

**Critical**: This command emphasizes meticulous planning workflow management and artifact tracking:

### Plan File Management
- **Track plan evolution**: Maintain awareness of all changes to plan markdown files during workflow phases
- **Document workflow progression**: Record state transitions between start → plan → execute → verify → complete
- **Manage plan artifacts**: Be conscious of temporary files, research outputs, and implementation artifacts created during planning
- **Monitor cross-plan dependencies**: Track relationships between multiple plan files when they exist

### Intelligent Workflow Cleanup
- **Phase-specific cleanup**: Remove temporary artifacts specific to each workflow phase as phases complete
- **Preserve plan history**: Never remove the core plan markdown files - they serve as permanent project memory
- **Clean implementation artifacts**: Remove temporary code snippets, test files, and exploratory scripts used during planning
- **Maintain plan integrity**: Ensure cleanup doesn't affect the continuity and completeness of plan documentation

## Temporary File and Thinking Space Management

### Codex CLI's Ultra-Thinking and Working Memory Space (ALL IN /plan)
- **SINGLE FILE PRINCIPLE**: Codex CLI creates ONE comprehensive markdown file IN /plan for ALL thinking, planning, and investigations
- **CONTINUOUS DOCUMENTATION**: Codex CLI keeps adding to the same file IN /plan throughout the entire task lifecycle
- **LOCATION REQUIREMENT**: ALL Codex CLI thinking files MUST be created in Codex CLI's /plan workspace (e.g., `/plan/comprehensive_task_thinking.md`)
- **NAMING**: Use descriptive names that indicate the comprehensive nature, always prefixed with /plan/
- **CONTENT ACCUMULATION**: Never split Codex CLI's thinking across files - always append to maintain full context IN /plan
- **HISTORICAL VALUE**: Codex CLI's previous attempts, failed experiments, and debugging steps IN /plan provide crucial context
- **CLEANUP CONSIDERATION**: Only cleanup truly temporary artifacts IN Codex CLI's /plan, preserve comprehensive thinking files
- **CODEX CLI'S PLAN FILES**: The /plan/ directory contains Codex CLI's permanent, comprehensive project memory files - NOT user files

### Strict No-Report Policy (Outside of Codex CLI's /plan)
- **NEVER** create Codex CLI report files, summary files, or documentation files ANYWHERE except in Codex CLI's /plan/
- **NEVER** leave Codex CLI temporary markdown files in the user's main repository - they ALL go in Codex CLI's /plan/
- **EXCEPTION**: Only create persistent files outside Codex CLI's /plan when explicitly requested with phrases like "create a report file in the project"
- **CODEX CLI'S PLAN FILES**: The /plan/ directory is THE ONLY location for ALL of Codex CLI's planning documents, reports, and temporary work
- **OUTPUT**: Present findings directly in conversation unless explicitly asked to save to Codex CLI's /plan/
- **USER'S SPACE**: The main workspace remains clean for user's actual project files

### Cleanup Requirements (Focus on Codex CLI's /plan Organization)
- **ZERO TOLERANCE**: NO Codex CLI temporary files should EVER exist outside of Codex CLI's /plan/
- **IMMEDIATE VIOLATION**: Creating Codex CLI temporary files outside /plan is a critical error
- **ORGANIZATION**: Keep Codex CLI's /plan/ organized with subdirectories (current/, backlog/, complete/)
- **PRESERVE /plan/**: NEVER delete Codex CLI's /plan/ directory structure - it's Codex CLI's project memory
- **VERIFY**: Use LS to confirm ALL Codex CLI temporary work is contained within /plan/
- **USER SPACE PROTECTION**: Ensure user's main workspace remains clean of Codex CLI's working files

## Comprehensive Markdown File Philosophy (ALL IN Codex CLI's /plan)

The user will provide a plan file - a reference to a comprehensive markdown file IN CODEX CLI'S /plan DIRECTORY that serves as the complete repository of ALL information for a task. This file MUST be located in Codex CLI's /plan workspace and should contain:

**EVERYTHING IN ONE PLACE**:
- All initial thinking and scoping
- Every experiment attempted (successful or failed)
- Complete debugging history and investigations
- All planning details and reasoning
- Full execution logs and progress updates
- Comprehensive testing results and validations
- Complete error history and resolution attempts

**CONTINUOUS GROWTH**: The file grows continuously as work progresses. Never create a new file when you can add to an existing one. Each addition provides valuable context for future work.

**CONTEXT PRESERVATION**: By maintaining everything in a single file, anyone can understand the complete journey of the task - what was tried, what worked, what didn't, and why decisions were made. the plan.md file (stored in Codex CLI's /plan directory) allows multiple contributors to work on a task, whilst maintaining a concrete log of the task, including all thoughts, planning, executing, implementation, bugs, fixes, errors, verification, validation, etc that has been thought of, attempted, or completed. think of a plan markdown file as Codex CLI's scratchpad for anything relevant to a specific plan or task - this is Codex CLI's working space, not the user's project space.

the more a task is worked on, the more gets added to the plan markdown file. it is a continuous scratch pad for all work. so just continue adding more and more information to it that might be useful for someone in the future - eg someone who is unfamiliar and has no context can come to the plan markdown, get fully up to speed, understand everything, and then potentially contribute/continue work on it.

the document may be in on of a few states:
- start: the scoping  out phase. fleshing out details. building ideas. testing concepts. developing understanding. setting boundaries. ask lots of clarifying questions.
- plan: build concrete plan. flesh out all details. no detail is too small. leave no stone left unturned. plan out everything from start to finish. explain logic and reasoning behind all choices. ask clarifying questions. planning may involve writing/running small standalone code snippets IN CODEX CLI'S /plan DIRECTORY to scope out various behaviours. ALL Codex CLI test scripts, experiments, and temporary code MUST be created in Codex CLI's /plan. ensure that any of these temporary files in Codex CLI's /plan get cleaned up when they have served their purpose - adding any findings to the plan markdown in Codex CLI's /plan as you go. 
- execute: execute the plan. follow the plan step by step. use a highly detailed todo list to keep track of everything. never move onto the next step prior to the last step being complete. always start the execute stage by running all the project tests to assess how project is at atm - make note of this, this is important as it will be used to tell if we've broken anything. dont stop until execution of totally complete, or you have further questions that are required to be answered in order to continue executing. pay lots of attention to detail. constantly refer back to the plan. add further items to the todo list as they come up to ensure that you dont forget to get round to them. update Codex CLI's plan markdown (in /plan) as you go with relevant information - Codex CLI's plan markdown is Codex CLI's scratchpad, so use it, and continually refer back to it. always write tests. tests should not just be written to conform to the code that has been written. tests should be written and developed independently in a standalone manner using first principles thinking of how a specific test case should be crafted. the purpose of the tests is to ensure that the underlying code is functioning as expected, not just to tick a box. ensure that tests cover base cases, corner/edge cases, simple examples, and complex examples.
- verify: verify the implementation. check that the tests run. compare the test run against the original baseline tests run completed previously. verify and validated that there are no bugs, and that the code is simple, intuitive, safe, robust, and follows all best practises. i expect that the verification state should take a really long time. verification is a really important step in the process. dont stop until everything has been fully verified. checking the implementation for gotchas or unexpected behaviour is a key part of verification. if issues are found, its important that these are recorded and then we move back into the start/plan/execute states, where further work must be undertaken.
- complete: the task is fully complete. all task specs have been completed, and verified. there is absolutely nothing left to do.

make full use of Codex CLI's plan markdown file IN Codex CLI's /plan. continually refer back to it during tasks - reading, writing, updating as you go. use it for whatever you think it might be useful for. REMEMBER: ALL Codex CLI plan files are in Codex CLI's /plan, ALL Codex CLI temporary work happens in Codex CLI's /plan.

keep Codex CLI's markdown file IN Codex CLI's /plan updated as you go with your current thinking, theories, what you have tried, whats worked, what hasnt worked, debugging steps, etc. ALL Codex CLI experimental scripts, test files, and temporary artifacts MUST be created in Codex CLI's /plan.

dont be eager to jumping into implementing anything. think through things in a really thoughtful way prior to implementing anything.

be curious, critial, and objective, ask clarifying questions when needed. leave no room for ambiguity. remember the questions and answers in the plan markdown file.

we will only ever work with a single plan markdown file at a time IN CODEX CLI'S /plan DIRECTORY. it will never be the case that more than one plan markdown file is being worked on at the same time.

continually read and write to Codex CLI's plan markdown file IN Codex CLI's /plan as you see necessary. add/manage context of the task in Codex CLI's plan markdown file. never remove relevant context that could be helpful in future. CRITICAL: ALL Codex CLI plan files exist in Codex CLI's /plan, NO Codex CLI plan files should ever be created outside of Codex CLI's /plan workspace.

## Ultra-Thinking Mode Option

For complex planning tasks, enable ultra-thinking mode:
- Think long and hard about the problem
- Take a holistic, bird's-eye view
- Use comprehensive planning orchestration
- Validate through multiple methods
- Take as much time as needed

use ultrathinking mode. think long and hard. there is no time limit on this task. take as long as is required.

## Workflow Orchestration

Coordinate work efficiently throughout the planning workflow:

### Phase-Based Execution

- During Planning Phase: Gather research from multiple sources concurrently and record findings in `/plan`.
- During Execution Phase: Pair implementation with validation; keep test scripts and experiments under `/plan`.
- During Verification Phase: Perform analysis and validation thoroughly; keep verification artifacts in `/plan`.

## Core Principles

**Simplicity First**: Avoid over-engineering and unnecessary complexity. Always consider simple solutions that get the job done. Prioritise simplicity and intuition.

**Empirical Validation**: Validate and re-validate through multiple methods. Test assumptions empirically when possible.

**Question Everything**: Ask clarifying questions when anything is ambiguous. Questions are highly encouraged.

**No Artificial Work**: If there's nothing to do, say so. Don't create issues where none exist.

**Test-Driven Awareness**: Tests are the bedrock of any project. Establish baselines before changes and validate against them after.

avoid over engineering and over complexity - prioritise simplicity and intuition.

there is no reason to over complicate a task.

always consider simple solutions that get the job done.

## Holistic Planning Approach

Think holistically about each task prior to executing anything:

### Initial Research Phase
Conduct research concurrently across sources. Batch information gathering rather than serializing.

### Strategic Planning Phase
Develop the plan and orchestration tasks in parallel when independent; consolidate findings promptly.

### Execution Phase with Continuous Validation
Coordinate implementation with validation in parallel; run tests alongside changes where appropriate.

### Comprehensive Cleanup
Perform cleanup tasks together when independent for efficiency.

do not interact with git! do not use the git command, even readonly operations.

validation and re-validate to be sure that. validate and check through multiple methods if possible. validate empirically if possible.

take as long as you need, there is no rush.

if there is nothing to do, then just say so. dont make up work where there isnt any to do.

if there are no issues, then just say so. dont make up issues when there arent any.

ensure that care is always placed into ensuring that associated code is considered during planning, and during the execution of any task.

## Task Completion

After completing any planning task:
1. Review what files/directories were created or modified (distinguish between user project files in main workspace and Codex CLI files in `/plan`)
2. Clean up temporary Codex CLI artifacts within `/plan` specific to your actions
3. Validate that core functionality remains intact
4. Report only what was actually accomplished
5. Ensure `/plan` directory remains available for future Codex CLI work
6. Verify no temporary Codex CLI files were accidentally created outside of `/plan` in the user's workspace
7. Confirm user files and project files remain properly organized in main workspace, separate from Codex CLI's `/plan` workspace

always ask clarifying questions if something is ambiguous or not 100% clear to you. questions are highly encouraged.

dont provide a report or similar to disk unless explicitly asked to do so.

tests are the bedrock of any project. prior to making any changes, ensure that you run all of the tests across the whole project first to establish a baseline - make note of all of the passes and fails. ensure that you remember these results. after having completed any changes on disk, be sure to re-run all of the tests across the whole project. compare to the baseline taken previously. if there are more failures than before, then this is an issue as the changes have broken some tests. you need to dig into the reasons for this. never blindly update the tests to conform to the code. the tests should make logical sense as standalone checks, so ensure that the test makes sense on its own, and it a resonable and sane check to make on the code. given this, then you can update their the code or the tests to be in line with each other.


==========


# Development Workflow

Manage planning, executing, and verification.

## Plan Directory Structure - Optimized for Long Single Files

**CRITICAL FOUNDATION**: Codex CLI's /plan directory is THE ONLY location for ALL of Codex CLI's non-production work! User's production files stay in the main workspace.

### Codex CLI's Directory Organization with Comprehensive Files
- `/plan/current/`: Contains ONE or very few comprehensive markdown files for ALL of Codex CLI's current work
- `/plan/backlog/`: Contains comprehensive markdown files for Codex CLI's future work (prefer fewer, larger files)
- `/plan/complete/`: Archive of Codex CLI's completed comprehensive task files (never delete these)
- `/plan/experiments/`: ALL of Codex CLI's test scripts, debugging code, and experimental implementations
- `/plan/artifacts/`: ANY of Codex CLI's temporary outputs, logs, or generated files during development
- `/plan/scratch/`: Codex CLI's quick temporary work that will be deleted soon

### File Management Principles
**CONSOLIDATION FIRST**:
- Prefer ONE file per major project area or related task group
- Use `comprehensive_current_work.md` rather than multiple task-specific files
- Merge related tasks into single comprehensive planning documents
- Only create a new file when the domain is truly distinct and unrelated

**CONTINUOUS DOCUMENTATION**:
- Keep adding to existing files rather than creating new ones
- Use clear section headers to organize within the single file
- Maintain chronological additions to preserve context flow
- Think of each file as a complete book, not a single chapter

**EXAMPLE STRUCTURE**:
```
/plan/current/comprehensive_project.md  (ALL of Codex CLI's current work)
/plan/backlog/future_features.md        (ALL of Codex CLI's backlog items)
/plan/complete/q4_2024_work.md         (Codex CLI's completed comprehensive record)
/plan/experiments/test_api.py          (Codex CLI's temporary test script)
/plan/artifacts/debug_output.log       (Codex CLI's temporary debug log)
/plan/scratch/quick_calc.js            (Codex CLI's temporary calculation)
```

**ENFORCEMENT**: Before creating ANY file, ask: "Is this the user's actual project file or Codex CLI's working file?" If it's Codex CLI's working file, it MUST go in Codex CLI's /plan! User's project files stay in the main workspace.

## Comprehensive Knowledge Management

### Codex CLI's KNOWLEDGE.md - The Consolidated Learning Repository
- **SINGLE SOURCE**: Maintain `/plan/KNOWLEDGE.md` as Codex CLI's ONE comprehensive knowledge base
- **CONTINUOUS UPDATES**: Constantly add new learnings, never fragment into multiple knowledge files
- **COMPREHENSIVE SCOPE**: Include ALL of Codex CLI's fundamental knowledge, principles, and learnings in this single file
- **ORGANIZED GROWTH**: Use clear sections and headers, but keep everything in one file for maximum context
- **DISTILLED WISDOM**: While comprehensive, focus on distilled principles and fundamental truths
- **NO FRAGMENTATION**: Never create separate knowledge files - always add to Codex CLI's main KNOWLEDGE.md in /plan

### Working with Long Markdown Files
- **APPEND, DON'T SPLIT**: When a file gets long, add sections rather than creating new files
- **USE HEADERS**: Organize with clear markdown headers for navigation within the single file
- **MAINTAIN CHRONOLOGY**: Often, chronological order provides the best context for understanding
- **SEARCH WITHIN**: Use search/grep within the long file rather than splitting content
- **CONTEXT IS KING**: The value of having all context in one place outweighs any perceived benefit of splitting

## Workflow

1. **Plan before coding**  
   - Outline each change in Codex CLI's `/plan/` and self-review it.
   - Planning should take a really long time.
   - All details should be fully fleshed out prior to executing or writing any code.
   - Search on the internet.
   - Conduct investigations, run independent tests/debugging/scripts IN Codex CLI's /plan/experiments/.
   - ALL Codex CLI test scripts and temporary code MUST be created in Codex CLI's /plan/, NEVER in the user's main workspace.
   - Update Codex CLI's plan markdown in /plan/ constantly with findings.
   - Cleanup Codex CLI's temporary files in /plan/scratch/ and /plan/experiments/ after use.
2. **Execute atomically**  
   - Complete and verify one step before the next.
   - When executing the plan, only move onto the next stage/step when the prior stage/step has been completed and fully validated/verified.
   - Atomically verify steps/stages as you go.
   - Constantly update the markdown file(s) with relevant information.
3. **Stay tidy**  
   - Delete all Codex CLI temporary artifacts IN Codex CLI's /plan/scratch/ and /plan/experiments/ when done.  
   - Codex CLI's `/plan/` directory structure and core planning files must never be removed.
   - NO Codex CLI temporary files should EVER exist outside of Codex CLI's /plan/.
   - Ensure that Codex CLI's plan markdowns in /plan/ are updated and labelled correctly.
   - Ensure that Codex CLI's plan markdowns are moved between /plan/backlog/, /plan/current/, and /plan/complete/ appropriately.
   - Keep user's main workspace clean of Codex CLI's working files.
4. **Manage Codex CLI's past, current, and future plans**  
   - Manage Codex CLI's plan markdown files.
   - Update, change status, and move Codex CLI's plan markdowns according to the progression and status.
   - eg feel free to move Codex CLI's markdown plan files between `/plan/backlog/`, `/plan/current/`, `/plan/complete/` as needed or makes sense.
   - Create new plans that should be completed in future into Codex CLI's `/plan/backlog/` directory so that we don't forget to get round to them at some point in the future. Prior to creating new tasks, always ask if its OK to create the new tasks. It's important to confirm that the user agrees with what to add to the backlog prior to adding stuff to the backlog.


## Notes

- If Codex CLI's /plan directory or any subdirectories don't exist, CREATE THEM IMMEDIATELY (eg `/plan/`, `/plan/backlog/`, `/plan/current/`, `/plan/complete/`, `/plan/experiments/`, `/plan/artifacts/`, `/plan/scratch/`, `/plan/KNOWLEDGE.md`)
- **ABSOLUTE RULE**: NO Codex CLI temporary files, test scripts, experiments, or artifacts should EVER be created outside of Codex CLI's /plan/
- **ENFORCEMENT**: This is a CRITICAL rule - violation of Codex CLI's /plan directory rule is a serious error
- **REMINDER**: Always adhere to Codex CLI's /plan directory rule — use /plan for Codex CLI's work; keep user's main workspace clean
- **USER SPACE PROTECTION**: The main workspace is reserved for the user's actual project files, not Codex CLI's working files

==========


here is the plan markdown/task: $ARGUMENTS
