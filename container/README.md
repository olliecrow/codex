# Codex CLI Container

A minimal Docker setup to run Codex CLI fully autonomously with internet access and host isolation.

- Autonomy: no approval prompts; no OS sandbox (uses Docker isolation)
- Host mounts: project directory at `/workspace` and host Codex config at `/home/dev/.codex`
- Git disabled: not installed, APT‑pinned, and wrapped to fail fast. `.git` mounted read‑only

## Build

From the repository root (always fresh, no cache):

```
./container/build.sh
```

## Run

Interactive Codex session against a project:

```
./container/run.sh /path/to/project
```

Get a shell in the container:

```
./container/run.sh /path/to/project --shell
```

Notes:
- Ensure you have authenticated locally so that `~/.codex/auth.json` exists. The container mounts this directory for auth/config/history.
- `.git` is mounted read‑only to prevent repository mutations from inside the container.
- Codex is launched with `--dangerously-bypass-approvals-and-sandbox` and `approval_policy=never` so it never prompts for approvals.

## Security model

- Only two host mounts are exposed: the project directory and `~/.codex`.
- No Git installed; apt installation is hard‑blocked; `git`, `git-lfs`, and `gh` commands are wrapped to fail with an explicit message.
- Container runs as non‑root user `dev` with uid/gid 1000.

## Defaults

- Model: `gpt-5`
- Reasoning effort: `high`

You can override defaults in your `~/.codex/config.toml` or using `--config` flags if you exec into the container and run Codex manually.

## Environment setup (Python/uv)

If you run component tests or training that use Python with `uv` and native extensions, you may hit build failures (e.g., `tinyscaler`, pulled in by `supersuit`) due to the lack of a system C compiler in the minimal image.

Options:
- Option A (recommended when building locally): include a build toolchain in the image so `uv` can compile native deps, then run your project setup (e.g., `./setup_env.sh`).
  - Build with toolchain: `./container/build.sh --with-toolchain`
  - This installs `build-essential` and `pkg-config` only. Git remains blocked via APT pin and wrapper scripts, and `.git/` stays mounted read‑only.
- Option B: if `supersuit` is not actually used, remove it from your dependencies in a future refactor to avoid pulling `tinyscaler` entirely.

Notes:
- The toolchain option does not relax security constraints. No additional host mounts are added; the Git APT pin and command wrappers still prevent Git usage; and the `.git` directory is still mounted read‑only at runtime.
