# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog.

---

## [Unreleased]

### Added

- Added ordered, reusable case-study sections and section media.
- Added dependency-free admin authoring and regression coverage for structured case studies.
- Added responsive, accessible custom 404 and 500 error pages with safe fallback navigation.
- Added a locally hosted GSAP 3.15.0 motion foundation and restrained
  homepage hero entrance.

### Changed

- Existing case studies retain legacy rendering until structured content is explicitly enabled.
- Case-study views now prefetch ordered sections, media, tags, and related projects.
- Replaced the hidden-by-default reveal system with opt-in, progressively
  enhanced motion that respects reduced-motion preferences.

### Fixed

- Added a dedicated main-content skip link and restored the Home link to normal navigation behaviour.
- Strengthened contact-form validation, preserved invalid submissions, enforced privacy consent, and added honeypot spam protection.
- Corrected legacy case-study markup, reflection rendering, project-card links, thumbnail alt text, and related-project queries.

---

## [0.1.0] - 2026-07-27

### Added

- Initial AI-assisted development workflow.
- Added `AGENTS.md`.
- Added `PROJECT.md`.
- Added `TASKS.md`.
- Added `TESTING.md`.
- Added `PROMPTS.md`.

### Fixed

- Fixed mobile overflow in the contact section.
- Long email addresses now wrap correctly.
- Contact form no longer exceeds the viewport on small devices.
- Restored consistent mobile spacing below 390px.

### Testing

- Django system check passed.
- Verified on desktop browsers.
- Verified on a real iPhone across multiple breakpoints.
