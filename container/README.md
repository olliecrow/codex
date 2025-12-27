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
- Codex CLI is installed from npm at build time using `@openai/codex@latest`, so each build pulls the newest published version.
- Codex is launched with `--dangerously-bypass-approvals-and-sandbox` plus config overrides (`approval_policy=never`, `sandbox_mode=danger-full-access`, `model=gpt-5.2-codex`, `model_reasoning_effort=xhigh`) so it never prompts for approvals and always uses the latest Codex model with extra-high reasoning.

## Security model

- Only two host mounts are exposed: the project directory and `~/.codex`.
- No Git installed; apt installation is hard‑blocked; `git`, `git-lfs`, and `gh` commands are wrapped to fail with an explicit message.
- Container runs as non‑root user `dev` with uid/gid 1000.

## Defaults

- Model: `gpt-5.2-codex`
- Reasoning effort: `xhigh`

You can override defaults in your `~/.codex/config.toml` or using `--config` flags if you exec into the container and run Codex manually.

## Environment setup (Python/Rust)

If you run component tests or training that use Python with `uv` and native extensions, you may hit build failures (e.g., `tinyscaler`, pulled in by `supersuit`) due to the lack of a system C compiler in the minimal image.

Included by default:
- Core native toolchain: `build-essential`, `binutils`, `pkg-config`, `cmake`, `ninja-build`, `python3-dev`
- Rust toolchain via `rustup` for user `dev` (stable installed; cargo/rustc available on PATH)
- uv CLI preinstalled (on PATH)
- Runtime libs and tools: `libgl1`, `libglib2.0-0`, `patchelf`, `ffmpeg`, `ripgrep`, `sccache`
- Extras: `clang`, `lld`, `ccache`, `gdb`, `valgrind`, `wget`, `unzip`, `libfreetype6-dev`, `libpng-dev`, `libgomp1`

Verification inside the container shell:
```
cc --version && g++ --version && ld --version
pkg-config --version && cmake --version && ninja --version
rustc --version && cargo --version
uv --version
```

Then from the repo root:
```
./setup_env.sh
```

Notes:
- Security posture unchanged: no additional host mounts; Git remains blocked via APT pin and command wrappers; `.git` still mounted read‑only.
- Default env: `PATH=/home/dev/.cargo/bin:$PATH`, `UV_LINK_MODE=copy`, `UV_PYTHON_PREFERENCE=managed`
