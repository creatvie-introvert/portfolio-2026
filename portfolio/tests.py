from html.parser import HTMLParser

from django.conf import settings
from django.test import TestCase, override_settings
from django.template.defaultfilters import date
from django.urls import reverse

from .models import (
    CaseStudy,
    CaseStudyMedia,
    CaseStudySection,
    Project,
    Tag,
)


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MOTION_ASSETS = (
    "/static/core/vendor/gsap/3.15.0/gsap.min.js",
    "/static/core/vendor/gsap/3.15.0/ScrollTrigger.min.js",
    "/static/core/js/motion.js",
)


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


def create_case_study(project, **overrides):
    values = {
        "project": project,
        "intro": "Case-study introduction.",
        "role": "Designer and developer",
        "stack": "Django, HTML, CSS",
        "timeline": "Two weeks",
        "problem": "The project problem.",
        "goals": "Deliver a clear experience",
        "process_discover": "Research the problem.",
        "process_design": "Design the solution.",
        "process_build": "Build the product.",
        "process_refine_launch": "Test and launch.",
        "solution_intro": "The solution.",
        "solution_1_title": "Solution one",
        "solution_1_body": "Solution one details.",
        "solution_2_title": "Solution two",
        "solution_2_body": "Solution two details.",
        "solution_3_title": "Solution three",
        "solution_3_body": "Solution three details.",
        "outcome_intro": "The outcome.",
        "outcome_bullets": "A useful result",
        "reflection_intro": "The reflection.",
        "reflection_body": "What was learned.",
    }
    values.update(overrides)
    return CaseStudy.objects.create(**values)


class MotionAssetAssertions:
    def assert_motion_assets_loaded_once_in_order(self, response):
        content = response.content.decode()
        positions = []

        for asset in MOTION_ASSETS:
            self.assertEqual(content.count(asset), 1)
            self.assertContains(
                response,
                f'<script defer src="{asset}"></script>',
                html=True,
            )
            positions.append(content.index(asset))

        self.assertEqual(positions, sorted(positions))

    def assert_motion_assets_not_loaded(self, response):
        content = response.content.decode()

        for asset in MOTION_ASSETS:
            self.assertNotIn(asset, content)


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
class WorkMotionTests(MotionAssetAssertions, TestCase):
    def test_work_page_loads_motion_and_uses_card_level_hooks(self):
        Project.objects.create(
            name="First project",
            slug="first-project",
            short_description="First project.",
        )
        Project.objects.create(
            name="Second project",
            slug="second-project",
            short_description="Second project.",
        )

        response = self.client.get(reverse("work"), HTTP_HOST="localhost")
        content = response.content.decode()

        self.assert_motion_assets_loaded_once_in_order(response)
        self.assertEqual(
            content.count('data-motion-root="project-list"'),
            1,
        )
        self.assertEqual(content.count('data-motion="section-intro"'), 1)
        self.assertEqual(content.count('data-motion="project-grid"'), 1)
        self.assertEqual(content.count('data-motion="project-card"'), 2)

        project_card_partial = (
            settings.BASE_DIR
            / "portfolio"
            / "templates"
            / "portfolio"
            / "partials"
            / "project_card.html"
        ).read_text()
        self.assertNotIn("data-motion", project_card_partial)

    def test_empty_work_grid_has_no_card_hooks(self):
        response = self.client.get(reverse("work"), HTTP_HOST="localhost")
        content = response.content.decode()

        self.assert_motion_assets_loaded_once_in_order(response)
        self.assertEqual(content.count('data-motion="project-grid"'), 1)
        self.assertNotIn('data-motion="project-card"', content)
        self.assertContains(response, "No projects found for this tag yet.")


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


@override_settings(STORAGES=TEST_STORAGES)
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


class CaseStudyContentModelTests(TestCase):
    def setUp(self):
        project = Project.objects.create(
            name="Structured project",
            slug="structured-project",
            short_description="A structured project.",
        )
        self.case_study = create_case_study(project)

    def test_sections_are_ordered_and_types_can_repeat(self):
        later = CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.PROBLEM,
            title="Later problem",
            sort_order=20,
        )
        first = CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.PROBLEM,
            title="First problem",
            sort_order=10,
        )
        last = CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.PROBLEM,
            title="Last problem",
            sort_order=20,
        )

        self.assertEqual(
            list(self.case_study.sections.all()),
            [first, later, last],
        )
        self.assertEqual(
            self.case_study.sections.filter(
                section_type=CaseStudySection.SectionType.PROBLEM
            ).count(),
            3,
        )

    def test_media_is_ordered_and_optional_fields_can_be_blank(self):
        section = CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.SOLUTION,
        )
        later = CaseStudyMedia.objects.create(
            section=section,
            image="case-studies/sections/later.png",
            media_type=CaseStudyMedia.MediaType.DESKTOP,
            sort_order=20,
        )
        first = CaseStudyMedia.objects.create(
            section=section,
            image="case-studies/sections/first.png",
            alt_text="A product screen",
            caption="The completed product screen.",
            media_type=CaseStudyMedia.MediaType.PRODUCT,
            sort_order=10,
        )

        self.assertEqual(list(section.media.all()), [first, later])
        self.assertEqual(section.title, "")
        self.assertEqual(section.body, "")
        self.assertEqual(later.alt_text, "")
        self.assertEqual(later.caption, "")


