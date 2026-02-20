from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Project, Tag, CaseStudy


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
    project = get_object_or_404(
        Project.objects.prefetch_related("tags"),
        slug=slug,
        is_published=True,
    )

    case_study = get_object_or_404(
        CaseStudy.objects.prefetch_related("project"),
        project=project,
    )

    context = {
        "project": project,
        "case_study": case_study,
    }

    return render(request, "portfolio/case_study.html", context)
