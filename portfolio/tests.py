from html.parser import HTMLParser

from django.test import TestCase, override_settings
from django.template.defaultfilters import date
from django.urls import reverse

from .models import CaseStudy, Project, Tag


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


def create_case_study(project):
    return CaseStudy.objects.create(
        project=project,
        intro="Case-study introduction.",
        role="Designer and developer",
        stack="Django, HTML, CSS",
        timeline="Two weeks",
        problem="The project problem.",
        goals="Deliver a clear experience",
        process_discover="Research the problem.",
        process_design="Design the solution.",
        process_build="Build the product.",
        process_refine_launch="Test and launch.",
        solution_intro="The solution.",
        solution_1_title="Solution one",
        solution_1_body="Solution one details.",
        solution_2_title="Solution two",
        solution_2_body="Solution two details.",
        solution_3_title="Solution three",
        solution_3_body="Solution three details.",
        outcome_intro="The outcome.",
        outcome_bullets="A useful result",
        reflection_intro="The reflection.",
        reflection_body="What was learned.",
    )


@override_settings(STORAGES=TEST_STORAGES)
class WorkMetadataTests(TestCase):
    def test_work_page_uses_page_specific_metadata(self):
        response = self.client.get(
            reverse("work"),
            HTTP_HOST="localhost",
        )
        metadata = get_head_metadata(response)
        description = (
            "Browse selected web development projects and UX case studies, "
            "including real-world builds and portfolio work."
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(metadata["title"], "Work | Leanne Bedeau-Rogers")
        self.assertEqual(metadata["description"], description)
        self.assertEqual(
            metadata["canonical"],
            "https://leannebedeaurogers.com/portfolio/work/",
        )
        self.assertEqual(
            metadata["og:title"],
            "Work | Leanne Bedeau-Rogers",
        )
        self.assertEqual(metadata["og:description"], description)
        self.assertEqual(
            metadata["og:url"],
            "https://leannebedeaurogers.com/portfolio/work/",
        )
        self.assertEqual(
            metadata["twitter:title"],
            "Work | Leanne Bedeau-Rogers",
        )
        self.assertEqual(metadata["twitter:description"], description)

    def test_filtered_work_page_canonicalises_to_unfiltered_route(self):
        project = Project.objects.create(
            name="Published project",
            slug="published-project",
            short_description="A published project.",
        )
        tag = Tag.objects.create(name="Django", slug="django")
        project.tags.add(tag)

        response = self.client.get(
            f"{reverse('work')}?tag={tag.slug}",
            HTTP_HOST="localhost",
        )
        metadata = get_head_metadata(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            metadata["canonical"],
            "https://leannebedeaurogers.com/portfolio/work/",
        )


@override_settings(STORAGES=TEST_STORAGES)
class CaseStudyMetadataTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Accessible Portfolio",
            slug="accessible-portfolio",
            short_description="An accessible portfolio case study.",
        )
        self.case_study = create_case_study(self.project)
        self.url = reverse("case_study", args=[self.project.slug])

    def test_case_study_uses_project_metadata(self):
        response = self.client.get(self.url, HTTP_HOST="localhost")
        metadata = get_head_metadata(response)
        full_title = (
            "Accessible Portfolio | Case Study | Leanne Bedeau-Rogers"
        )
        absolute_url = (
            "https://leannebedeaurogers.com"
            "/portfolio/work/accessible-portfolio"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(metadata["title"], full_title)
        self.assertEqual(
            metadata["description"],
            self.project.short_description,
        )
        self.assertEqual(metadata["canonical"], absolute_url)
        self.assertEqual(metadata["og:title"], full_title)
        self.assertEqual(
            metadata["og:description"],
            self.project.short_description,
        )
        self.assertEqual(metadata["og:url"], absolute_url)
        self.assertEqual(metadata["twitter:title"], full_title)
        self.assertEqual(
            metadata["twitter:description"],
            self.project.short_description,
        )

    def test_case_study_article_dates_use_model_timestamps(self):
        response = self.client.get(self.url, HTTP_HOST="localhost")
        metadata = get_head_metadata(response)

        self.assertEqual(
            metadata["article:published_time"],
            date(self.case_study.created_at, "c"),
        )
        self.assertEqual(
            metadata["article:modified_time"],
            date(self.case_study.updated_at, "c"),
        )


class ProjectSitemapTests(TestCase):
    def test_sitemap_includes_published_and_excludes_unpublished_projects(self):
        published = Project.objects.create(
            name="Published project",
            slug="published-project",
            short_description="A published project.",
            is_published=True,
        )
        unpublished = Project.objects.create(
            name="Unpublished project",
            slug="unpublished-project",
            short_description="An unpublished project.",
            is_published=False,
        )

        response = self.client.get("/sitemap.xml", HTTP_HOST="localhost")
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            f"<loc>http://localhost{reverse('case_study', args=[published.slug])}</loc>",
            content,
        )
        self.assertNotIn(
            f"<loc>http://localhost{reverse('case_study', args=[unpublished.slug])}</loc>",
            content,
        )

    def test_unpublished_case_study_route_returns_404(self):
        project = Project.objects.create(
            name="Unpublished project",
            slug="unpublished-project",
            short_description="An unpublished project.",
            is_published=False,
        )
        create_case_study(project)

        response = self.client.get(
            reverse("case_study", args=[project.slug]),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 404)
