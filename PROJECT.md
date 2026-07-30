# PROJECT.md

# Portfolio 2026

## Project Overview

Portfolio 2026 is my personal portfolio website, built to showcase my skills, projects and experience as a Full Stack Developer.

The project serves three primary purposes:

- Demonstrate technical ability to potential employers.
- Generate freelance opportunities.
- Provide a platform to experiment with modern web development practices and AI-assisted development.

The project prioritises quality over speed. Every change should improve the project while keeping the codebase simple, accessible and maintainable.

---

# Project Goals

## Primary Goals

- Showcase development projects professionally.
- Demonstrate front-end and back-end skills.
- Maintain excellent accessibility and performance.
- Create an enjoyable user experience on every device.
- Build a portfolio that reflects production-quality development practices.

## Technical Goals

- Responsive across all supported screen sizes.
- Accessible using WCAG best practices.
- High Lighthouse scores.
- Reusable components.
- Clean architecture.
- Comprehensive documentation.
- Easy to extend and maintain.

---

# Technology Stack

## Backend

- Python
- Django

## Frontend

- HTML5
- CSS3
- JavaScript

## Development

- Git
- GitHub
- Visual Studio Code
- Python Virtual Environment

---

# Development Workflow

Every development task follows the same lifecycle.

## 1. Planning

- Define the task in `TASKS.md`.
- Understand the current behaviour.
- Identify the root cause.
- Review affected files.
- Define acceptance criteria.

No implementation begins until the task is understood.

---

## 2. Investigation

Codex should inspect the existing implementation and provide:

- Current behaviour
- Root cause
- Files involved
- Proposed solution
- Tests required
- Documentation likely to require updates

Wait for approval before editing.

---

## 3. Implementation

After approval:

- Apply only the agreed changes.
- Keep changes as small as possible.
- Preserve existing behaviour unless intentionally changing it.
- Avoid unrelated refactoring.
- Add regression tests where appropriate.

---

## 4. Validation

Before a task is considered complete:

- Run Django system checks.
- Run automated tests.
- Check for whitespace errors.
- Complete manual QA.
- Verify responsive layouts.
- Verify accessibility.
- Confirm existing functionality still works.

---

## 5. Documentation

Review whether the following require updates:

- CHANGELOG.md
- TASKS.md
- PROJECT.md
- TESTING.md
- AGENTS.md
- PROMPTS.md
- README.md

Only update documentation genuinely affected by the completed task.

---

## 6. Git Workflow

Development branch:

`portfolio-v2`

Production branch:

`main`

Workflow:

1. Review completed work.
2. Stage only intended files.
3. Review staged changes.
4. Commit using Conventional Commits.
5. Push to `portfolio-v2`.
6. Merge into `main` after the feature or milestone is complete.

---

# AI Development Workflow

AI assistance is used throughout the project.

### ChatGPT

Responsible for:

- Planning
- Architecture review
- Code review
- Design feedback
- Workflow improvements
- Documentation review

### Codex

Responsible for:

- Repository inspection
- Code implementation
- Regression tests
- Documentation updates
- Validation
- Commit preparation

Codex must never commit or push without explicit approval.

---

# Design Principles

The site should feel:

- Modern
- Minimal
- Professional
- Fast
- Accessible
- Consistent

Avoid unnecessary animations, clutter or decorative effects that do not improve usability.

Every design decision should improve the user experience.

---

# Accessibility Standards

Accessibility is a project requirement, not an optional enhancement.

Every page should support:

- Keyboard navigation
- Visible focus states
- Semantic HTML
- Screen readers
- Sufficient colour contrast

The shared base template must provide:

- A dedicated "Skip to main content" link.
- One unique `main-content` target.
- Navigation links must never reuse the `skip-link` class.

Accessibility regressions should be treated as bugs.

---

# Code Standards

The project prioritises:

- Readability
- Simplicity
- Consistency
- Maintainability

General principles:

- Write self-explanatory code.
- Avoid duplication.
- Prefer reusable solutions.
- Keep files organised.
- Remove dead code.
- Comment only where intent is not obvious.
- Follow existing project conventions.

Form handling:

