from django.shortcuts import render
from .models import Project, Tag


def work(request):
    # Multi-select: /work/?tag=django&tag=ux
    selected_tag_slugs = request.GET.getlist("tag")

    # Base queryset: all published projects
    projects = (
        Project.objects
        .filter(is_published=True)
        .prefetch_related("tags")
    )

    # Tags for the filter UI (only tags linked to published projects)
    tags = (
        Tag.objects
        .filter(projects__is_published=True)
        .distinct()
        .order_by("name")
    )

    # OR logic: must match at least 1 selected tag
    if selected_tag_slugs:
        projects = projects.filter(tags__slug__in=selected_tag_slugs)

    context = {
        "projects": projects.distinct(),
        "tags": tags,
        "selected_tag_slugs": selected_tag_slugs,
    }

    return render(request, "portfolio/work.html", context)