@override_settings(STORAGES=TEST_STORAGES)
class CaseStudyStructuredRenderingTests(
    MotionAssetAssertions,
    TestCase,
):
    def setUp(self):
        self.project = Project.objects.create(
            name="Structured case study",
            slug="structured-case-study",
            short_description="A structured case study.",
        )
        self.case_study = create_case_study(self.project)
        self.url = reverse("case_study", args=[self.project.slug])

    def render_case_study(self):
        return self.client.get(self.url, HTTP_HOST="localhost")

    def test_legacy_content_renders_while_switch_is_false(self):
        CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.SOLUTION,
            title="Draft structured section",
            body="Draft structured body.",
        )

        response = self.render_case_study()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The project problem.")
        self.assertContains(response, "What was learned.")
        self.assertNotContains(response, "Draft structured section")
        self.assertNotContains(response, "Draft structured body.")
        self.assert_motion_assets_not_loaded(response)
        self.assertNotContains(
            response,
            'data-motion="case-study-section"',
        )

    def test_switch_with_no_renderable_sections_keeps_legacy_content(self):
        self.case_study.use_structured_sections = True
        self.case_study.save(update_fields=["use_structured_sections"])
        CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.TESTING,
            title="Empty draft section",
        )

        response = self.render_case_study()

        self.assertContains(response, "The project problem.")
        self.assertNotContains(response, "Empty draft section")
        self.assert_motion_assets_not_loaded(response)
        self.assertNotContains(
            response,
            'data-motion="case-study-section"',
        )

    def test_structured_sections_render_in_order_and_omit_empty_sections(self):
        self.case_study.use_structured_sections = True
        self.case_study.save(update_fields=["use_structured_sections"])
        CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.RESULTS,
            title="Second section",
            body="Second structured body.",
            sort_order=20,
        )
        CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.PROBLEM,
            title="First section",
            body="First structured body.",
            sort_order=10,
        )
        CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.TESTING,
            title="Omitted empty section",
            sort_order=15,
        )

        response = self.render_case_study()
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertLess(
            content.index("First section"),
            content.index("Second section"),
        )
        self.assertNotContains(response, "Omitted empty section")
        self.assertNotContains(response, "The project problem.")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(
            response,
            '<h2 class="h3 fw-semibold mb-0">',
            count=2,
        )
        self.assert_motion_assets_loaded_once_in_order(response)
        self.assertContains(
            response,
            'data-motion="case-study-section"',
            count=2,
        )
        self.assertEqual(
            content.count('data-motion="case-study-section"'),
            content.count("data-motion="),
        )

    def test_media_renders_ordered_accessible_markup_and_optional_caption(self):
        self.case_study.use_structured_sections = True
        self.case_study.save(update_fields=["use_structured_sections"])
        section = CaseStudySection.objects.create(
            case_study=self.case_study,
            section_type=CaseStudySection.SectionType.SOLUTION,
            body="Media evidence.",
        )
        CaseStudyMedia.objects.create(
            section=section,
            image="case-studies/sections/authored.png",
            alt_text="Dashboard showing ordered enquiries",
            caption="The staff enquiry dashboard.",
            media_type=CaseStudyMedia.MediaType.DESKTOP,
            sort_order=20,
        )
        CaseStudyMedia.objects.create(
            section=section,
            image="case-studies/sections/decorative.png",
            alt_text="",
            caption="",
            media_type=CaseStudyMedia.MediaType.PRODUCT,
            sort_order=10,
        )

        response = self.render_case_study()
        content = response.content.decode()

        self.assertLess(
            content.index("decorative.png"),
            content.index("authored.png"),
        )
        self.assertContains(response, 'alt=""')
        self.assertContains(
            response,
            'alt="Dashboard showing ordered enquiries"',
        )
        self.assertContains(response, 'loading="lazy"', count=2)
        self.assertContains(response, "<figure", count=2)
        self.assertContains(response, "<figcaption", count=1)
        self.assertContains(response, "The staff enquiry dashboard.")


@override_settings(STORAGES=TEST_STORAGES)
class ProjectCardRenderingTests(TestCase):
    def test_project_without_case_study_has_no_project_links(self):
        project = Project.objects.create(
            name="Catalogue-only project",
            slug="catalogue-only-project",
            short_description="A project without a case study.",
            thumbnail="projects/thumbnails/catalogue.jpg",
            thumbnail_alt="Catalogue project interface",
        )

        response = self.client.get(reverse("work"), HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            reverse("case_study", args=[project.slug]),
        )
        self.assertNotContains(response, "View live")
        self.assertContains(
            response,
            'alt="Catalogue project interface"',
        )

    def test_case_study_without_live_url_has_only_case_study_link(self):
        project = Project.objects.create(
            name="Case-study-only project",
            slug="case-study-only-project",
            short_description="A project without a live URL.",
        )
        create_case_study(project, live_url="")

        response = self.client.get(reverse("work"), HTTP_HOST="localhost")

        self.assertContains(
            response,
            reverse("case_study", args=[project.slug]),
        )
        self.assertContains(response, "View case study")
        self.assertNotContains(response, "View live")

    def test_related_projects_render_from_queryset(self):
        related_project = Project.objects.create(
            name="Related project",
            slug="related-project",
            short_description="Another published case study.",
        )
        create_case_study(related_project)
        project = Project.objects.create(
            name="Current project",
            slug="current-project",
            short_description="The current case study.",
        )
        create_case_study(project)

        response = self.client.get(
            reverse("case_study", args=[project.slug]),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "More work")
        self.assertContains(response, "Related project")
