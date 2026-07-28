# AGENTS.md

# Portfolio 2026 — AI Development Guide

This document defines how AI coding agents (Codex, ChatGPT and future agents) should work on this repository.

The goal is to produce production-quality code through small, well-tested, well-documented changes.

---

# Core Principles

Always favour:

- Simplicity
- Readability
- Accessibility
- Maintainability
- Small focused commits
- Incremental improvements

Never introduce unnecessary complexity.

If a task can be completed with a simple solution, prefer that over a more clever one.

---

# General Rules

Before making any code changes:

- Understand the existing implementation.
- Understand the reason the current code behaves as it does.
- Preserve existing behaviour unless the task explicitly changes it.
- Minimise the size of each change.
- Avoid unrelated refactoring.

If unsure, ask rather than guess.

---

# Code Quality Standards

All code should:

- Follow existing project conventions.
- Be readable.
- Be self-explanatory where possible.
- Avoid duplication.
- Prefer reusable components.
- Avoid premature optimisation.

---

# Accessibility Standards

Accessibility is a core project requirement.

Every implementation should consider:

- Keyboard navigation
- Visible focus states
- Semantic HTML
- Screen readers
- Colour contrast
- Skip links
- Appropriate ARIA usage where required

Accessibility regressions are considered bugs.

---

# Testing Standards

Where practical:

- Add automated regression tests.
- Avoid reducing existing test coverage.
- Preserve existing behaviour.

After implementation run:

```bash
env -u DEBUG .venv/bin/python manage.py check
env -u DEBUG .venv/bin/python manage.py test
git diff --check
```

The `env -u DEBUG` wrapper is used only because the Codex execution environment injects `DEBUG=release` into subprocesses.

Do not modify:

- `.env`
- `config/settings.py`
- environment precedence

to work around this behaviour.

---

# Documentation Standards

Documentation is part of every completed task.

Review whether the following files require updating:

- CHANGELOG.md
- TASKS.md
- PROJECT.md
- TESTING.md
- AGENTS.md
- PROMPTS.md
- README.md

Only update files genuinely affected by the task.

Do not duplicate information across documentation.

---

# Task Workflow

Every task follows the same workflow.

## Phase 1 — Investigation

Before editing any files:

- Inspect the existing implementation.
- Understand the current behaviour.
- Identify the root cause.
- Identify affected files.
- Identify tests required.
- Identify documentation likely to change.

Produce:

- implementation summary
- risks
- proposed approach

Wait for approval.

---

## Phase 2 — Implementation

After approval:

- Apply only the agreed changes.
- Preserve existing behaviour.
- Avoid unrelated refactoring.
- Keep changes focused.
- Update or add regression tests where appropriate.

Do not commit.

---

## Phase 3 — Validation

Run:

```bash
env -u DEBUG .venv/bin/python manage.py check
env -u DEBUG .venv/bin/python manage.py test
git diff --check
```

If validation fails:

- Stop.
- Report the exact command.
- Report the exact error.
- Investigate the cause.
- Do not continue.

Never hide errors.

---

## Phase 4 — Manual QA

Provide a concise checklist describing:

- expected behaviour
- edge cases
- accessibility checks
- browser behaviour (if applicable)

Wait for confirmation before preparing a commit.

---

## Phase 5 — Documentation Review

Review whether documentation needs updating.

Possible files:

- CHANGELOG.md
- TASKS.md
- PROJECT.md
- TESTING.md
- AGENTS.md
- PROMPTS.md
- README.md

Before editing:

Provide:

1. Documentation summary
2. Files requiring updates
3. Files not requiring updates
4. Proposed diffs

Wait for approval.

---

## Phase 6 — Commit Preparation

Before committing:

Review the complete working tree.

Confirm:

- no secrets
- no database files
- no backup files
- no generated files
- no unrelated edits

Show:

```bash
git status
```

Provide:

- staged file summary
- validation summary
- proposed Conventional Commit message

Wait for approval.

---

## Phase 7 — Commit

Only commit after explicit approval.

Never commit automatically.

---

## Phase 8 — Push

Only push after explicit approval.

Never push automatically.

After pushing provide:

- branch name
- commit hash
- commit message
- confirmation that the repository is clean

---

# Conventional Commits

Prefer:

```
feat:
fix:
refactor:
docs:
style:
test:
build:
ci:
perf:
```

Examples:

```
fix(accessibility): implement proper skip link navigation

feat(projects): add case study filtering

docs: update testing workflow

refactor(core): simplify navigation component
```

---

# Things To Avoid

Never:

- rewrite unrelated code
- rename files unnecessarily
- introduce breaking changes
- remove tests without good reason
- commit secrets
- commit databases
- commit backup files
- commit generated artefacts

---

# Definition of Done

A task is complete only when:

✓ Implementation finished

✓ Automated tests pass

✓ Manual QA completed

✓ Documentation updated where required

✓ Validation completed

✓ No unrelated changes remain

✓ Commit approved

✓ Push approved

Anything less is work in progress.