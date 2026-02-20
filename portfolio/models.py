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

    # Hero
    intro = models.TextField()
    hero_image_light = models.ImageField(
        upload_to="case_studies",
        blank=True,
        null=True,
    )
    hero_image_dark = models.ImageField(
        upload_to="case_studies",
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