- Django forms provide authoritative server-side validation.
- Browser validation is progressive enhancement and must not be the only enforcement.
- Invalid submissions should render bound forms with preserved values and accessible errors.
- Spam controls must not interfere with keyboard or assistive-technology users.

---

# Case Study Architecture

`Project` remains the shared catalogue record and `CaseStudy` stores
project-level context.

Reusable case-study narratives use:

- Ordered `CaseStudySection` records for semantic content.
- Ordered `CaseStudyMedia` records attached to individual sections.
- Author-controlled image alt text and optional captions.
- A `use_structured_sections` switch for staged migration from legacy fields.

Legacy fields remain available until each existing case study has been
transferred. Structured sections render only when the switch is enabled and at
least one section contains body text or media.

Case-study templates must preserve semantic headings, omit empty sections, and
render captioned content images with `figure` and `figcaption`.

---

# Motion Architecture

GSAP 3.15.0 and ScrollTrigger are stored as pinned local vendor files and
served through Django static files and WhiteNoise. Pages opt in through the
shared `page_scripts` template block; motion assets must not be loaded globally.

`core/static/core/js/motion.js` is the single owner of site motion. Templates
use semantic `data-motion` hooks rather than presentation classes, and reusable
durations, distances, staggers, easing, and media queries live in one immutable
configuration object.

Motion is progressive enhancement:

- Content remains visible in base HTML and CSS.
- Missing JavaScript, GSAP, or ScrollTrigger must not hide content.
- Animation-added inline styles are cleared after completion and cleanup.
- `gsap.matchMedia()` handles responsive and reduced-motion behaviour.
- Reduced-motion users receive immediately visible, stationary content.

Task 007A animates only the homepage hero. ScrollTrigger is available for
future approved work but no scroll-triggered animation is part of this phase.

Task 007B adds restrained, once-only ScrollTrigger reveals under these
conventions:

- Project introductions use one trigger each.
- Project grids use one trigger for the grid and stagger complete card columns.
- Structured case studies use one trigger per complete semantic section.
- Selectors are scoped to their component root.
- Filters, card internals, and legacy case-study layouts remain static.
- Work always opts into page-level motion assets.
- Case studies opt in only when structured sections are enabled and renderable.

Scroll content remains visible when JavaScript, GSAP, or ScrollTrigger is
unavailable and when reduced motion is enabled. Motion code must not add
hidden-by-default CSS, pinning, scrubbing, batching, or scroll-jacking.

---

# Performance Standards

Target Lighthouse scores:

- Performance: 95+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

Optimise only where there is measurable benefit.

Areas to monitor:

- Images
- CSS
- JavaScript
- Fonts
- Rendering performance

---

# Responsive Support

The website must support:

- 320px
- 375px
- 390px
- 430px
- 768px
- 1024px
- Desktop

Requirements:

- No unintended horizontal scrolling.
- Consistent navigation.
- Readable typography.
- Appropriate spacing.
- Touch-friendly interactions.

---

# Documentation

The project documentation consists of:

| File | Purpose |
|------|---------|
| `README.md` | Project overview and setup |
| `PROJECT.md` | Standards, architecture and workflow |
| `AGENTS.md` | AI development instructions |
| `TASKS.md` | Backlog and completed tasks |
| `TESTING.md` | Automated and manual testing procedures |
| `PROMPTS.md` | Reusable Codex prompt library |
| `CHANGELOG.md` | Developer-facing project history |

Documentation should remain concise, accurate and consistent.

---

# Known Development Environment Notes

When Django management commands are executed through the current Codex runner, the execution environment may inherit an external `DEBUG=release` environment variable.

For Codex validation, run:

```bash
env -u DEBUG .venv/bin/python manage.py check
env -u DEBUG .venv/bin/python manage.py test
git diff --check
```

This workaround applies only to the current Codex execution environment.

Normal local development should continue to use the project's existing `.env` configuration.

---

# Success Criteria

The project is successful if it:

- Demonstrates professional software engineering practices.
- Provides an excellent user experience.
- Achieves high accessibility and performance standards.
- Remains easy to maintain.
- Evolves through small, well-tested, well-documented improvements.
