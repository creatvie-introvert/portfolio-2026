from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import (
    CaseStudy,
    CaseStudyMedia,
    CaseStudySection,
    Project,
    Tag,
)


def work(request):
    # Multi-select: /work/?tag=django&tag=ux
    selected_tag_slugs = request.GET.getlist("tag")

    # Get valid tag slugs from DB
    valid_slugs = list(
        Tag.objects
        .filter(slug__in=selected_tag_slugs)
        .values_list("slug", flat=True)
    )

    # If invalid slug exists → redirect to cleaned URL
    if set(selected_tag_slugs) != set(valid_slugs):
        if valid_slugs:
            query = "&".join([f"tag={slug}" for slug in valid_slugs])
            return redirect(f"{reverse('work')}?{query}")
        return redirect(reverse("work"))

    # Base queryset: all published projects
    projects = (
        Project.objects
        .filter(is_published=True)
        .select_related("case_study")
        .prefetch_related("tags")
    )

    if valid_slugs:
        projects = projects.filter(tags__slug__in=valid_slugs)

    # Tags for the filter UI (only tags linked to published projects)
    tags = (
        Tag.objects
        .filter(projects__is_published=True)
        .distinct()
        .order_by("name")
    )

    context = {
        "projects": projects.distinct(),
        "tags": tags,
        "selected_tag_slugs": selected_tag_slugs,
    }

    return render(request, "portfolio/work.html", context)


def case_study(request, slug):
    media_queryset = CaseStudyMedia.objects.order_by("sort_order", "pk")
    section_queryset = (
        CaseStudySection.objects
        .order_by("sort_order", "pk")
        .prefetch_related(
            Prefetch(
                "media",
                queryset=media_queryset,
                to_attr="ordered_media",
            )
        )
    )

    case_study = get_object_or_404(
        CaseStudy.objects
        .select_related("project")
        .prefetch_related(
            "project__tags",
            Prefetch(
                "sections",
                queryset=section_queryset,
                to_attr="ordered_sections",
            ),
        ),
        project__slug=slug,
        project__is_published=True,
    )
    project = case_study.project

    structured_sections = [
        section
        for section in case_study.ordered_sections
        if section.body.strip() or section.ordered_media
    ]

    other_projects = (
        Project.objects
        .filter(is_published=True, case_study__isnull=False)
        .exclude(pk=project.pk)
        .select_related("case_study")
        .prefetch_related("tags")
        .order_by("-created_at")[:3]
    )

    context = {
        "project": project,
        "case_study": case_study,
        "structured_sections": structured_sections,
        "other_projects": other_projects,
    }

    return render(request, "portfolio/case_study.html", context)
