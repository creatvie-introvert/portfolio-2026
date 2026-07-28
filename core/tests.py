from html.parser import HTMLParser
from unittest.mock import patch

from django.core import mail
from django.test import Client, TestCase, override_settings

from .forms import ContactForm


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


class HeadMetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metadata = {}
        self._in_title = False
        self._title_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = attributes.get("name") or attributes.get("property")
            if key:
                self.metadata[key] = attributes.get("content", "").strip()
        elif tag == "link" and attributes.get("rel") == "canonical":
            self.metadata["canonical"] = attributes.get("href", "").strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.metadata["title"] = "".join(self._title_parts).strip()

    def handle_data(self, data):
        if self._in_title:
            self._title_parts.append(data)


def get_head_metadata(response):
    parser = HeadMetadataParser()
    parser.feed(response.content.decode())
    return parser.metadata


@override_settings(STORAGES=TEST_STORAGES)
class SkipLinkAccessibilityTests(TestCase):
    def test_shared_layout_has_dedicated_main_content_skip_link(self):
        response = self.client.get("/", HTTP_HOST="localhost")
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="skip-link" href="#main-content">'
            "Skip to main content</a>",
            html=True,
        )
        self.assertContains(
            response,
            '<main id="main-content" tabindex="-1">',
            count=1,
        )
        self.assertNotIn('class="nav-link skip-link"', content)
        self.assertContains(
            response,
            '<a href="/" class="nav-link">Home</a>',
            html=True,
        )


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="sender@example.com",
    STORAGES=TEST_STORAGES,
)
class ContactFormTests(TestCase):
    def valid_data(self, **overrides):
        data = {
            "name": "Leanne",
            "email": "leanne@example.com",
            "message": "I would like to discuss a project.",
            "privacy": "1",
            "contact_reference": "",
        }
        data.update(overrides)
        return data

    def test_homepage_renders_contact_form_and_honeypot(self):
        response = self.client.get("/", HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["contact_form"], ContactForm)
        self.assertContains(response, 'name="privacy"')
        self.assertContains(response, 'name="contact_reference"')
        self.assertContains(response, 'class="contact-form__honeypot"')
        self.assertContains(response, 'autocomplete="one-time-code"')
        self.assertContains(response, 'tabindex="-1"')
        self.assertContains(response, 'aria-hidden="true"')
        self.assertContains(response, 'data-1p-ignore="true"')
        self.assertContains(response, 'data-lpignore="true"')
        self.assertContains(response, 'data-bwignore="true"')

    def test_valid_submission_sends_email_and_redirects_to_success(self):
        response = self.client.post(
            "/contact/",
            self.valid_data(
                name="  Leanne  ",
                message="  A valid project enquiry.  ",
            ),
            HTTP_HOST="localhost",
        )

        self.assertRedirects(
            response,
            "/?contact=success",
            fetch_redirect_response=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ["leanne@example.com"])
        self.assertIn("Name: Leanne", mail.outbox[0].body)
        self.assertIn("A valid project enquiry.", mail.outbox[0].body)

    def test_invalid_submission_preserves_values_and_shows_inline_errors(self):
        response = self.client.post(
            "/contact/",
            self.valid_data(
                email="not-an-email",
                message="Hello from the preserved message field.",
            ),
            HTTP_HOST="localhost",
        )
        form = response.context["contact_form"]

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", form.errors)
        self.assertEqual(
            form["message"].value(),
            "Hello from the preserved message field.",
        )
        self.assertIs(form["privacy"].value(), True)
        self.assertContains(
            response,
            'id="contact-error-summary"',
            status_code=400,
        )
        self.assertContains(
            response,
            'aria-invalid="true"',
            status_code=400,
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_privacy_consent_is_required_server_side(self):
        data = self.valid_data()
        data.pop("privacy")

        response = self.client.post(
            "/contact/",
            data,
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("privacy", response.context["contact_form"].errors)
        self.assertEqual(len(mail.outbox), 0)

    def test_name_email_and_message_validation_rules(self):
        invalid_values = (
            ("name", "   "),
            ("name", "n" * 101),
            ("email", "invalid"),
            ("email", f"{'a' * 245}@example.com"),
            ("message", "   "),
            ("message", "four"),
            ("message", "m" * 3001),
        )

        for field_name, value in invalid_values:
            with self.subTest(field=field_name, value_length=len(value)):
                form = ContactForm(
                    self.valid_data(**{field_name: value})
                )

                self.assertFalse(form.is_valid())
                self.assertIn(field_name, form.errors)

    def test_honeypot_must_remain_empty(self):
        response = self.client.post(
            "/contact/",
            self.valid_data(contact_reference="automated value"),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            response.context["contact_form"].non_field_errors()
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_visible_fields_do_not_populate_honeypot(self):
        data = self.valid_data()
        data.pop("contact_reference")
        form = ContactForm(data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["contact_reference"], "")

    @patch("core.views.EmailMessage.send", side_effect=RuntimeError)
    def test_email_failure_preserves_values_and_shows_error(self, _send):
        response = self.client.post(
            "/contact/",
            self.valid_data(message="Please preserve this enquiry."),
            HTTP_HOST="localhost",
        )
        form = response.context["contact_form"]

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            form["message"].value(),
            "Please preserve this enquiry.",
        )
        self.assertTrue(form.non_field_errors())

    def test_contact_get_redirects_to_homepage(self):
        response = self.client.get("/contact/", HTTP_HOST="localhost")

        self.assertRedirects(
            response,
            "/",
            fetch_redirect_response=False,
        )

    def test_contact_post_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            "/contact/",
            self.valid_data(),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(mail.outbox), 0)


@override_settings(STORAGES=TEST_STORAGES)
class HomepageMetadataTests(TestCase):
    def test_homepage_metadata_remains_unchanged(self):
        response = self.client.get("/", HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            get_head_metadata(response),
            {
                "title": "UX Developer Portfolio | Leanne Bedeau-Rogers",
                "viewport": "width=device-width, initial-scale=1",
                "description": (
                    "UX-led Full Stack Developer portfolio. Explore projects, "
                    "case studies, and scalable web apps built with Django, "
                    "JavaScript, and modern UI design principles."
                ),
                "author": "Leanne Bedeau-Rogers",
                "article:author": "Leanne Bedeau-Rogers",
                "canonical": "https://leannebedeaurogers.com/",
                "og:title": "UX Developer Portfolio | Leanne Bedeau-Rogers",
                "og:description": (
                    "Explore UX-focused web development projects, case studies, "
                    "and accessible builds."
                ),
                "og:url": "https://leannebedeaurogers.com/",
                "og:type": "website",
                "og:image": (
                    "https://leannebedeaurogers.com/static/core/img/og-image.png"
                ),
                "og:image:width": "1200",
                "og:image:height": "630",
                "twitter:card": "summary_large_image",
                "twitter:title": "Portfolio 2026",
                "twitter:description": (
                    "UX-led web developer portfolio showcasing selected "
                    "projects and case studies."
                ),
                "twitter:image": (
                    "https://leannebedeaurogers.com/static/core/img/og-image.png"
                ),
                "theme-color": "#000000",
            },
        )


@override_settings(STORAGES=TEST_STORAGES)
class LegalMetadataTests(TestCase):
    def test_legal_pages_use_page_specific_metadata(self):
        pages = (
            (
                "/privacy/",
                "Privacy Policy",
                (
                    "Read the privacy policy for leannebedeaurogers.com and "
                    "understand how your data is used."
                ),
                "Read the privacy policy for leannebedeaurogers.com.",
            ),
            (
                "/accessibility/",
                "Accessibility Statement",
                (
                    "Accessibility statement for leannebedeaurogers.com, "
                    "outlining usability and inclusivity standards."
                ),
                "Accessibility statement for leannebedeaurogers.com.",
            ),
            (
                "/terms/",
                "Terms of Use",
                (
                    "Terms of use for leannebedeaurogers.com explaining how "
                    "the website and content can be used."
                ),
                "Terms of use for leannebedeaurogers.com.",
            ),
        )

        for path, title, description, social_description in pages:
            with self.subTest(path=path):
                response = self.client.get(path, HTTP_HOST="localhost")
                metadata = get_head_metadata(response)
                full_title = f"{title} | Leanne Bedeau-Rogers"
                absolute_url = f"https://leannebedeaurogers.com{path}"

                self.assertEqual(response.status_code, 200)
                self.assertEqual(metadata["title"], full_title)
                self.assertEqual(metadata["description"], description)
                self.assertEqual(metadata["canonical"], absolute_url)
                self.assertEqual(metadata["og:title"], full_title)
                self.assertEqual(
                    metadata["og:description"],
                    social_description,
                )
                self.assertEqual(metadata["og:url"], absolute_url)
                self.assertEqual(metadata["twitter:title"], full_title)
                self.assertEqual(
                    metadata["twitter:description"],
                    social_description,
                )


class StaticSitemapTests(TestCase):
    def test_static_sitemap_contains_pages_but_not_contact_endpoint(self):
        response = self.client.get("/sitemap.xml", HTTP_HOST="localhost")
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        for path in (
            "/",
            "/privacy/",
            "/accessibility/",
            "/terms/",
            "/portfolio/work/",
        ):
            with self.subTest(path=path):
                self.assertIn(f"<loc>http://localhost{path}</loc>", content)

        self.assertNotIn("<loc>http://localhost/contact/</loc>", content)
