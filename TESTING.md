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
