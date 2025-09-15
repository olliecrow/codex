# Codex CLI Container
# Purpose: run Codex CLI fully autonomously in a sandboxed Docker environment
# with internet access and write access limited to the mounted project and
# mounted Codex config directory. Git usage is blocked via multiple layers.

FROM debian:stable-slim

# Optional build tools for compiling native extensions
ARG INCLUDE_BUILD_TOOLS=0

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

# 3b) Optionally install C/C++ build toolchain (keeps Git blocked)
RUN set -eux; \
    if [ "$INCLUDE_BUILD_TOOLS" = "1" ]; then \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            build-essential \
            pkg-config; \
        rm -rf /var/lib/apt/lists/*; \
    fi

# 4) Install Codex CLI from npm
RUN set -eux; \
    npm install -g @openai/codex; \
    npm cache clean --force

# 5) Create non-root user
RUN set -eux; \
    groupadd -g 1000 dev && useradd -m -u 1000 -g 1000 -s /bin/bash dev

# 6) Environment for Codex
ENV CODEX_HOME=/home/dev/.codex \
    NODE_OPTIONS=--unhandled-rejections=strict

# 7) Block git/gh/git-lfs via wrapper scripts (extra defense)
RUN set -eux; \
    echo '#!/bin/sh\necho "git is disabled in this container" >&2; exit 127' > /usr/local/bin/git && chmod +x /usr/local/bin/git; \
    echo '#!/bin/sh\necho "git-lfs is disabled in this container" >&2; exit 127' > /usr/local/bin/git-lfs && chmod +x /usr/local/bin/git-lfs; \
    echo '#!/bin/sh\necho "GitHub CLI (gh) is disabled in this container" >&2; exit 127' > /usr/local/bin/gh && chmod +x /usr/local/bin/gh

# 8) Optional: avoid noisy bells; provide a simple notifier noop
RUN set -eux; echo '#!/bin/sh' > /usr/local/bin/afplay && chmod +x /usr/local/bin/afplay

USER dev
WORKDIR /workspace

# 9) Healthcheck is a no-op (Codex runs via exec)
HEALTHCHECK NONE

ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["bash"]
