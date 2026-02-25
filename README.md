# codex

`codex` is a working repository for a hardened Codex CLI container plus reusable skills and agent-oriented automation docs.

## Project Aim

Provide a reproducible local runtime for Codex-driven development loops:

- run Codex in an isolated container against arbitrary project directories
- keep reusable skills versioned and composable
- maintain durable automation guidance in repo docs

## What This Repository Does

- builds and runs a Codex CLI container (`container/`)
- ships reusable skills (`skills/`) for planning, verification, git workflows, investigations, and more
- stores long-lived automation docs and decisions (`docs/`)

## Requirements

- Docker
- internet access for image build/package retrieval
- local Codex authentication state (for example `~/.codex/auth.json`)

## Authentication

The container run scripts copy/use local Codex auth state. Ensure you are authenticated locally before first run.

## Quick Start

Build the container image:

```bash
./container/build.sh
```

Run Codex against a target project:

```bash
./container/run.sh /path/to/project
```

Run with an interactive shell instead of the Codex TUI:

```bash
./container/run.sh /path/to/project --shell
```

## Getting Started

1. Build the image.
2. Launch against a target repository/workspace.
3. Validate container sanity (write access to `/workspace`, expected network behavior, git restrictions inside container).
4. Iterate using repo skills and docs as workflow guidance.

## Local State and Directory Layout

- `container/`: Docker image, run scripts, and runtime helpers
- `skills/`: versioned Codex skills loaded by user skill symlink setup
- `docs/`: long-lived documentation and decision records
- `plan/`: short-lived scratch space (not for commits)
- `codex_docs.md`: local copy of Codex documentation
- `AGENTS.md`: repository operating policy for agent workflows

## Logging and Debugging

- container runtime output is emitted to terminal by run scripts
- for runtime debugging, launch with `--shell` and inspect environment directly
- for skills changes, run the local skills validator before publishing updates

## Documentation Map

- `README.md`: human-facing project orientation
- `AGENTS.md`: agent operating guidelines and repository policy
- `container/README.md`: container-specific behavior and security model
- `docs/workflows.md`: workflow conventions
- `docs/decisions.md`: durable rationale and decisions
- `docs/skills.md`: skill maintenance and validation guidance
