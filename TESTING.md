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
- All tests pass, including the shared skip-link regression test.
- Git reports no whitespace errors.

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
