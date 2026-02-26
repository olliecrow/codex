# codex

`codex` is a working repository for a Codex CLI container plus reusable skills and automation docs.

## What this project is trying to achieve

Give you a repeatable local runtime for Codex driven development.

## What you experience as a user

1. You build the Codex container once.
2. You run it against any local project path.
3. You reuse versioned skills for planning, verification, and git workflows.
4. You use docs in this repo to keep workflows consistent.

## Quick start

Build the container image.

```bash
./container/build.sh
```

Run Codex against a target project.

```bash
./container/run.sh /path/to/project
```

Run with an interactive shell.

```bash
./container/run.sh /path/to/project --shell
```

Run a quick preflight check before long sessions.

```bash
./container/doctor.sh
```

Preview exactly what will run without starting Docker.

```bash
./container/dry_run.sh /path/to/project
./container/dry_run.sh /path/to/project --shell
```

## Example output

Doctor summary.

```text
codex container doctor
[ok] tool docker: /usr/local/bin/docker
[ok] host codex auth: /Users/you/.codex/auth.json
doctor result: PASS
```

Dry-run summary.

```text
codex container dry-run
repo: /path/to/project
mode: codex tui
planned sequence:
1. Validate local prerequisites.
2. Start detached container and mounts.
3. Write container config.
4. Launch Codex.
5. Remove container on exit.
dry-run only: no Docker commands were executed.
```

## Requirements

- Docker
- internet access for image build and package retrieval
- local Codex authentication state, for example `~/.codex/auth.json`

## Authentication

Run scripts use your local Codex auth state.
Authenticate locally before first run.

## Helpful tips

- Use `--shell` when you need to inspect the runtime environment directly.
- Run local skill validation checks before publishing skill changes.

## Directory layout

- `container/`: Docker image, run scripts, and runtime helpers
- `skills/`: versioned Codex skills
- `docs/`: long-lived documentation and decisions
- `plan/`: short lived scratch notes
- `AGENTS.md`: repository operating policy

## Documentation map

- `README.md`: human-facing project orientation
- `AGENTS.md`: agent operating guidelines and repo policy
- `container/README.md`: container behavior and security model
- `docs/workflows.md`: workflow conventions
- `docs/decisions.md`: durable rationale and decisions
- `docs/skills.md`: skill maintenance and validation guidance
- `docs/project-preferences.md`: durable project maintenance preferences
