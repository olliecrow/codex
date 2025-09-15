# Codex CLI Container
# Purpose: run Codex CLI fully autonomously in a sandboxed Docker environment
# with internet access and write access limited to the mounted project and
# mounted Codex config directory. Git usage is blocked via multiple layers.

FROM debian:stable-slim

# Core/optional build tools for compiling native extensions
# By default, include the core toolchain needed for building Python/Rust extensions
ARG INCLUDE_BUILD_TOOLS=1
ARG INCLUDE_EXTRA_TOOLS=1

# 1) Base packages and tini
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        procps \
        lsof \
        bash \
        tini; \
    rm -rf /var/lib/apt/lists/*

# 2) Deny installing git via apt (defense-in-depth)
RUN set -eux; \
    mkdir -p /etc/apt/preferences.d; \
    printf 'Package: git*\nPin: release *\nPin-Priority: -1\n' > /etc/apt/preferences.d/deny-git

# 3) Install Node.js LTS (22.x) from NodeSource
RUN set -eux; \
    ARCH=$(dpkg --print-architecture); \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /usr/share/keyrings/nodesource.gpg; \
    echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" > /etc/apt/sources.list.d/nodesource.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends nodejs; \
    rm -rf /var/lib/apt/lists/*

# 3b) Core toolchain for native builds (keeps Git blocked)
# Includes GCC toolchain, binutils, pkg-config, CMake, Ninja, and Python headers
RUN set -eux; \
    if [ "$INCLUDE_BUILD_TOOLS" = "1" ]; then \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            build-essential \
            binutils \
            pkg-config \
            cmake \
            ninja-build \
            python3-dev; \
        rm -rf /var/lib/apt/lists/*; \
    fi

# 3c) Optional extras for performance/debugging/packaging and plotting build deps
RUN set -eux; \
    if [ "$INCLUDE_EXTRA_TOOLS" = "1" ]; then \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            clang \
            lld \
            ccache \
            gdb \
            valgrind \
            patchelf \
            wget \
            unzip \
            libfreetype6-dev \
            libpng-dev \
            libgomp1 \
            libstdc++6; \
        rm -rf /var/lib/apt/lists/*; \
    fi

# 4) Install Codex CLI from npm
RUN set -eux; \
    npm install -g @openai/codex; \
    npm cache clean --force

# 5) Create non-root user
RUN set -eux; \
    groupadd -g 1000 dev && useradd -m -u 1000 -g 1000 -s /bin/bash dev

# 6) Environment for Codex and Rust
ENV CODEX_HOME=/home/dev/.codex \
    NODE_OPTIONS=--unhandled-rejections=strict \
    PATH=/home/dev/.cargo/bin:$PATH

# 7) Block git/gh/git-lfs via wrapper scripts (extra defense)
RUN set -eux; \
    echo '#!/bin/sh\necho "git is disabled in this container" >&2; exit 127' > /usr/local/bin/git && chmod +x /usr/local/bin/git; \
    echo '#!/bin/sh\necho "git-lfs is disabled in this container" >&2; exit 127' > /usr/local/bin/git-lfs && chmod +x /usr/local/bin/git-lfs; \
    echo '#!/bin/sh\necho "GitHub CLI (gh) is disabled in this container" >&2; exit 127' > /usr/local/bin/gh && chmod +x /usr/local/bin/gh

# 8) Optional: avoid noisy bells; provide a simple notifier noop
RUN set -eux; echo '#!/bin/sh' > /usr/local/bin/afplay && chmod +x /usr/local/bin/afplay

USER dev

# 9) Install Rust toolchain via rustup for non-root user
RUN set -eux; \
    curl -fsSL https://sh.rustup.rs | sh -s -- -y; \
    /home/dev/.cargo/bin/rustup toolchain install stable

WORKDIR /workspace

# 10) Healthcheck is a no-op (Codex runs via exec)
HEALTHCHECK NONE

ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["bash"]
