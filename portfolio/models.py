from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    short_description = models.CharField(max_length=180)

    thumbnail = models.ImageField(
        upload_to="projects/thumbnails/",
        blank=True,
        null=True,
    )
    thumbnail_alt = models.CharField(max_length=255, blank=True)

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class CaseStudy(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="case_study",
    )
    use_structured_sections = models.BooleanField(default=False)

    # Hero
    intro = models.TextField()
    hero_image_light = models.ImageField(
        upload_to="case-studies/hero/",
        blank=True,
        null=True,
    )
    hero_image_dark = models.ImageField(
        upload_to="case-studies/hero/",
        blank=True,
        null=True,
    )

    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)

    # Overview cards
    role = models.CharField(max_length=120)
    stack = models.CharField(max_length=160)
    timeline = models.CharField(max_length=120)

    # Problem
    problem = models.TextField()

    # Goals (bullet list)
    goals = models.TextField(help_text="Store as one bullet per line")

    # Process cards
    process_discover = models.TextField()
    process_design = models.TextField()
    process_build = models.TextField()
    process_refine_launch = models.TextField()

    # Solution section intro
    solution_intro = models.TextField()

    # Solution blocks (3)
    solution_1_title = models.CharField(max_length=120)
    solution_1_body = models.TextField()
    solution_1_image_light = models.ImageField(
        upload_to="case-studies/solutions/",
        blank=True,
        null=True,
    )
    solution_1_image_dark = models.ImageField(
        upload_to="case-studies/solutions/",
        blank=True,
        null=True,
    )

    solution_2_title = models.CharField(max_length=120)
    solution_2_body = models.TextField()
    solution_2_image_light = models.ImageField(
        upload_to="case-studies/solutions/",
        blank=True,
        null=True,
    )
    solution_2_image_dark = models.ImageField(
        upload_to="case-studies/solutions/",
        blank=True,
        null=True,
    )

    solution_3_title = models.CharField(max_length=120)
    solution_3_body = models.TextField()
    solution_3_image_light = models.ImageField(
        upload_to="case-studies/solutions/",
        blank=True,
        null=True,
    )
    solution_3_image_dark = models.ImageField(
        upload_to="case-studies/solutions/",
        blank=True,
        null=True
    )

    # Outcome
    outcome_intro = models.TextField()
    outcome_bullets = models.TextField(
        help_text="Store as one bullet per line",
    )

    # Reflection
    reflection_intro = models.TextField()
    reflection_body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Case Study: {self.project.name}"


class CaseStudySection(models.Model):
    class SectionType(models.TextChoices):
        PROBLEM = "problem", "Problem"
        USERS_AND_GOALS = "users_and_goals", "Users and goals"
        CONSTRAINTS = "constraints", "Constraints"
        ROLE = "role", "Role and responsibilities"
        RESEARCH_AND_PLANNING = (
            "research_and_planning",
            "Research and planning",
        )
        SOLUTION = "solution", "Solution"
        TECHNICAL_DECISIONS = (
            "technical_decisions",
            "Technical decisions",
        )
        CHALLENGES_AND_TRADEOFFS = (
            "challenges_and_tradeoffs",
            "Challenges and trade-offs",
        )
        TESTING = "testing", "Testing"
        ACCESSIBILITY = "accessibility", "Accessibility"
        RESULTS = "results", "Results"
        LESSONS_LEARNED = "lessons_learned", "Lessons learned"
        IMPROVEMENTS = "improvements", "What I would improve next"
        DEVELOPMENT_PROCESS = (
            "development_process",
            "Development process",
        )

    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    section_type = models.CharField(
        max_length=40,
        choices=SectionType.choices,
    )
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.title or self.get_section_type_display()


class CaseStudyMedia(models.Model):
    class MediaType(models.TextChoices):
        PRODUCT = "product", "Product"
        MOBILE = "mobile", "Mobile"
        DESKTOP = "desktop", "Desktop"
        PROCESS = "process", "Process"
        DIAGRAM = "diagram", "Diagram"
        TESTING_EVIDENCE = "testing_evidence", "Testing evidence"
        BEFORE = "before", "Before"
        AFTER = "after", "After"

    section = models.ForeignKey(
        CaseStudySection,
        on_delete=models.CASCADE,
        related_name="media",
    )
    image = models.ImageField(upload_to="case-studies/sections/")
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)
    media_type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return f"{self.section}: {self.get_media_type_display()}"
