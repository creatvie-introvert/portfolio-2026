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

## Task 002

### Title

Fix shared SEO metadata and sitemap output

### Status

In Progress

### Priority

High

---

### Problem

Several non-home pages inherit the homepage metadata instead of outputting metadata for their own route.

Current issues include:

- Work, case-study, and legal pages declare the homepage as their canonical URL.
- Non-home pages output the homepage as their Open Graph URL.
- Legal pages render the generic title `Portfolio 2026`.
- Case-study titles use `project.title`, but the model field is `project.name`.
- The contact POST endpoint is included in the sitemap even though it is not a standalone page.
- The project sitemap can include unpublished projects.

This may cause incorrect search indexing, duplicate-page signals, and inaccurate social sharing previews.

---

### Acceptance Criteria

- [ ] Every indexable page outputs its own canonical URL.
- [ ] Every indexable page outputs its own Open Graph URL.
- [ ] The Work page has a specific page title and metadata.
- [ ] Each case study uses `project.name` in its page title.
- [ ] Each case study has route-specific title, description, canonical URL, and Open Graph URL.
- [ ] Privacy, Accessibility, and Terms pages output their supplied page titles and route-specific metadata.
- [ ] `/contact/` is removed from the sitemap.
- [ ] Project sitemap entries include only projects where `is_published=True`.
- [ ] Existing homepage metadata remains unchanged.
- [ ] No visual layout changes are introduced.
- [ ] `DEBUG=True .venv/bin/python manage.py check` passes.
- [ ] Relevant automated tests are added where appropriate.

---

### Investigation Notes

Pending Codex investigation.

---

### Files Likely Involved

- `core/templates/core/base.html`
- `core/templates/core/legal.html`
- `portfolio/templates/portfolio/work.html`
- `portfolio/templates/portfolio/case_study.html`
- `core/sitemaps.py`
- Relevant view or test files

These files are provisional and must be verified before implementation.

---

### Testing Required

#### Automated

- Django system check
- Metadata tests for homepage, Work, case studies, and legal pages
- Sitemap tests for unpublished projects and the contact endpoint

#### Manual

Verify page source for:

- Homepage
- Work page
- All published case studies
- Privacy page
- Accessibility page
- Terms page

Confirm that each page has:

- Correct `<title>`
- Correct canonical URL
- Correct `og:url`
- Correct page-specific social title and description where applicable

---

# Blocked

No blocked tasks.

---

# Completed

## Task 004

### Title

Strengthen the contact form

### Status

✅ Complete

### Priority

High

---

### Problem

The contact endpoint performed only basic presence checks, discarded submitted values after errors, ignored privacy consent, and had no meaningful spam protection.

---

### Acceptance Criteria

- [x] Dedicated Django form provides authoritative server-side validation
- [x] Name, email, and message validation rules enforced
- [x] Privacy consent required server-side
- [x] Invalid submissions retain user input
- [x] Validation errors render inline with an accessible summary
- [x] Honeypot field rejects likely automated submissions
- [x] Existing success redirect and modal preserved
- [x] Email-only delivery preserved
- [x] Existing responsive form layout preserved
- [x] Comprehensive regression tests added
- [x] No CAPTCHA, timing token, rate limiter, dependency, model, or migration added

---

### Root Cause

The view read raw POST values instead of using Django’s form-validation system. Invalid requests redirected to a new homepage request, browser-only consent could be bypassed, and every request containing three truthy strings reached the email backend.

---

### Solution

- Added a dedicated `ContactForm` with whitespace, length, email, consent, and honeypot validation.
- Rendered bound forms after validation and email-delivery errors.
- Added accessible error summaries, inline errors, invalid-field relationships, and focus handling.
- Continued to redirect successful submissions to the existing success modal.
- Added regression coverage for validation, preservation, consent, spam protection, email delivery, delivery failure, CSRF, and routing.

---

### Testing

#### Automated

- `env -u DEBUG .venv/bin/python manage.py check`
- `env -u DEBUG .venv/bin/python manage.py test`
- `git diff --check`

#### Manual

- Verify valid, invalid, and failed-delivery form states.
- Verify keyboard and screen-reader relationships for the error summary and fields.
- Verify the honeypot remains hidden and outside the Tab order.
- Verify light and dark themes at all supported responsive widths.

---

### Completed

28 July 2026

---

## Task 003

### Title

Proper skip link accessibility fix

### Status

✅ Complete

### Priority

High

---

### Problem

The Home navigation link incorrectly used the `skip-link` class. This hid Home off-screen by default and left the page without a dedicated link for bypassing repeated navigation.

---

### Acceptance Criteria

- [x] Dedicated “Skip to main content” link added as the first focusable element in the page body
- [x] Skip link points to `#main-content`
- [x] Shared main content has one unique `main-content` target
- [x] Main-content target can receive focus without entering the normal Tab sequence
- [x] Home behaves as a normal navigation link
- [x] Existing navigation design and behaviour preserved
- [x] Regression test added
- [x] Django system check passes
- [x] Full automated test suite passes
- [x] `git diff --check` passes

---

### Root Cause

The existing off-screen `.skip-link` styling was attached to the Home navigation link instead of a dedicated accessibility link. The shared main element also lacked a fragment target.

---

### Solution

- Added a dedicated skip link to the shared base template.
- Added `id="main-content"` and `tabindex="-1"` to the shared main element.
- Removed the `skip-link` class from Home.
- Reused the existing skip-link CSS.
- Added regression coverage for the shared markup.

---

### Testing

#### Automated

- ✅ `.venv/bin/python manage.py check`
- ✅ `.venv/bin/python manage.py test`
- ✅ `git diff --check`

Result:

```
System check identified no issues (0 silenced).
Ran 10 tests.
OK
```

#### Manual

- Confirm the first Tab press reveals the skip link.
- Confirm Enter moves focus to the main content.
- Confirm Home remains visible and behaves as normal navigation.
- Confirm the focused skip link is visible in light and dark themes.

---

### Completed

28 July 2026

---

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

- Use `env -u DEBUG` when running Django validation through Codex because the Codex command runner injects `DEBUG=release` into subprocesses.
- Review the local static-files setup to remove the missing `staticfiles/` directory warning during tests.
- Review overall visual polish
- Improve project case studies
- Improve homepage copy
- Accessibility audit
- Lighthouse performance improvements
