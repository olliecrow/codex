---
name: verify
description: Verify correctness of recent code changes, decisions, plans, or outputs by running checks/tests and gathering evidence. Use when the user asks to confirm, validate, double-check, or prove that recent work (including plans) is correct, complete, or meets requirements, especially after edits, bug fixes, refactors, or discussions.
---

# Verify

## Overview

Verify recent work by collecting evidence that it is correct, complete, and matches requirements, prioritizing targeted checks over broad stress testing unless risk demands it.

When a current plan is the subject, use **plan verification mode**: review, critique, and refine the plan; run small investigations if needed; then return a fresh, improved plan.

## Workflow

### 1) Establish scope and criteria

- Identify the recent changes or claims to verify.
- Extract acceptance criteria, expected behavior, invariants, and risk areas.
- Ask minimal clarifying questions only when requirements are ambiguous.
- Note what would constitute proof of correctness vs. "good enough."
- If verifying a plan: capture the current plan, its goals, constraints, and why it is being proposed now.

### 2) Plan verification probes

- Map each criterion to a concrete check (tests, manual steps, logs, queries, static analysis).
- Prefer fast, focused probes first; include regression checks around touched areas.
- If basics fail, stop early and fix before scaling the verification effort.
- Keep a lightweight verification log in `plan/verify.md` (untracked) with probes and outcomes.
- Track a minimal verification matrix of configs/perspectives already covered to avoid repeats.
- Use `plan/` as scratch space for ad-hoc experiments; remove any that are no longer needed.
- Keep `plan/` untracked and never commit it.

### 2b) Plan verification mode (when the subject is a plan)

- Review the plan for completeness, ordering, dependencies, and feasibility.
- Challenge assumptions against prior conversation context and known constraints.
- Identify missing steps, risky leaps, vague items, or unclear ownership/exit criteria.
- Run small investigations or experiments when they materially reduce uncertainty.
- Produce a refreshed plan with explicit steps, dependencies, and verification points.

### 3) Execute and gather evidence

- Run the smallest checks that validate each claim.
- Add targeted tests or reproducible steps when gaps exist.
- Create small, isolated experiments or standalone tests when they give clearer evidence.
- Record commands, configs, and results in the verification log.
- After any fixes, re-run the smallest relevant probes to confirm no regression.

### 4) Evaluate and close gaps

- Compare outcomes to criteria; mark verified, failed, or unknown.
- If unknown, design an additional probe or request missing context.
- If failures appear and the user wants fixes, fix and re-run relevant probes.

### 5) Report

- Summarize verified items, remaining risks, and confidence level.
- Call out critical red flags and any regressions introduced during verification.
- List evidence (tests run, steps, outputs, artifacts).
- Note follow-up items and any limitations.
- If plan verification mode was used, include the refreshed plan as a full replacement copy.

## Repeat invocations

- Avoid repeating the same probes; add new perspectives or deeper edge cases.
- Update the verification log and carry forward unresolved items.
- Re-run the minimal subset needed to confirm no regression when new changes land.
- Expand only as needed: vary configs, environments, or perspectives when risk warrants it.
- If re-invoked, follow prior suggested next steps or take a fresh angle; both are acceptable.
