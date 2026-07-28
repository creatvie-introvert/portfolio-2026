# PROMPTS.md

# Codex Prompt Library

This document contains reusable prompts for working on the Portfolio 2026 project.

These prompts are designed to be copied directly into Codex.

---

# 1. Task Planning

Inspect the existing implementation.

Do **not** edit any files.

Provide:

1. Current behaviour
2. Root cause (or likely cause)
3. Files involved
4. Proposed implementation
5. Tests required
6. Risks or edge cases
7. Documentation likely to require updates
8. Proposed implementation outline

Wait for approval before making changes.

---

# 2. Task Implementation

The proposed implementation is approved.

Apply only the agreed changes.

Requirements:

- Keep changes as small as possible.
- Preserve existing behaviour unless the task explicitly changes it.
- Avoid unrelated refactoring.
- Follow existing project conventions.
- Add or update regression tests where appropriate.
- Do not update documentation yet.
- Do not commit or push.

After implementation provide:

- Files changed
- Summary of changes
- Tests added or updated
- Diff summary
- Manual QA required

---

# 3. Documentation Review

The implementation is complete.

Review whether documentation should be updated.

Review:

- CHANGELOG.md
- TASKS.md
- PROJECT.md
- TESTING.md
- AGENTS.md
- PROMPTS.md
- README.md

Only update documentation genuinely affected by the completed task.

Provide:

1. Documentation summary
2. Files requiring updates
3. Files that do not require updates
4. Proposed diffs

Wait for approval before editing.

Do not commit or push.

---

# 4. Task Completion

Implementation, testing and documentation are complete.

Before preparing a commit:

Run:

```bash
env -u DEBUG .venv/bin/python manage.py check
env -u DEBUG .venv/bin/python manage.py test
git diff --check
```

Then:

1. Review the complete working tree.
2. Confirm there are no unrelated changes.
3. Confirm there are no secrets.
4. Confirm there are no database files.
5. Confirm there are no backup files.
6. Confirm there are no generated files.
7. Stage only the intended files.
8. Show:

- validation results
- git status
- staged diff summary
- proposed Conventional Commit message

Wait for approval before committing.

Never commit or push without explicit approval.

---

# 5. Refactor

Improve readability and maintainability without changing behaviour.

Requirements:

- No functional changes.
- Preserve all tests.
- Reduce duplication where appropriate.
- Improve naming if beneficial.
- Do not introduce unnecessary abstraction.

Provide a summary before making changes.

Wait for approval.

---

# 6. Accessibility Audit

Audit the implementation against WCAG best practices.

Review:

- Keyboard navigation
- Focus order
- Focus visibility
- Semantic HTML
- Colour contrast
- Screen reader support
- Skip links
- ARIA usage

Provide:

- Issues found
- Severity
- Recommended fixes

Do not edit code until approval.

---

# 7. Performance Audit

Audit this page for performance.

Review:

- CSS
- JavaScript
- Images
- Rendering
- Network requests
- Layout shifts
- Unnecessary DOM updates

Recommend improvements before implementation.

Wait for approval.

---

# 8. CSS Bug Investigation

Investigate this layout issue.

Requirements:

- Preserve desktop behaviour.
- Fix mobile only unless instructed otherwise.
- Explain the root cause.
- Identify affected CSS.
- Propose the smallest appropriate fix.

Wait for approval.

---

# 9. Django Investigation

Inspect this Django feature.

Explain:

- Current behaviour
- Relevant models
- Views
- URLs
- Templates
- Forms
- Context data
- Database interactions
- Possible improvements

Do not edit code.

Wait for approval.

---

# 10. Code Review

Review the latest implementation.

Look for:

- Bugs
- Edge cases
- Accessibility issues
- Performance issues
- Maintainability
- Security concerns
- Missing tests
- Documentation updates

Do not edit code.

Provide a prioritised review.

---

# 11. Bug Investigation

Investigate the reported bug.

Do not edit code.

Provide:

- Root cause
- Files involved
- Reproduction steps
- Proposed fix
- Risks
- Tests required

Wait for approval.

---

# 12. Feature Planning

Plan the implementation of the following feature.

Do not edit code.

Provide:

- High-level approach
- Architecture impact
- Files affected
- Database changes (if any)
- Testing strategy
- Accessibility considerations
- Documentation updates required
- Risks
- Implementation phases

Wait for approval.

---

# Prompt Usage

Most development tasks should follow this sequence:

1. Task Planning
2. Task Implementation
3. Documentation Review
4. Task Completion

Use the remaining prompts only when they are appropriate for the task.