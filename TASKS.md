# Portfolio Development Backlog

This file tracks all development work for the Portfolio 2026 project.

Workflow for every task:

1. Add a new task to the **Ready** section.
2. Ask Codex to inspect the task only.
3. Review the proposed solution.
4. Approve the implementation.
5. Test using `TESTING.md`.
6. Mark the task as complete.
7. Commit the changes.
8. Move the completed task to the **Completed** section.

---

# Ready

No tasks currently.

---

# In Progress

No tasks currently.

---

# Blocked

No blocked tasks.

---

# Completed

## Task 001

### Title

Fix mobile overflow in contact section

### Status

✅ Complete

### Priority

High

---

### Problem

On a real iPhone, the contact information cards and contact form fields extended beyond the right edge of the viewport, creating horizontal scrolling.

---

### Acceptance Criteria

- [x] No horizontal scrolling from 320px upwards
- [x] Contact information cards fit within the viewport
- [x] Contact form fields fit within the viewport
- [x] Long email addresses wrap safely
- [x] Existing visual design preserved
- [x] Desktop layout unchanged
- [x] Tested on a real iPhone
- [x] `python manage.py check` passes

---

### Root Cause

The long unbroken email address created an intrinsic minimum width inside the contact grid.

Because grid and flex children retained their default `min-width: auto`, the grid expanded beyond the available viewport width. The contact form then expanded to match the oversized grid track.

A mobile media query also increased the contact grid padding below 390px, reducing the available content width.

---

### Solution

Implemented a CSS-only fix.

Changes included:

- Added `min-width: 0` to the relevant contact layout elements.
- Added safe wrapping for email addresses.
- Restored 16px mobile padding for the contact grid.
- No template changes required.

---

### Files Changed

```
core/static/core/css/style.css
```

---

### Testing

#### Automated

- ✅ `DEBUG=True .venv/bin/python manage.py check`
- ✅ `git diff --check`

Result:

```
System check identified no issues (0 silenced).
```

#### Manual

Completed successfully on:

- ✅ Chrome Desktop
- ✅ Safari Desktop
- ✅ Real iPhone
- ✅ 320px
- ✅ 375px
- ✅ 390px
- ✅ 430px
- ✅ 768px
- ✅ 1024px
- ✅ Desktop
- ✅ Light Mode
- ✅ Dark Mode

---

### Lessons Learned

The CSS implementation was correct.

Safari/iPhone cached the stylesheet after the changes.

Clearing the browser cache loaded the updated stylesheet and resolved the apparent issue.

Future CSS testing should always include a hard refresh or cache clear before assuming the implementation has failed.

---

### Completed

27 July 2026

---

## Future Tasks

- Review overall visual polish
- Improve project case studies
- Improve homepage copy
- Accessibility audit
- Lighthouse performance improvements