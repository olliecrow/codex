# Entrypoints and Auto-Run Checklist

Use this to locate execution surfaces. Open each file and review scripts and hooks.

## General

- CI/CD: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `circleci/config.yml`, `buildkite/*`, `.buildkite/*`, `Jenkinsfile`, `.travis.yml`.
- Containers: `Dockerfile*`, `docker-compose*.yml`, `devcontainer.json`, `.devcontainer/*`.
- Scripts: `scripts/`, `bin/`, `tools/`, `install/`, `setup/`, `hack/`.
- Git hooks and hook managers: `.git/hooks/*` (if present), `.husky/*`, `lefthook.yml`, `.lefthook.yml`, `pre-commit` configs.
- Editor/IDE tasks: `.vscode/tasks.json`, `.vscode/extensions.json`, `.idea/`, `.run/`.
- Shell auto-run: `.envrc`, `.direnv/`, `.tool-versions`, `.mise.toml`.
- Build orchestrators: `Makefile`, `CMakeLists.txt`, `Taskfile.yml`, `justfile`.

## Node.js / JS

- `package.json` scripts (especially `preinstall`, `install`, `postinstall`, `prepare`, `prepack`, `postpack`, `prepublish*`).
- `.npmrc`, `.yarnrc`, `.yarnrc.yml`, `.pnpmfile.cjs`, `pnpm-workspace.yaml`.
- `binding.gyp`, `node-gyp` configs, `prebuild*` scripts.

## Python

- `pyproject.toml` (`[build-system]`, custom build backend).
- `setup.py`, `setup.cfg` (`cmdclass`, `entry_points`, custom build steps).
- `requirements*.txt`, `Pipfile`, `Pipfile.lock`, `poetry.lock`, `tox.ini`, `noxfile.py`.
- `pip.conf`, `pip.ini` for custom indexes or trusted hosts.
- Task runners: `tasks.py` (invoke), `fabfile.py`.

## Ruby

- `Gemfile`, `Gemfile.lock`, `*.gemspec`.
- `Rakefile`, `extconf.rb` (native extensions).

## Go

- `go.mod`, `go.sum`, `Makefile`.
- `//go:generate` directives in source.
- `magefile.go`.

## Rust

- `Cargo.toml` (`build = "build.rs"`, `build-dependencies`).
- `build.rs`.
- `.cargo/config.toml`.

## Java / JVM

- `pom.xml`, `build.gradle`, `settings.gradle`, `gradle.properties`.
- `mvnw`, `gradlew` scripts.

## .NET

- `*.csproj`, `Directory.Build.props`, `Directory.Build.targets`.
- `build.ps1`, `build.sh`.

## PHP

- `composer.json` scripts, `composer.lock`.

## Shell / PowerShell

- `*.sh`, `*.bash`, `*.zsh`, `*.ps1`, `*.cmd`, `*.bat` in `scripts/` or root.
