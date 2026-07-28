from html.parser import HTMLParser

from django.test import TestCase, override_settings


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
