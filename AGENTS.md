# AGENTS.md

## Project

This repository contains the source code for Leanne Bedeau-Rogers' professional portfolio website.

The purpose of the site is to demonstrate professional full-stack development skills while providing an excellent user experience across desktop, tablet and mobile devices.

---

# Primary Goal

Improve the portfolio without introducing regressions.

Every change should make the project:

- Cleaner
- Faster
- More accessible
- Easier to maintain
- More professional

---

# Technology

- Python 3.12
- Django 6
- HTML5
- CSS3
- JavaScript
- SQLite (local)
- PostgreSQL (production)
- Cloudinary
- WhiteNoise

---

# Development Rules

Always inspect the existing implementation before proposing changes.

Never redesign unrelated parts of the application.

Work on ONE task at a time.

Keep edits as small as possible.

Explain your reasoning before editing.

After making changes explain:

- Root cause
- Files changed
- Why those files changed
- Risks
- Manual testing required

---

# Git Rules

Never:

- switch branches
- push
- commit
- deploy
- rewrite Git history

unless explicitly instructed.

---

# Database Rules

Never create migrations automatically.

Instead run

python manage.py makemigrations --dry-run --verbosity 3

and report the proposed migration.

Wait for approval.

---

# Deployment

Never deploy.

Never modify production settings.

Never modify secrets inside .env.

---

# Code Style

Prefer:

- readable code
- reusable components
- responsive layouts
- semantic HTML
- accessibility
- maintainability

Avoid:

- duplicated code
- unnecessary dependencies
- magic numbers
- fixed widths on responsive layouts

---

# CSS Rules

Desktop layouts must not regress.

Always test:

320px

375px

390px

430px

768px

1024px

Desktop

Never introduce horizontal scrolling.

---

# Response Format

After completing work always provide:

## Summary

## Root Cause

## Files Changed

## Tests Performed

## Manual Testing Required

## Suggested Next Task