# Manual Testing Checklist

## Desktop

- Homepage
- Navigation
- Theme switch
- Hero
- Projects
- Contact form
- Footer

---

## Mobile

320px

375px

390px

430px

Check:

- No horizontal scrolling

- Cards fit viewport

- Images responsive

- Buttons accessible

- Navigation works

- Forms usable

- Footer fits

---

## Accessibility

- Press Tab immediately after loading the page.
- Confirm “Skip to main content” appears above the header.
- Press Enter and confirm focus moves to the main content.
- Confirm Home remains visible and behaves as normal navigation.
- Repeat the skip-link check in light and dark themes.

Visible focus states

Alt text

ARIA labels

Colour contrast

---

## Automated Tests

Run:

```text
.venv/bin/python manage.py check
.venv/bin/python manage.py test
git diff --check
```

Expected:

- Django reports no system-check issues.
- All tests pass, including the shared skip-link and contact-form regression tests.
- Git reports no whitespace errors.

---

## Contact Form

Automated coverage includes:

- Required, whitespace, length and email validation.
- Mandatory server-side privacy consent.
- Preservation of submitted values after errors.
- Honeypot rejection without email delivery.
- Successful email construction and delivery handling.
- Email-backend failure handling.
- CSRF enforcement and contact-route behaviour.

Manual checks:

- Submit valid and invalid enquiries.
- Confirm valid values remain populated when another field fails.
- Confirm errors are visible, linked to fields and announced appropriately.
- Confirm privacy consent cannot be omitted.
- Confirm the honeypot is hidden and absent from keyboard navigation.
- Confirm successful submissions still show the existing success modal.
- Check light and dark themes at all supported responsive widths.

---

## Reusable Case Studies

Automated coverage includes:

- Section and media ordering.
- Repeated and optional section types.
- Structured and legacy rendering modes.
- Empty-section omission.
- Authored and decorative image alt text.
- Optional media captions.
- Project-card link fallbacks.
- Heading, metadata, publication, and sitemap regressions.

Manual checks:

- Confirm existing legacy case studies still display all current content.
- Using a local test case study, confirm structured sections follow their
  configured order.
- Confirm empty structured sections do not appear.
- Confirm media remains responsive without horizontal scrolling.
- Confirm captions appear only when supplied.
- Inspect informative and decorative image alt text.
- Confirm projects without a case study do not show a case-study link.
- Confirm case studies without a live URL do not show a live link.
- Check light and dark themes at all supported responsive widths.

---

## Error Pages

Automated coverage runs with `DEBUG=False` and includes:

- Unknown URLs returning the custom 404 page and status.
- Safe standalone 500-handler rendering and status.
- One h1 per error page.
- Homepage and Work links.
- `noindex, nofollow` metadata.
- Exclusion of traceback, exception, secret, and request details.

Manual checks:

- Trigger an unknown URL and a temporary runtime-only server error with
  `DEBUG=False`.
- Confirm 404 and 500 status codes in the browser network panel.
- Confirm both links work without JavaScript.
- Confirm keyboard focus, skip links, 200% zoom, and no horizontal scrolling.
- Check light and dark themes at all supported responsive widths.
- Confirm no technical error details are visible.

---

## Motion System

Automated coverage includes:

- Homepage-only loading of pinned GSAP, ScrollTrigger, and `motion.js`.
- Dependency order and deferred script loading.
- Exclusion of motion assets from Work, legal, 404, and 500 pages.
- Approved semantic homepage hero hooks.
- Removal of the old `.animate` reveal system.
- Visible-by-default motion targets.
- Defensive GSAP checks, conditional ScrollTrigger registration, and
  `gsap.matchMedia()` reduced-motion handling.
- Confirmation that Task 007A creates no ScrollTrigger animation.

Manual checks:

- Confirm the homepage hero copy enters in the intended five-item order and the
  illustration enters independently.
- Test at 320, 375, 390, 430, 768, 1024 pixels and desktop.
- Test light and dark themes and resize across the 992-pixel breakpoint.
- Confirm content remains visible with JavaScript disabled.
- Block GSAP, ScrollTrigger, and `motion.js` separately and confirm safe
  fallback behaviour.
- Enable reduced motion before loading and change it after loading.
- Confirm keyboard focus, hero links, browser history, and navigation remain
  unaffected.
- Simulate a slow network and confirm there is no persistent hidden content,
  empty gap, or obvious backward jump.
- Confirm completed animation styles are cleared in browser developer tools.

Task 007A is not complete until this manual QA passes.

---

## Browser Testing

Chrome

Safari

Firefox

Edge

---

## Performance

Run:

python manage.py check

Check browser console.

Check Lighthouse.

Fix new warnings.
