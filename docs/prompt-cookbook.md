# Prompt Cookbook

Reusable copy-paste prompt templates for high-frequency workflows in this repository.

## Session bootstrap

- `[$setup] and [$prime]. then [$git-sync] sync current branch with upstream (ff-only).`

## Git sync

- `[$git-sync] sync current branch with upstream (ff-only) and verify branch/upstream/ahead-behind.`
- `[$git-sync] pull most recent remote main (ff-only) and report new HEAD commit.`
- `[$git-sync] sync explicit branch olliecrow/<branch-name> to latest remote state (ff-only).`

## Git review

- `[$git-review] full branch review vs main for critical red flags and serious issues. findings first by severity.`
- `[$git-review] scoped review: <area> + boundary files only. focus on critical red flags/serious issues first.`
- `[$git-review] scoped review: <area>; explicitly list out-of-scope files not reviewed.`

## Cluster checks

- `[$cluster-check] quick-status: per-node cpu/gpu usage, queue counts by state, and qos values with timestamp.`
- `[$cluster-check] quick-status: are all jobs finished for current project/user? include state counts.`
- `[$cluster-check] deep-check: analyze recent batch end-to-end (logs, outputs, sync integrity, root causes).`

## Competition submission checks

- `[$competition-submit-check] ammchallenge capability-check. verify auth and submit-flow readiness; stop before irreversible submit.`
- `[$competition-submit-check] highload capability-check with can-submit/blocked verdict and checkpoint evidence.`
- `[$competition-submit-check] ammchallenge submit-now using <artifact-path>; return submission receipt/id.`

## Milestone checkpoint

- `[$checkpoint] run docs promotion + small logical commits for work completed so far.`
- `[$checkpoint] milestone checkpoint now: organise durable findings, then commit verified changes.`
